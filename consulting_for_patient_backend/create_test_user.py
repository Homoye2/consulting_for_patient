#!/usr/bin/env python
"""
Script pour créer un utilisateur de test pour l'application
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from pf.models import User

def create_test_users():
    """Crée des utilisateurs de test pour chaque rôle"""
    
    # Vérifier si des utilisateurs existent déjà
    if User.objects.exists():
        print("⚠️  Des utilisateurs existent déjà dans la base de données.")
        response = input("Voulez-vous créer des utilisateurs de test supplémentaires ? (o/n): ")
        if response.lower() != 'o':
            print("Annulé.")
            return
    
    users_to_create = [
        {
            'nom': 'Admin Principal',
            'email': 'admin@example.com',
            'password': 'admin123',
            'role': 'administrateur',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'nom': 'Dr. Marie Dupont',
            'email': 'medecin@example.com',
            'password': 'medecin123',
            'role': 'medecin',
        },
        {
            'nom': 'Sage-femme Sophie',
            'email': 'sagefemme@example.com',
            'password': 'sagefemme123',
            'role': 'sage_femme',
        },
        {
            'nom': 'Infirmier Jean',
            'email': 'infirmier@example.com',
            'password': 'infirmier123',
            'role': 'infirmier',
        },
        {
            'nom': 'Pharmacien Paul',
            'email': 'pharmacien@example.com',
            'password': 'pharmacien123',
            'role': 'pharmacien',
        },
        {
            'nom': 'Agent Sarah',
            'email': 'agent@example.com',
            'password': 'agent123',
            'role': 'agent_enregistrement',
        },
    ]
    
    created_users = []
    
    for user_data in users_to_create:
        email = user_data['email']
        if User.objects.filter(email=email).exists():
            print(f"⚠️  L'utilisateur {email} existe déjà. Ignoré.")
            continue
        
        password = user_data.pop('password')
        email = user_data.pop('email')
        user = User.objects.create_user(email=email, password=password, **user_data)
        created_users.append({
            'email': email,
            'password': password,
            'nom': user.nom,
            'role': user.role,
        })
        print(f"✅ Utilisateur créé : {user.nom} ({email}) - Rôle: {user.get_role_display()}")
    
    if created_users:
        print(f"\n🎉 {len(created_users)} utilisateur(s) créé(s) avec succès !\n")
        print("=" * 80)
        print("IDENTIFIANTS DE CONNEXION")
        print("=" * 80)
        for user in created_users:
            print(f"\nEmail: {user['email']}")
            print(f"Mot de passe: {user['password']}")
            print(f"Nom: {user['nom']}")
            print(f"Rôle: {user['role']}")
            print("-" * 80)
    else:
        print("\nAucun nouvel utilisateur créé.")

if __name__ == '__main__':
    create_test_users()

