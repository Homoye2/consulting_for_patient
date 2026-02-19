#!/usr/bin/env python
"""
Script de seeding complet pour la base de données MySQL
Remplit toutes les tables avec des données réalistes
"""

import os
import sys
import django
from datetime import datetime, timedelta, date
from decimal import Decimal
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from faker import Faker

# Import des modèles
from pf.models import (
    User, Patient, RendezVous, ConsultationPF,
    LandingPageContent,
    Service, Value, ContactMessage, Pharmacie, Hopital, Specialite,
    Specialiste, DisponibiliteSpecialiste, Produit, StockProduit,
    CommandePharmacie, LigneCommande, Notification, RapportConsultation,
    AvisSpecialiste
)

# Configuration Faker pour le français/sénégalais
fake = Faker(['fr_FR'])

class DatabaseSeeder:
    def __init__(self):
        self.users = []
        self.patients = []
        self.hopitaux = []
        self.specialites = []
        self.specialistes = []
        self.pharmacies = []
        self.produits = []
        self.rendez_vous = []
        self.consultations = []
        
    def clear_database(self):
        """Vide toutes les tables"""
        print("🗑️  Suppression des données existantes...")
        
        # Ordre important pour respecter les contraintes de clés étrangères
        models_to_clear = [
            AvisSpecialiste, RapportConsultation, Notification,
            LigneCommande, CommandePharmacie, StockProduit,
            ConsultationPF, RendezVous, DisponibiliteSpecialiste, 
            Specialiste, ContactMessage, Value, Service,
            Patient, Pharmacie, Produit, Specialite, Hopital, 
            User, LandingPageContent
        ]
        
        for model in models_to_clear:
            model.objects.all().delete()
            print(f"   ✅ {model.__name__} vidé")

    def create_users(self):
        """Crée les utilisateurs de base"""
        print("👥 Création des utilisateurs...")
        
        # Super Admin
        super_admin = User.objects.create(
            nom="Super Administrateur",
            email="admin@system.sn",
            password=make_password("admin123"),
            role="super_admin",
            actif=True
        )
        self.users.append(super_admin)
        
        # Admins d'hôpitaux
        admin_hopital_names = [
            ("Dr. Amadou Ba", "admin.abassndao@hopital.sn"),
            ("Dr. Fatou Sall", "admin.hoggy@hopital.sn"),
            ("Dr. Ousmane Diop", "admin.dalal@hopital.sn"),
        ]
        
        for nom, email in admin_hopital_names:
            admin = User.objects.create(
                nom=nom,
                email=email,
                password=make_password("admin123"),
                role="admin_hopital",
                actif=True
            )
            self.users.append(admin)
        
        # Spécialistes
        specialiste_names = [
            "Dr. Aissatou Diallo", "Dr. Mamadou Ndiaye", "Dr. Khadija Fall",
            "Dr. Ibrahima Sarr", "Dr. Mariama Cissé", "Dr. Cheikh Sy",
            "Dr. Aminata Touré", "Dr. Moussa Kane", "Dr. Binta Sow",
            "Dr. Alioune Badara", "Dr. Ndeye Fatou", "Dr. Babacar Dieng"
        ]
        
        for nom in specialiste_names:
            email = nom.lower().replace("dr. ", "").replace(" ", ".") + "@hopital.sn"
            specialiste = User.objects.create(
                nom=nom,
                email=email,
                password=make_password("doc123"),
                role="specialiste",
                actif=True
            )
            self.users.append(specialiste)
        
        # Pharmaciens
        pharmacien_names = [
            "Pharmacien Abdou Diouf", "Pharmacienne Rama Seck",
            "Pharmacien Modou Faye", "Pharmacienne Awa Diop",
            "Pharmacien Saliou Ba"
        ]
        
        for nom in pharmacien_names:
            email = nom.lower().replace("pharmacien", "").replace("ne ", "").strip().replace(" ", ".") + "@pharma.sn"
            pharmacien = User.objects.create(
                nom=nom,
                email=email,
                password=make_password("pharma123"),
                role="pharmacien",
                actif=True
            )
            self.users.append(pharmacien)
        
        # Agents d'enregistrement
        for i in range(5):
            agent = User.objects.create(
                nom=f"Agent {fake.last_name()}",
                email=f"agent{i+1}@hopital.sn",
                password=make_password("agent123"),
                role="agent_enregistrement",
                actif=True
            )
            self.users.append(agent)
        
        # Patients
        for i in range(50):
            patient_user = User.objects.create(
                nom=fake.last_name(),
                email=fake.email(),
                password=make_password("patient123"),
                role="patient",
                actif=True
            )
            self.users.append(patient_user)
        
        print(f"   ✅ {len(self.users)} utilisateurs créés")

    def create_hopitaux(self):
        """Crée les hôpitaux"""
        print("🏥 Création des hôpitaux...")
        
        hopitaux_data = [
            {
                "nom": "Hôpital Abass Ndao",
                "code_hopital": "HAN001",
                "adresse": "Route de l'aéroport, Dakar",
                "ville": "Dakar",
                "telephone": "+221338234567",
                "email": "contact@abassndao.sn",
                "latitude": Decimal("14.6937"),
                "longitude": Decimal("-17.4441"),
                "admin_hopital": [u for u in self.users if u.role == "admin_hopital"][0]
            },
            {
                "nom": "Hôpital Aristide Le Dantec",
                "code_hopital": "HALD002",
                "adresse": "Avenue Pasteur, Dakar",
                "ville": "Dakar", 
                "telephone": "+221338891234",
                "email": "contact@ledantec.sn",
                "latitude": Decimal("14.6928"),
                "longitude": Decimal("-17.4467"),
                "admin_hopital": [u for u in self.users if u.role == "admin_hopital"][1]
            },
            {
                "nom": "Hôpital Dalal Jamm",
                "code_hopital": "HDJ003",
                "adresse": "Guédiawaye, Dakar",
                "ville": "Guédiawaye",
                "telephone": "+221338567890",
                "email": "contact@dalaljamm.sn",
                "latitude": Decimal("14.7667"),
                "longitude": Decimal("-17.4167"),
                "admin_hopital": [u for u in self.users if u.role == "admin_hopital"][2]
            }
        ]
        
        for data in hopitaux_data:
            hopital = Hopital.objects.create(**data)
            self.hopitaux.append(hopital)
        
        print(f"   ✅ {len(self.hopitaux)} hôpitaux créés")

    def create_specialites(self):
        """Crée les spécialités médicales"""
        print("🩺 Création des spécialités...")
        
        specialites_data = [
            {"nom": "Gynécologie-Obstétrique", "code": "GYNO", "description": "Santé reproductive féminine", "icone": "Heart"},
            {"nom": "Médecine Générale", "code": "MGEN", "description": "Médecine générale et familiale", "icone": "Stethoscope"},
            {"nom": "Pédiatrie", "code": "PEDI", "description": "Médecine des enfants", "icone": "Baby"},
            {"nom": "Cardiologie", "code": "CARD", "description": "Maladies cardiovasculaires", "icone": "Heart"},
            {"nom": "Dermatologie", "code": "DERM", "description": "Maladies de la peau", "icone": "Scan"},
            {"nom": "Ophtalmologie", "code": "OPHT", "description": "Maladies des yeux", "icone": "Eye"},
            {"nom": "Endocrinologie", "code": "ENDO", "description": "Troubles hormonaux", "icone": "Activity"},
            {"nom": "Psychiatrie", "code": "PSYC", "description": "Santé mentale", "icone": "Brain"},
        ]
        
        for data in specialites_data:
            specialite = Specialite.objects.create(**data)
            self.specialites.append(specialite)
        
        print(f"   ✅ {len(self.specialites)} spécialités créées")

    def create_specialistes(self):
        """Crée les spécialistes"""
        print("👨‍⚕️ Création des spécialistes...")
        
        specialiste_users = [u for u in self.users if u.role == "specialiste"]
        
        for i, user in enumerate(specialiste_users):
            hopital = random.choice(self.hopitaux)
            specialite = random.choice(self.specialites)
            
            specialiste = Specialiste.objects.create(
                user=user,
                hopital=hopital,
                specialite=specialite,
                numero_ordre=f"ORD{1000 + i}",
                titre="Docteur en Médecine",
                annees_experience=random.randint(2, 25),
                bio=f"Spécialiste en {specialite.nom} avec {random.randint(2, 25)} années d'expérience.",
                tarif_consultation=Decimal(random.choice([15000, 20000, 25000, 30000])),
                duree_consultation=random.choice([30, 45, 60]),
                accepte_nouveaux_patients=random.choice([True, True, False]),
                consultation_en_ligne=random.choice([True, False]),
                actif=True
            )
            self.specialistes.append(specialiste)
        
        print(f"   ✅ {len(self.specialistes)} spécialistes créés")

    def create_disponibilites(self):
        """Crée les disponibilités des spécialistes"""
        print("📅 Création des disponibilités...")
        
        jours_semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]
        
        for specialiste in self.specialistes:
            # Chaque spécialiste travaille 4-6 jours par semaine
            jours_travail = random.sample(jours_semaine, random.randint(4, 6))
            
            for jour in jours_travail:
                # Créneaux du matin
                if random.choice([True, True, False]):  # 66% de chance
                    DisponibiliteSpecialiste.objects.create(
                        specialiste=specialiste,
                        jour_semaine=jour,
                        heure_debut="08:00",
                        heure_fin="12:00",
                        actif=True
                    )
                
                # Créneaux de l'après-midi
                if random.choice([True, False]):  # 50% de chance
                    DisponibiliteSpecialiste.objects.create(
                        specialiste=specialiste,
                        jour_semaine=jour,
                        heure_debut="14:00",
                        heure_fin="18:00",
                        actif=True
                    )
        
        print("   ✅ Disponibilités créées")

    def create_patients(self):
        """Crée les profils patients"""
        print("🤱 Création des patients...")
        
        patient_users = [u for u in self.users if u.role == "patient"]
        
        for user in patient_users:
            patient = Patient.objects.create(
                nom=user.nom,
                prenom=fake.first_name_female() if random.choice([True, False]) else fake.first_name_male(),
                dob=fake.date_of_birth(minimum_age=16, maximum_age=50),
                sexe=random.choice(["F", "M"]),
                telephone=f"+221{random.randint(700000000, 799999999)}",
                email=user.email,
                adresse=fake.address(),
                ville_actuelle=random.choice(["Dakar", "Thiès", "Saint-Louis", "Kaolack", "Ziguinchor"]),
                antecedents=random.choice([
                    "Aucun antécédent particulier",
                    "Hypertension artérielle",
                    "Diabète type 2",
                    "Asthme",
                    ""
                ]),
                allergies=random.choice([
                    "Aucune allergie connue",
                    "Pénicilline",
                    "Aspirine",
                    "Fruits de mer",
                    ""
                ]),
                user=user
            )
            self.patients.append(patient)
        
        print(f"   ✅ {len(self.patients)} patients créés")

    def create_pharmacies(self):
        """Crée les pharmacies"""
        print("🏪 Création des pharmacies...")
        
        pharmacien_users = [u for u in self.users if u.role == "pharmacien"]
        
        pharmacies_data = [
            {"nom": "Pharmacie Centrale", "ville": "Dakar"},
            {"nom": "Pharmacie du Plateau", "ville": "Dakar"},
            {"nom": "Pharmacie Médina", "ville": "Dakar"},
            {"nom": "Pharmacie Thiès Centre", "ville": "Thiès"},
            {"nom": "Pharmacie Saint-Louis", "ville": "Saint-Louis"},
        ]
        
        for i, data in enumerate(pharmacies_data):
            if i < len(pharmacien_users):
                pharmacie = Pharmacie.objects.create(
                    nom=data["nom"],
                    adresse=fake.address(),
                    ville=data["ville"],
                    telephone=f"+221{random.randint(800000000, 899999999)}",
                    email=f"contact@{data['nom'].lower().replace(' ', '')}.sn",
                    user=pharmacien_users[i],
                    actif=True
                )
                self.pharmacies.append(pharmacie)
        
        print(f"   ✅ {len(self.pharmacies)} pharmacies créées")

    def create_produits(self):
        """Crée les produits pharmaceutiques"""
        print("💉 Création des produits...")
        
        produits_data = [
            {"nom": "Paracétamol 500mg", "categorie": "medicament", "prix": "500"},
            {"nom": "Ibuprofène 400mg", "categorie": "medicament", "prix": "750"},
            {"nom": "Amoxicilline 500mg", "categorie": "medicament", "prix": "1200"},
            {"nom": "Pilule Jasmine", "categorie": "contraceptif", "prix": "2500"},
            {"nom": "Préservatifs Durex", "categorie": "contraceptif", "prix": "1500"},
            {"nom": "Test de grossesse", "categorie": "materiel_medical", "prix": "2000"},
            {"nom": "Vitamine D3", "categorie": "supplement", "prix": "3000"},
            {"nom": "Fer + Acide folique", "categorie": "supplement", "prix": "2200"},
            {"nom": "Savon antiseptique", "categorie": "hygiene", "prix": "800"},
            {"nom": "Solution hydroalcoolique", "categorie": "hygiene", "prix": "1200"},
        ]
        
        for data in produits_data:
            produit = Produit.objects.create(
                nom=data["nom"],
                categorie=data["categorie"],
                description=f"Description du produit {data['nom']}",
                fabricant=fake.company(),
                prix_unitaire=Decimal(data["prix"]),
                prescription_requise=random.choice([True, False]),
                actif=True
            )
            self.produits.append(produit)
        
        print(f"   ✅ {len(self.produits)} produits créés")

    def create_stocks(self):
        """Crée les stocks"""
        print("📦 Création des stocks...")
        
        # Stocks produits
        for produit in self.produits:
            for pharmacie in random.sample(self.pharmacies, random.randint(2, len(self.pharmacies))):
                StockProduit.objects.create(
                    pharmacie=pharmacie,
                    produit=produit,
                    quantite=random.randint(0, 150),
                    seuil_alerte=random.randint(5, 25),
                    numero_lot=f"LOT{random.randint(100000, 999999)}",
                    date_expiration=fake.date_between(start_date='+30d', end_date='+2y'),
                    prix_vente=produit.prix_unitaire * Decimal(random.uniform(1.1, 1.5))
                )
        
        print("   ✅ Stocks créés")

    def create_rendez_vous(self):
        """Crée les rendez-vous"""
        print("📅 Création des rendez-vous...")
        
        statuts = ["en_attente", "confirme", "termine", "annule"]
        
        for _ in range(100):
            patient = random.choice(self.patients)
            specialiste = random.choice(self.specialistes)
            
            # Date dans les 3 derniers mois ou 2 prochains mois
            if random.choice([True, False]):
                # Passé
                date_rdv = fake.date_time_between(start_date='-3M', end_date='now', tzinfo=timezone.get_current_timezone())
                statut = random.choice(["termine", "annule"])
            else:
                # Futur
                date_rdv = fake.date_time_between(start_date='now', end_date='+2M', tzinfo=timezone.get_current_timezone())
                statut = random.choice(["en_attente", "confirme"])
            
            rdv = RendezVous.objects.create(
                patient=patient,
                specialiste=specialiste,
                hopital=specialiste.hopital,
                datetime=date_rdv,
                statut=statut,
                motif=random.choice([
                    "Consultation de routine",
                    "Suivi contraceptif",
                    "Consultation prénatale",
                    "Problème gynécologique",
                    "Consultation post-partum"
                ]),
                confirme_par_specialiste=(statut in ["confirme", "termine"]),
                notes=fake.text(max_nb_chars=200) if random.choice([True, False]) else ""
            )
            self.rendez_vous.append(rdv)
        
        print(f"   ✅ {len(self.rendez_vous)} rendez-vous créés")

    def create_consultations(self):
        """Crée les consultations"""
        print("🩺 Création des consultations...")
        
        # Créer des consultations pour les RDV terminés
        rdv_termines = [rdv for rdv in self.rendez_vous if rdv.statut == "termine"]
        
        for rdv in rdv_termines[:50]:  # Limiter le nombre
            consultation = ConsultationPF.objects.create(
                patient=rdv.patient,
                specialiste=rdv.specialiste,
                hopital=rdv.hopital,
                rendez_vous=rdv,
                date=rdv.datetime,
                anamnese=fake.text(max_nb_chars=300),
                examen=fake.text(max_nb_chars=200),
                methode_posee=random.choice([True, False]),
                effets_secondaires=random.choice(["Aucun", "Légers maux de tête", "Nausées", ""]),
                notes=fake.text(max_nb_chars=150),
                observation=fake.text(max_nb_chars=100)
            )
            self.consultations.append(consultation)
        
        print(f"   ✅ {len(self.consultations)} consultations créées")

    def create_commandes(self):
        """Crée les commandes de pharmacie"""
        print("🛒 Création des commandes...")
        
        statuts = ["en_attente", "confirmee", "preparee", "prete", "recuperee"]
        
        for _ in range(30):
            patient = random.choice(self.patients)
            pharmacie = random.choice(self.pharmacies)
            
            commande = CommandePharmacie.objects.create(
                patient=patient,
                pharmacie=pharmacie,
                statut=random.choice(statuts),
                notes_patient=fake.text(max_nb_chars=100) if random.choice([True, False]) else ""
            )
            
            # Ajouter des lignes de commande
            nb_produits = random.randint(1, 4)
            produits_commande = random.sample(self.produits, nb_produits)
            
            for produit in produits_commande:
                quantite = random.randint(1, 3)
                LigneCommande.objects.create(
                    commande=commande,
                    produit=produit,
                    quantite=quantite,
                    prix_unitaire=produit.prix_unitaire
                )
            
            # Calculer le montant total
            lignes = commande.lignes.all()
            montant_total = sum(ligne.prix_total for ligne in lignes)
            commande.montant_total = montant_total
            commande.save()
        
        print("   ✅ Commandes créées")

    def create_notifications(self):
        """Crée les notifications"""
        print("🔔 Création des notifications...")
        
        types_notif = [
            "rendez_vous_nouveau", "rendez_vous_confirme", "rendez_vous_rappel",
            "commande_confirmee", "commande_prete", "consultation_rapport"
        ]
        
        for _ in range(50):
            user = random.choice([u for u in self.users if u.role in ["patient", "specialiste"]])
            
            Notification.objects.create(
                user=user,
                type_notification=random.choice(types_notif),
                titre=fake.sentence(nb_words=4),
                message=fake.text(max_nb_chars=200),
                lu=random.choice([True, False])
            )
        
        print("   ✅ Notifications créées")

    def create_landing_page_content(self):
        """Crée le contenu de la landing page"""
        print("🌐 Création du contenu de la landing page...")
        
        content = LandingPageContent.objects.create(
            logo_text="Hôpital Abass Ndao",
            hero_title="Votre Santé, Notre Priorité",
            hero_description="Centre d'excellence en santé reproductive et planification familiale au Sénégal.",
            hero_button_primary="Prendre Rendez-vous",
            hero_button_secondary="En savoir plus",
            about_title="À propos de l'Hôpital Abass Ndao",
            about_description_1="L'Hôpital Abass Ndao est un établissement de référence en matière de santé reproductive et de planification familiale au Sénégal.",
            about_description_2="Nous offrons des soins de qualité avec une équipe de professionnels expérimentés et des équipements modernes.",
            about_stat_1_value="15+",
            about_stat_1_label="Années d'expérience",
            about_stat_2_value="50+",
            about_stat_2_label="Professionnels de santé",
            services_title="Nos Services",
            services_subtitle="Une gamme complète de services de santé reproductive",
            values_title="Nos Valeurs",
            values_subtitle="Ce qui nous guide dans notre mission",
            footer_about_text="Votre partenaire de confiance pour la santé reproductive et le bien-être.",
            footer_address="Route de l'aéroport, Dakar, Sénégal",
            footer_phone="+221 33 823 45 67",
            footer_email="contact@abassndao.sn"
        )
        
        # Services
        services_data = [
            {"titre": "Consultation Gynécologique", "description": "Consultations spécialisées en gynécologie", "icone": "Heart"},
            {"titre": "Planification Familiale", "description": "Conseils et méthodes contraceptives", "icone": "Users"},
            {"titre": "Suivi de Grossesse", "description": "Accompagnement pendant la grossesse", "icone": "Baby"},
            {"titre": "Urgences", "description": "Prise en charge des urgences 24h/24", "icone": "AlertCircle"},
        ]
        
        for i, data in enumerate(services_data):
            Service.objects.create(
                landing_page=content,
                titre=data["titre"],
                description=data["description"],
                icone=data["icone"],
                ordre=i
            )
        
        # Valeurs
        values_data = [
            {"titre": "Excellence", "description": "Nous visons l'excellence dans tous nos services", "icone": "Award"},
            {"titre": "Compassion", "description": "Nous traitons chaque patient avec empathie", "icone": "Heart"},
            {"titre": "Innovation", "description": "Nous adoptons les dernières technologies", "icone": "Lightbulb"},
            {"titre": "Intégrité", "description": "Nous agissons avec transparence et honnêteté", "icone": "Shield"},
        ]
        
        for i, data in enumerate(values_data):
            Value.objects.create(
                landing_page=content,
                titre=data["titre"],
                description=data["description"],
                icone=data["icone"],
                ordre=i
            )
        
        print("   ✅ Contenu de la landing page créé")

    def create_contact_messages(self):
        """Crée des messages de contact"""
        print("💬 Création des messages de contact...")
        
        for _ in range(20):
            ContactMessage.objects.create(
                nom=fake.name(),
                email=fake.email(),
                sujet=fake.sentence(nb_words=6),
                message=fake.text(max_nb_chars=500),
                patient=random.choice(self.patients) if random.choice([True, False]) else None,
                lu=random.choice([True, False])
            )
        
        print("   ✅ Messages de contact créés")

    def create_mouvements_stock(self):
        """Crée des mouvements de stock - Fonction supprimée car les modèles associés ont été supprimés"""
        print("📊 Mouvements de stock - Fonctionnalité supprimée")
        pass

    def run_seed(self):
        """Lance le processus complet de seeding"""
        print("🌱 Début du seeding de la base de données MySQL e_sora...")
        print("=" * 60)
        
        try:
            self.clear_database()
            self.create_users()
            self.create_hopitaux()
            self.create_specialites()
            self.create_specialistes()
            self.create_disponibilites()
            self.create_patients()
            self.create_pharmacies()
            self.create_produits()
            self.create_stocks()
            self.create_rendez_vous()
            self.create_consultations()
            self.create_commandes()
            self.create_notifications()
            self.create_landing_page_content()
            self.create_contact_messages()
            self.create_mouvements_stock()
            
            print("=" * 60)
            print("✅ Seeding terminé avec succès!")
            print("\n📊 Résumé des données créées:")
            print(f"   👥 Utilisateurs: {User.objects.count()}")
            print(f"   🤱 Patients: {Patient.objects.count()}")
            print(f"   🏥 Hôpitaux: {Hopital.objects.count()}")
            print(f"   👨‍⚕️ Spécialistes: {Specialiste.objects.count()}")
            print(f"   🏪 Pharmacies: {Pharmacie.objects.count()}")
            print(f"   💊 Produits: {Produit.objects.count()}")
            print(f"   📅 Rendez-vous: {RendezVous.objects.count()}")
            print(f"   🩺 Consultations: {ConsultationPF.objects.count()}")
            print(f"   🛒 Commandes: {CommandePharmacie.objects.count()}")
            print(f"   🔔 Notifications: {Notification.objects.count()}")
            
            print("\n🔑 Comptes de test:")
            print("   Super Admin: admin@system.sn / admin123")
            print("   Admin Hôpital: admin.abassndao@hopital.sn / admin123")
            print("   Spécialiste: dr.aissatou.diallo@hopital.sn / doc123")
            print("   Pharmacien: abdou.diouf@pharma.sn / pharma123")
            print("   Patient: (voir les emails générés) / patient123")
            
        except Exception as e:
            print(f"❌ Erreur lors du seeding: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    seeder = DatabaseSeeder()
    seeder.run_seed()