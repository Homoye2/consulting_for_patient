#!/usr/bin/env python
"""
Script de test pour vérifier l'API des pharmacies
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from pf.models import Pharmacie, User

def test_pharmacies():
    """Teste l'état des pharmacies dans la base de données"""
    print("\n" + "="*60)
    print("🔍 TEST DE L'API PHARMACIES")
    print("="*60)
    
    # Compter toutes les pharmacies
    total_pharmacies = Pharmacie.objects.count()
    print(f"\n📊 Total de pharmacies dans la base: {total_pharmacies}")
    
    # Compter les pharmacies actives
    pharmacies_actives = Pharmacie.objects.filter(actif=True).count()
    print(f"✅ Pharmacies actives: {pharmacies_actives}")
    
    # Compter les pharmacies inactives
    pharmacies_inactives = Pharmacie.objects.filter(actif=False).count()
    print(f"❌ Pharmacies inactives: {pharmacies_inactives}")
    
    # Lister toutes les pharmacies avec détails
    print("\n" + "-"*60)
    print("📋 LISTE DÉTAILLÉE DES PHARMACIES:")
    print("-"*60)
    
    pharmacies = Pharmacie.objects.all().order_by('id')
    
    if not pharmacies.exists():
        print("⚠️  Aucune pharmacie trouvée dans la base de données!")
        print("\n💡 Solution: Exécutez le script seed_database.py pour créer des données de test")
        return
    
    for pharmacie in pharmacies:
        statut = "✅ ACTIVE" if pharmacie.actif else "❌ INACTIVE"
        user_info = f"Utilisateur: {pharmacie.user.email}" if pharmacie.user else "⚠️  Pas d'utilisateur"
        
        print(f"\n{statut}")
        print(f"  ID: {pharmacie.id}")
        print(f"  Nom: {pharmacie.nom}")
        print(f"  Adresse: {pharmacie.adresse}")
        print(f"  Ville: {pharmacie.ville}")
        print(f"  Téléphone: {pharmacie.telephone}")
        print(f"  Email: {pharmacie.email}")
        print(f"  {user_info}")
        
        if pharmacie.user:
            user_actif = "✅ Actif" if pharmacie.user.actif else "❌ Inactif"
            print(f"  Statut utilisateur: {user_actif}")
    
    # Recommandations
    print("\n" + "="*60)
    print("💡 RECOMMANDATIONS:")
    print("="*60)
    
    if pharmacies_actives == 0:
        print("\n⚠️  PROBLÈME DÉTECTÉ: Aucune pharmacie active!")
        print("\n🔧 Solutions possibles:")
        print("  1. Activer les pharmacies existantes:")
        print("     python activer_pharmacie.py")
        print("\n  2. Créer de nouvelles pharmacies:")
        print("     python seed_database.py")
    else:
        print(f"\n✅ {pharmacies_actives} pharmacie(s) active(s) - L'API devrait fonctionner")
        print("\n🔍 Si l'app mobile ne voit toujours pas les pharmacies:")
        print("  1. Vérifiez que le backend est démarré sur http://192.168.1.90:8000")
        print("  2. Testez l'endpoint: curl http://192.168.1.90:8000/api/pharmacies/")
        print("  3. Vérifiez la configuration dans e-sora-mobile/config/environment.ts")
        print("  4. Redémarrez l'app mobile")

if __name__ == '__main__':
    test_pharmacies()
