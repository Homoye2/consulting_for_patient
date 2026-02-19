#!/usr/bin/env python
"""
Script de gestion de la base de données
Commandes utiles pour la maintenance
"""

import os
import sys
import django
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.management import execute_from_command_line
from pf.models import *

def show_stats():
    """Affiche les statistiques de la base de données"""
    print("📊 Statistiques de la base de données")
    print("=" * 40)
    
    stats = {
        "👥 Utilisateurs": User.objects.count(),
        "🤱 Patients": Patient.objects.count(),
        "🏥 Hôpitaux": Hopital.objects.count(),
        "🩺 Spécialités": Specialite.objects.count(),
        "👨‍⚕️ Spécialistes": Specialiste.objects.count(),
        "🏪 Pharmacies": Pharmacie.objects.count(),
        "💊 Méthodes contraceptives": MethodeContraceptive.objects.count(),
        "🧴 Produits": Produit.objects.count(),
        "📅 Rendez-vous": RendezVous.objects.count(),
        "🩺 Consultations": ConsultationPF.objects.count(),
        "💊 Prescriptions": Prescription.objects.count(),
        "🛒 Commandes": CommandePharmacie.objects.count(),
        "📦 Stocks (anciens)": StockItem.objects.count(),
        "📦 Stocks produits": StockProduit.objects.count(),
        "🔔 Notifications": Notification.objects.count(),
        "💬 Messages contact": ContactMessage.objects.count(),
    }
    
    for label, count in stats.items():
        print(f"{label}: {count}")

def show_test_accounts():
    """Affiche les comptes de test"""
    print("\n🔑 Comptes de test disponibles")
    print("=" * 40)
    
    accounts = [
        ("Super Admin", "admin@system.sn", "admin123"),
        ("Admin Hôpital", "admin.abassndao@hopital.sn", "admin123"),
        ("Spécialiste", "dr.aissatou.diallo@hopital.sn", "doc123"),
        ("Pharmacien", "abdou.diouf@pharma.sn", "pharma123"),
    ]
    
    for role, email, password in accounts:
        print(f"{role}: {email} / {password}")
    
    print("\nPatients: Utilisez les emails générés / patient123")

def reset_database():
    """Remet à zéro la base de données"""
    print("⚠️  ATTENTION: Cette action va supprimer toutes les données!")
    confirm = input("Tapez 'CONFIRMER' pour continuer: ")
    
    if confirm == "CONFIRMER":
        print("🗑️  Suppression des données...")
        
        # Ordre important pour les contraintes
        models = [
            AvisSpecialiste, RapportConsultation, Notification,
            LigneCommande, CommandePharmacie, StockProduit,
            MouvementStock, Prescription, ConsultationPF,
            RendezVous, DisponibiliteSpecialiste, Specialiste,
            StockItem, ContactMessage, Value, Service,
            Patient, Pharmacie, Produit, MethodeContraceptive,
            Specialite, Hopital, User, LandingPageContent
        ]
        
        for model in models:
            count = model.objects.count()
            model.objects.all().delete()
            print(f"   ✅ {model.__name__}: {count} supprimés")
        
        print("✅ Base de données vidée")
    else:
        print("❌ Opération annulée")

def backup_database():
    """Crée une sauvegarde de la base de données"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.sql"
    
    print(f"💾 Création de la sauvegarde: {filename}")
    
    # Commande mysqldump pour port 8888
    os.system(f"mysqldump -P 8888 -u root -p e_sora > {filename}")
    
    print(f"✅ Sauvegarde créée: {filename}")

def restore_database():
    """Restaure une sauvegarde"""
    print("📁 Fichiers de sauvegarde disponibles:")
    
    backups = [f for f in os.listdir('.') if f.startswith('backup_') and f.endswith('.sql')]
    
    if not backups:
        print("❌ Aucune sauvegarde trouvée")
        return
    
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")
    
    try:
        choice = int(input("Choisissez un fichier (numéro): ")) - 1
        if 0 <= choice < len(backups):
            filename = backups[choice]
            print(f"📥 Restauration de {filename}...")
            
            # Commande mysql pour port 8888
            os.system(f"mysql -P 8888 -u root -p e_sora < {filename}")
            
            print("✅ Restauration terminée")
        else:
            print("❌ Choix invalide")
    except ValueError:
        print("❌ Veuillez entrer un numéro valide")

def check_health():
    """Vérifie la santé de la base de données"""
    print("🔍 Vérification de la santé de la base de données")
    print("=" * 50)
    
    checks = []
    
    # Vérifier les utilisateurs sans profil
    users_without_profile = User.objects.filter(role='patient', patient_profile__isnull=True).count()
    checks.append(("Utilisateurs patients sans profil", users_without_profile, users_without_profile == 0))
    
    # Vérifier les spécialistes sans disponibilités
    specialistes_sans_dispo = Specialiste.objects.filter(disponibilites__isnull=True).count()
    checks.append(("Spécialistes sans disponibilités", specialistes_sans_dispo, specialistes_sans_dispo < 5))
    
    # Vérifier les stocks en rupture
    stocks_rupture = StockProduit.objects.filter(quantite=0).count()
    checks.append(("Stocks en rupture", stocks_rupture, stocks_rupture < 10))
    
    # Vérifier les RDV sans consultation
    rdv_sans_consultation = RendezVous.objects.filter(statut='termine', consultations__isnull=True).count()
    checks.append(("RDV terminés sans consultation", rdv_sans_consultation, rdv_sans_consultation < 10))
    
    # Afficher les résultats
    for check_name, value, is_ok in checks:
        status = "✅" if is_ok else "⚠️"
        print(f"{status} {check_name}: {value}")
    
    print("\n📈 Statistiques rapides:")
    print(f"   Utilisateurs actifs: {User.objects.filter(actif=True).count()}")
    print(f"   RDV ce mois: {RendezVous.objects.filter(datetime__month=datetime.now().month).count()}")
    print(f"   Notifications non lues: {Notification.objects.filter(lu=False).count()}")

def main():
    """Menu principal"""
    while True:
        print("\n🛠️  Gestionnaire de Base de Données")
        print("=" * 40)
        print("1. Afficher les statistiques")
        print("2. Afficher les comptes de test")
        print("3. Vérifier la santé de la DB")
        print("4. Créer une sauvegarde")
        print("5. Restaurer une sauvegarde")
        print("6. Lancer le seeder")
        print("7. Remettre à zéro la DB")
        print("8. Quitter")
        
        choice = input("\nChoisissez une option (1-8): ")
        
        if choice == "1":
            show_stats()
        elif choice == "2":
            show_test_accounts()
        elif choice == "3":
            check_health()
        elif choice == "4":
            backup_database()
        elif choice == "5":
            restore_database()
        elif choice == "6":
            print("🌱 Lancement du seeder...")
            os.system("python seed_database.py")
        elif choice == "7":
            reset_database()
        elif choice == "8":
            print("👋 Au revoir!")
            break
        else:
            print("❌ Option invalide")

if __name__ == "__main__":
    main()