#!/usr/bin/env python
"""
Script pour lister tous les utilisateurs de la base de données
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from pf.models import User
from django.utils import timezone

def list_all_users():
    """Liste tous les utilisateurs avec leurs informations"""
    users = User.objects.all().order_by('id')
    
    print("=" * 80)
    print("LISTE DES UTILISATEURS - APPLICATION DE PLANIFICATION FAMILIALE")
    print("=" * 80)
    print()
    
    if not users.exists():
        print("Aucun utilisateur trouvé dans la base de données.")
        return
    
    print(f"Total d'utilisateurs: {users.count()}\n")
    print("-" * 80)
    
    for user in users:
        print(f"ID: {user.id}")
        print(f"Nom: {user.nom}")
        print(f"Email: {user.email}")
        print(f"Rôle: {user.get_role_display()} ({user.role})")
        print(f"Statut: {'✅ Actif' if user.actif else '❌ Inactif'}")
        print(f"Staff: {'Oui' if user.is_staff else 'Non'}")
        print(f"Superuser: {'Oui' if user.is_superuser else 'Non'}")
        print(f"Date d'inscription: {user.date_joined.strftime('%d/%m/%Y %H:%M:%S')}")
        if user.last_login:
            print(f"Dernière connexion: {user.last_login.strftime('%d/%m/%Y %H:%M:%S')}")
        else:
            print("Dernière connexion: Jamais")
        print("-" * 80)
        print()
    
    # Générer le contenu pour le fichier markdown
    markdown_content = "# Identifiants des Utilisateurs - Application de Planification Familiale\n\n"
    markdown_content += "> **⚠️ ATTENTION : Ce fichier contient des informations sensibles. Ne le partagez pas publiquement.**\n\n"
    markdown_content += f"**Date de génération :** {django.utils.timezone.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
    markdown_content += f"**Total d'utilisateurs :** {users.count()}\n\n"
    markdown_content += "---\n\n"
    
    for user in users:
        markdown_content += f"## Utilisateur #{user.id}\n\n"
        markdown_content += f"- **Nom :** {user.nom}\n"
        markdown_content += f"- **Email :** `{user.email}`\n"
        markdown_content += f"- **Rôle :** {user.get_role_display()} (`{user.role}`)\n"
        markdown_content += f"- **Statut :** {'✅ Actif' if user.actif else '❌ Inactif'}\n"
        markdown_content += f"- **Staff :** {'Oui' if user.is_staff else 'Non'}\n"
        markdown_content += f"- **Superuser :** {'Oui' if user.is_superuser else 'Non'}\n"
        markdown_content += f"- **Date d'inscription :** {user.date_joined.strftime('%d/%m/%Y %H:%M:%S')}\n"
        if user.last_login:
            markdown_content += f"- **Dernière connexion :** {user.last_login.strftime('%d/%m/%Y %H:%M:%S')}\n"
        else:
            markdown_content += "- **Dernière connexion :** Jamais\n"
        markdown_content += "\n---\n\n"
    
    markdown_content += "## Notes importantes\n\n"
    markdown_content += "1. **Les mots de passe ne sont pas stockés en clair** dans la base de données.\n"
    markdown_content += "2. Si vous avez oublié votre mot de passe, contactez un administrateur.\n"
    markdown_content += "3. Pour créer un nouvel utilisateur, utilisez l'interface d'administration Django ou l'API.\n"
    markdown_content += "4. Pour réinitialiser un mot de passe, utilisez la commande Django :\n"
    markdown_content += "   ```bash\n"
    markdown_content += "   python manage.py changepassword <email>\n"
    markdown_content += "   ```\n\n"
    markdown_content += "## Rôles disponibles\n\n"
    markdown_content += "- **administrateur** : Accès complet à toutes les fonctionnalités\n"
    markdown_content += "- **medecin** : Gestion des patients, consultations, rendez-vous\n"
    markdown_content += "- **sage_femme** : Gestion des patients, consultations, rendez-vous\n"
    markdown_content += "- **infirmier** : Gestion des patients, consultations, rendez-vous\n"
    markdown_content += "- **pharmacien** : Gestion des stocks\n"
    markdown_content += "- **agent_enregistrement** : Gestion des rendez-vous\n\n"
    
    # Sauvegarder dans un fichier
    output_file = 'UTILISATEURS.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n✅ Fichier '{output_file}' créé avec succès !")
    print(f"📄 Le fichier contient {users.count()} utilisateur(s).\n")

if __name__ == '__main__':
    list_all_users()

