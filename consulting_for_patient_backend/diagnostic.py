#!/usr/bin/env python3
"""
Script de diagnostic pour identifier le problème
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, os.path.dirname(__file__))

try:
    django.setup()
    print("✅ Django configuré avec succès\n")
except Exception as e:
    print(f"❌ Erreur de configuration Django: {e}\n")
    sys.exit(1)

from django.db import connection
from pf.models import EmployePharmacie

print("🔍 DIAGNOSTIC DU SYSTÈME\n")
print("=" * 50)

# 1. Vérifier la connexion à la base de données
print("\n1. Connexion à la base de données")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("   ✅ Connexion OK")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 2. Vérifier la table employes_pharmacies
print("\n2. Structure de la table employes_pharmacies")
try:
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(employes_pharmacies)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"   Colonnes trouvées: {len(column_names)}")
        
        # Vérifier les nouvelles colonnes
        if 'peut_annuler_vente' in column_names:
            print("   ✅ peut_annuler_vente existe")
        else:
            print("   ❌ peut_annuler_vente MANQUANTE")
        
        if 'peut_enregistrer_facture' in column_names:
            print("   ✅ peut_enregistrer_facture existe")
        else:
            print("   ❌ peut_enregistrer_facture MANQUANTE")
            
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 3. Vérifier les tables fournisseurs
print("\n3. Tables des factures fournisseurs")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%fournisseur%'")
        tables = cursor.fetchall()
        
        if tables:
            print(f"   ✅ Tables trouvées: {[t[0] for t in tables]}")
        else:
            print("   ❌ Aucune table fournisseur trouvée")
            
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 4. Vérifier les migrations
print("\n4. Migrations appliquées")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM django_migrations WHERE app='pf' ORDER BY id DESC LIMIT 5")
        migrations = cursor.fetchall()
        
        print("   Dernières migrations:")
        for mig in migrations:
            print(f"   - {mig[0]}")
            
        # Vérifier la migration spécifique
        cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app='pf' AND name='0999_add_factures_fournisseurs'")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("\n   ✅ Migration 0999_add_factures_fournisseurs appliquée")
        else:
            print("\n   ❌ Migration 0999_add_factures_fournisseurs NON appliquée")
            
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 5. Tester le modèle EmployePharmacie
print("\n5. Test du modèle EmployePharmacie")
try:
    # Essayer d'accéder aux nouveaux champs
    fields = [f.name for f in EmployePharmacie._meta.get_fields()]
    
    if 'peut_annuler_vente' in fields:
        print("   ✅ Champ peut_annuler_vente dans le modèle")
    else:
        print("   ❌ Champ peut_annuler_vente ABSENT du modèle")
    
    if 'peut_enregistrer_facture' in fields:
        print("   ✅ Champ peut_enregistrer_facture dans le modèle")
    else:
        print("   ❌ Champ peut_enregistrer_facture ABSENT du modèle")
        
    # Essayer de faire une requête
    count = EmployePharmacie.objects.count()
    print(f"\n   ✅ Requête réussie: {count} employé(s) trouvé(s)")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    print("\n   Détails de l'erreur:")
    print(traceback.format_exc())

print("\n" + "=" * 50)
print("\n📋 RÉSUMÉ\n")

print("Si vous voyez des ❌, suivez ces étapes:\n")
print("1. Arrêtez le serveur (Ctrl+C)")
print("2. Exécutez: python3 manage.py migrate")
print("3. Redémarrez: python3 manage.py runserver")
print("\nOu utilisez le script: bash fix_error_500.sh\n")
