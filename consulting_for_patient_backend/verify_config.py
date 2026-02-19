#!/usr/bin/env python
"""
Script de vérification de la configuration e_sora
Vérifie que tous les fichiers utilisent le bon nom de base de données
"""

import os
import re
import sys

def check_file_content(filepath, search_patterns, expected_patterns):
    """Vérifie le contenu d'un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        issues = []
        
        # Vérifier les anciens patterns
        for pattern in search_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"❌ Trouvé ancien pattern: {pattern}")
        
        # Vérifier les nouveaux patterns
        found_expected = False
        for pattern in expected_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_expected = True
                break
        
        if not found_expected and expected_patterns:
            issues.append(f"⚠️  Pattern attendu non trouvé: {expected_patterns}")
        
        return issues
        
    except Exception as e:
        return [f"❌ Erreur lecture fichier: {e}"]

def main():
    """Fonction principale de vérification"""
    print("🔍 Vérification de la configuration e_sora")
    print("=" * 50)
    
    # Fichiers à vérifier
    files_to_check = {
        'mysite/settings.py': {
            'old_patterns': [r'consulting_for_patient_db'],
            'expected_patterns': [r'e_sora']
        },
        'setup_mysql.py': {
            'old_patterns': [r'consulting_for_patient_db', r'consulting_user'],
            'expected_patterns': [r'e_sora', r'e_sora_user']
        },
        'manage_db.py': {
            'old_patterns': [r'consulting_for_patient_db'],
            'expected_patterns': [r'e_sora']
        },
        'MIGRATION_MYSQL.md': {
            'old_patterns': [r'consulting_for_patient_db', r'consulting_user'],
            'expected_patterns': [r'e_sora', r'e_sora_user']
        },
        'README.md': {
            'old_patterns': [r'consulting_for_patient_db'],
            'expected_patterns': [r'e_sora']
        },
        'INSTRUCTIONS_MIGRATION.md': {
            'old_patterns': [r'consulting_for_patient_db'],
            'expected_patterns': [r'e_sora']
        }
    }
    
    all_good = True
    
    for filepath, patterns in files_to_check.items():
        if os.path.exists(filepath):
            print(f"\n📄 Vérification de {filepath}:")
            issues = check_file_content(
                filepath, 
                patterns['old_patterns'], 
                patterns['expected_patterns']
            )
            
            if issues:
                all_good = False
                for issue in issues:
                    print(f"   {issue}")
            else:
                print("   ✅ Configuration correcte")
        else:
            print(f"\n⚠️  Fichier non trouvé: {filepath}")
    
    # Vérification de la configuration Django
    print(f"\n🔧 Vérification de la configuration Django:")
    try:
        import django
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        django.setup()
        
        from django.conf import settings
        
        db_config = settings.DATABASES['default']
        
        if db_config['NAME'] == 'e_sora':
            print("   ✅ Nom de base de données: e_sora")
        else:
            print(f"   ❌ Nom de base de données incorrect: {db_config['NAME']}")
            all_good = False
        
        if db_config['PORT'] == '8888':
            print("   ✅ Port MySQL: 8888")
        else:
            print(f"   ⚠️  Port MySQL: {db_config['PORT']} (attendu: 8888)")
        
        print(f"   📍 Host: {db_config['HOST']}")
        print(f"   👤 User: {db_config['USER']}")
        
    except Exception as e:
        print(f"   ❌ Erreur configuration Django: {e}")
        all_good = False
    
    # Résumé
    print("\n" + "=" * 50)
    if all_good:
        print("✅ Configuration e_sora correcte !")
        print("\n🚀 Prochaines étapes:")
        print("1. python setup_mysql.py")
        print("2. python manage.py makemigrations")
        print("3. python manage.py migrate")
        print("4. python seed_database.py")
    else:
        print("❌ Des problèmes de configuration ont été détectés")
        print("Veuillez corriger les erreurs ci-dessus")
    
    # Vérification de la connexion MySQL (optionnel)
    print(f"\n🔌 Test de connexion MySQL:")
    try:
        import mysql.connector
        
        connection = mysql.connector.connect(
            host='localhost',
            port=8888,
            user='root',
            password=''
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'e_sora'")
            result = cursor.fetchone()
            
            if result:
                print("   ✅ Base de données e_sora existe")
            else:
                print("   ⚠️  Base de données e_sora n'existe pas encore")
            
            cursor.close()
            connection.close()
        
    except Exception as e:
        print(f"   ⚠️  Impossible de se connecter à MySQL: {e}")
        print("   💡 Assurez-vous que MySQL est démarré sur le port 8888")

if __name__ == "__main__":
    main()