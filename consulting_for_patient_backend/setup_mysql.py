#!/usr/bin/env python
"""
Script de configuration MySQL pour le projet
Crée la base de données et configure l'environnement
"""

import mysql.connector
from mysql.connector import Error
import os
import sys

def create_database():
    """Crée la base de données MySQL"""
    try:
        # Configuration de connexion pour localhost:3306 (MySQL standard)
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root'  # Mot de passe MySQL
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Créer la base de données
            cursor.execute("CREATE DATABASE IF NOT EXISTS e_sora CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Base de données 'e_sora' créée avec succès")
            
            # Créer un utilisateur dédié (optionnel)
            try:
                cursor.execute("CREATE USER IF NOT EXISTS 'e_sora_user'@'localhost' IDENTIFIED BY 'e_sora_password'")
                cursor.execute("GRANT ALL PRIVILEGES ON e_sora.* TO 'e_sora_user'@'localhost'")
                cursor.execute("FLUSH PRIVILEGES")
                print("✅ Utilisateur 'e_sora_user' créé avec succès")
            except Error as e:
                print(f"⚠️  Utilisateur déjà existant ou erreur: {e}")
            
            cursor.close()
            
    except Error as e:
        print(f"❌ Erreur lors de la création de la base de données: {e}")
        return False
    
    finally:
        if connection.is_connected():
            connection.close()
    
    return True

def install_requirements():
    """Installe les dépendances Python"""
    print("📦 Installation des dépendances...")
    os.system("pip install -r requirements.txt")
    print("✅ Dépendances installées")

def run_migrations():
    """Lance les migrations Django"""
    print("🔄 Exécution des migrations...")
    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate")
    print("✅ Migrations terminées")

def main():
    """Fonction principale"""
    print("🚀 Configuration MySQL pour le projet Django")
    print("=" * 50)
    
    # Vérifier si MySQL est installé
    try:
        import mysql.connector
    except ImportError:
        print("❌ mysql-connector-python n'est pas installé")
        print("Installez-le avec: pip install mysql-connector-python")
        return
    
    # Créer la base de données
    if not create_database():
        print("❌ Échec de la création de la base de données")
        return
    
    # Installer les dépendances
    install_requirements()
    
    # Lancer les migrations
    run_migrations()
    
    print("\n✅ Configuration terminée!")
    print("\n📝 Prochaines étapes:")
    print("1. Vérifiez la configuration dans mysite/settings.py")
    print("2. Lancez le seeder: python seed_database.py")
    print("3. Démarrez le serveur: python manage.py runserver")
    
    print("\n🔧 Configuration de la base de données:")
    print("   Nom: e_sora")
    print("   Host: localhost")
    print("   Port: 3306")
    print("   User: root (ou e_sora_user)")

if __name__ == "__main__":
    main()