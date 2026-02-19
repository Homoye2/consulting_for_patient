#!/usr/bin/env python
"""
Script pour activer un utilisateur pharmacien
"""
import os
import sys
import django

# Configuration Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from pf.models import User, Pharmacie

def activer_pharmacien(email):
    """Active un utilisateur pharmacien"""
    try:
        user = User.objects.get(email=email)
        
        print(f"\n📋 Informations de l'utilisateur:")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Nom: {user.nom}")
        print(f"   Rôle: {user.role}")
        print(f"   Actif (actif): {user.actif}")
        print(f"   Actif (is_active): {user.is_active}")
        
        if user.actif and user.is_active:
            print(f"\n✅ L'utilisateur est déjà actif!")
            return
        
        # Activer l'utilisateur
        user.actif = True
        user.is_active = True
        user.save()
        
        print(f"\n✅ Utilisateur activé avec succès!")
        print(f"   Actif (actif): {user.actif}")
        print(f"   Actif (is_active): {user.is_active}")
        
        # Vérifier la pharmacie associée
        try:
            pharmacie = Pharmacie.objects.get(user=user)
            print(f"\n📋 Pharmacie associée:")
            print(f"   ID: {pharmacie.id}")
            print(f"   Nom: {pharmacie.nom}")
            print(f"   Actif: {pharmacie.actif}")
            
            if not pharmacie.actif:
                print(f"\n⚠️  La pharmacie est désactivée!")
                reponse = input("Voulez-vous activer la pharmacie aussi? (o/n): ")
                if reponse.lower() == 'o':
                    pharmacie.actif = True
                    pharmacie.save()
                    print(f"✅ Pharmacie activée!")
        except Pharmacie.DoesNotExist:
            print(f"\n⚠️  Aucune pharmacie associée à cet utilisateur")
        
    except User.DoesNotExist:
        print(f"\n❌ Utilisateur avec l'email '{email}' non trouvé")
        return
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        return

def lister_pharmaciens():
    """Liste tous les pharmaciens"""
    print("\n📋 Liste des pharmaciens:")
    print("━" * 80)
    
    pharmaciens = User.objects.filter(role='pharmacien')
    
    if not pharmaciens.exists():
        print("Aucun pharmacien trouvé")
        return
    
    for user in pharmaciens:
        status = "✅ Actif" if (user.actif and user.is_active) else "❌ Inactif"
        print(f"{status} | ID: {user.id:3d} | {user.email:40s} | {user.nom}")
        
        # Vérifier la pharmacie
        try:
            pharmacie = Pharmacie.objects.get(user=user)
            pharma_status = "✅" if pharmacie.actif else "❌"
            print(f"         Pharmacie: {pharma_status} {pharmacie.nom}")
        except Pharmacie.DoesNotExist:
            print(f"         Pharmacie: ⚠️  Aucune pharmacie associée")
        print()

def activer_tous_pharmaciens():
    """Active tous les pharmaciens"""
    pharmaciens = User.objects.filter(role='pharmacien')
    
    if not pharmaciens.exists():
        print("Aucun pharmacien trouvé")
        return
    
    print(f"\n🔄 Activation de {pharmaciens.count()} pharmacien(s)...")
    
    for user in pharmaciens:
        if not user.actif or not user.is_active:
            user.actif = True
            user.is_active = True
            user.save()
            print(f"✅ {user.email} activé")
        else:
            print(f"⏭️  {user.email} déjà actif")
    
    print(f"\n✅ Tous les pharmaciens sont maintenant actifs!")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gérer les utilisateurs pharmaciens')
    parser.add_argument('--email', help='Email du pharmacien à activer')
    parser.add_argument('--list', action='store_true', help='Lister tous les pharmaciens')
    parser.add_argument('--all', action='store_true', help='Activer tous les pharmaciens')
    
    args = parser.parse_args()
    
    if args.list:
        lister_pharmaciens()
    elif args.all:
        activer_tous_pharmaciens()
    elif args.email:
        activer_pharmacien(args.email)
    else:
        print("Usage:")
        print("  python activer_pharmacien.py --list                    # Lister les pharmaciens")
        print("  python activer_pharmacien.py --email EMAIL             # Activer un pharmacien")
        print("  python activer_pharmacien.py --all                     # Activer tous les pharmaciens")
        print("\nExemple:")
        print("  python activer_pharmacien.py --email abdou.diouf@pharma.sn")
