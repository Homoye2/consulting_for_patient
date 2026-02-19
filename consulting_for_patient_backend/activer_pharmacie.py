#!/usr/bin/env python
"""
Script pour activer/désactiver une pharmacie et son utilisateur
"""
import os
import sys
import django

# Configuration Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from pf.models import Pharmacie, User

def lister_pharmacies():
    """Liste toutes les pharmacies avec leur statut"""
    print("\n📋 Liste des Pharmacies:")
    print("━" * 100)
    
    pharmacies = Pharmacie.objects.all().select_related('user')
    
    if not pharmacies.exists():
        print("Aucune pharmacie trouvée")
        return
    
    for pharmacie in pharmacies:
        pharma_status = "✅ Active" if pharmacie.actif else "❌ Inactive"
        user_status = "✅ Actif" if (pharmacie.user.actif and pharmacie.user.is_active) else "❌ Inactif"
        
        print(f"\n{pharma_status} | ID: {pharmacie.id:3d} | {pharmacie.nom}")
        print(f"         Email: {pharmacie.email}")
        print(f"         Ville: {pharmacie.ville}, {pharmacie.pays}")
        if pharmacie.user:
            print(f"         Utilisateur: {user_status} | {pharmacie.user.email} ({pharmacie.user.nom})")
        else:
            print(f"         Utilisateur: ⚠️  Aucun utilisateur associé")

def activer_pharmacie(pharmacie_id):
    """Active une pharmacie et son utilisateur"""
    try:
        pharmacie = Pharmacie.objects.get(id=pharmacie_id)
        
        print(f"\n📋 Pharmacie: {pharmacie.nom}")
        print(f"   ID: {pharmacie.id}")
        print(f"   Actif (avant): {pharmacie.actif}")
        
        if pharmacie.user:
            print(f"\n👤 Utilisateur: {pharmacie.user.email}")
            print(f"   Actif (avant): {pharmacie.user.actif}")
            print(f"   Is Active (avant): {pharmacie.user.is_active}")
        
        # Activer la pharmacie (le signal activera automatiquement l'utilisateur)
        pharmacie.actif = True
        pharmacie.save()
        
        # Recharger pour voir les changements
        pharmacie.refresh_from_db()
        
        print(f"\n✅ Pharmacie activée!")
        print(f"   Actif (après): {pharmacie.actif}")
        
        if pharmacie.user:
            pharmacie.user.refresh_from_db()
            print(f"\n✅ Utilisateur activé automatiquement!")
            print(f"   Actif (après): {pharmacie.user.actif}")
            print(f"   Is Active (après): {pharmacie.user.is_active}")
        
    except Pharmacie.DoesNotExist:
        print(f"\n❌ Pharmacie avec l'ID {pharmacie_id} non trouvée")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

def desactiver_pharmacie(pharmacie_id):
    """Désactive une pharmacie et son utilisateur"""
    try:
        pharmacie = Pharmacie.objects.get(id=pharmacie_id)
        
        print(f"\n📋 Pharmacie: {pharmacie.nom}")
        print(f"   ID: {pharmacie.id}")
        print(f"   Actif (avant): {pharmacie.actif}")
        
        if pharmacie.user:
            print(f"\n👤 Utilisateur: {pharmacie.user.email}")
            print(f"   Actif (avant): {pharmacie.user.actif}")
            print(f"   Is Active (avant): {pharmacie.user.is_active}")
        
        # Désactiver la pharmacie (le signal désactivera automatiquement l'utilisateur)
        pharmacie.actif = False
        pharmacie.save()
        
        # Recharger pour voir les changements
        pharmacie.refresh_from_db()
        
        print(f"\n❌ Pharmacie désactivée!")
        print(f"   Actif (après): {pharmacie.actif}")
        
        if pharmacie.user:
            pharmacie.user.refresh_from_db()
            print(f"\n❌ Utilisateur désactivé automatiquement!")
            print(f"   Actif (après): {pharmacie.user.actif}")
            print(f"   Is Active (après): {pharmacie.user.is_active}")
        
    except Pharmacie.DoesNotExist:
        print(f"\n❌ Pharmacie avec l'ID {pharmacie_id} non trouvée")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

def info_pharmacie(pharmacie_id):
    """Affiche les informations détaillées d'une pharmacie"""
    try:
        pharmacie = Pharmacie.objects.get(id=pharmacie_id)
        
        print(f"\n📋 Informations de la Pharmacie")
        print("━" * 80)
        print(f"ID: {pharmacie.id}")
        print(f"Nom: {pharmacie.nom}")
        print(f"Email: {pharmacie.email}")
        print(f"Téléphone: {pharmacie.telephone}")
        print(f"Adresse: {pharmacie.adresse}")
        print(f"Ville: {pharmacie.ville}")
        print(f"Pays: {pharmacie.pays}")
        print(f"Actif: {'✅ Oui' if pharmacie.actif else '❌ Non'}")
        
        if pharmacie.user:
            print(f"\n👤 Utilisateur Associé")
            print("━" * 80)
            print(f"ID: {pharmacie.user.id}")
            print(f"Email: {pharmacie.user.email}")
            print(f"Nom: {pharmacie.user.nom}")
            print(f"Rôle: {pharmacie.user.role}")
            print(f"Actif: {'✅ Oui' if pharmacie.user.actif else '❌ Non'}")
            print(f"Is Active: {'✅ Oui' if pharmacie.user.is_active else '❌ Non'}")
        else:
            print(f"\n⚠️  Aucun utilisateur associé")
        
    except Pharmacie.DoesNotExist:
        print(f"\n❌ Pharmacie avec l'ID {pharmacie_id} non trouvée")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gérer les pharmacies')
    parser.add_argument('--list', action='store_true', help='Lister toutes les pharmacies')
    parser.add_argument('--activer', type=int, metavar='ID', help='Activer une pharmacie')
    parser.add_argument('--desactiver', type=int, metavar='ID', help='Désactiver une pharmacie')
    parser.add_argument('--info', type=int, metavar='ID', help='Afficher les infos d\'une pharmacie')
    
    args = parser.parse_args()
    
    if args.list:
        lister_pharmacies()
    elif args.activer:
        activer_pharmacie(args.activer)
    elif args.desactiver:
        desactiver_pharmacie(args.desactiver)
    elif args.info:
        info_pharmacie(args.info)
    else:
        print("Usage:")
        print("  python activer_pharmacie.py --list                    # Lister les pharmacies")
        print("  python activer_pharmacie.py --info ID                 # Infos d'une pharmacie")
        print("  python activer_pharmacie.py --activer ID              # Activer une pharmacie")
        print("  python activer_pharmacie.py --desactiver ID           # Désactiver une pharmacie")
        print("\nExemple:")
        print("  python activer_pharmacie.py --activer 11")
