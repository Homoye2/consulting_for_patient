#!/usr/bin/env python
"""
Script pour charger des données de test dans la base de données
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from pf.models import (
    User, Patient, MethodeContraceptive, RendezVous,
    ConsultationPF, StockItem, Prescription, MouvementStock
)

def create_methodes_contraceptives():
    """Créer les méthodes contraceptives"""
    methodes = [
        {'nom': 'Pilule contraceptive combinée', 'categorie': 'hormonale', 'description': 'Pilule contenant œstrogène et progestatif'},
        {'nom': 'Pilule progestative', 'categorie': 'hormonale', 'description': 'Pilule contenant uniquement du progestatif'},
        {'nom': 'Implant contraceptif', 'categorie': 'hormonale', 'description': 'Implant sous-cutané à libération prolongée'},
        {'nom': 'Injection contraceptive', 'categorie': 'hormonale', 'description': 'Injection trimestrielle de progestatif'},
        {'nom': 'DIU au cuivre', 'categorie': 'iud', 'description': 'Dispositif intra-utérin au cuivre'},
        {'nom': 'DIU hormonal', 'categorie': 'iud', 'description': 'Dispositif intra-utérin hormonal'},
        {'nom': 'Préservatif masculin', 'categorie': 'barriere', 'description': 'Préservatif en latex ou polyuréthane'},
        {'nom': 'Préservatif féminin', 'categorie': 'barriere', 'description': 'Préservatif interne'},
        {'nom': 'Diaphragme', 'categorie': 'barriere', 'description': 'Barrière mécanique'},
        {'nom': 'Stérilisation féminine', 'categorie': 'permanent', 'description': 'Ligature des trompes'},
        {'nom': 'Stérilisation masculine', 'categorie': 'permanent', 'description': 'Vasectomie'},
        {'nom': 'Méthode du calendrier', 'categorie': 'naturelle', 'description': 'Suivi du cycle menstruel'},
        {'nom': 'Méthode de la température', 'categorie': 'naturelle', 'description': 'Suivi de la température basale'},
    ]
    
    created = []
    for methode_data in methodes:
        if not MethodeContraceptive.objects.filter(nom=methode_data['nom']).exists():
            methode = MethodeContraceptive.objects.create(**methode_data)
            created.append(methode)
            print(f"✅ Méthode créée : {methode.nom}")
    
    return created

def create_patients():
    """Créer des patients de test"""
    prenoms_f = ['Marie', 'Fatou', 'Aissatou', 'Aminata', 'Khadija', 'Mariama', 'Awa', 'Ndeye', 'Aissatou', 'Rokhaya']
    prenoms_m = ['Amadou', 'Moussa', 'Ibrahima', 'Ousmane', 'Mamadou', 'Cheikh', 'Modou', 'Pape', 'Alioune', 'Samba']
    noms = ['Diallo', 'Ba', 'Ndiaye', 'Seck', 'Fall', 'Diop', 'Sarr', 'Thiam', 'Sy', 'Kane', 'Gueye', 'Niang']
    
    patients = []
    for i in range(50):
        sexe = random.choice(['F', 'M'])
        if sexe == 'F':
            prenom = random.choice(prenoms_f)
        else:
            prenom = random.choice(prenoms_m)
        
        nom = random.choice(noms)
        email = f"{prenom.lower()}.{nom.lower()}{i}@example.com"
        
        if not Patient.objects.filter(nom=nom, prenom=prenom).exists():
            # Date de naissance entre 18 et 45 ans
            age = random.randint(18, 45)
            dob = datetime.now() - timedelta(days=age*365 + random.randint(0, 365))
            
            patient = Patient.objects.create(
                nom=nom,
                prenom=prenom,
                dob=dob.date(),
                sexe=sexe,
                telephone=f"+22177{random.randint(1000000, 9999999)}",
                adresse=f"Adresse {random.randint(1, 100)}, Dakar",
                antecedents=random.choice([
                    'Aucun antécédent notable',
                    'Hypertension artérielle',
                    'Diabète de type 2',
                    'Asthme',
                    'Allergie aux antibiotiques',
                    None
                ]),
                allergies=random.choice([
                    'Aucune allergie connue',
                    'Allergie à la pénicilline',
                    'Allergie aux produits laitiers',
                    None
                ])
            )
            patients.append(patient)
            print(f"✅ Patient créé : {patient.nom} {patient.prenom}")
    
    return patients

def create_rendez_vous(patients, users):
    """Créer des rendez-vous"""
    medecins = [u for u in users if u.role in ['medecin', 'sage_femme', 'infirmier']]
    if not medecins:
        print("⚠️  Aucun médecin trouvé pour créer des rendez-vous")
        return []
    
    rendez_vous = []
    statuts = ['planifie', 'confirme', 'en_cours', 'termine', 'annule', 'absent']
    
    for i in range(30):
        patient = random.choice(patients)
        medecin = random.choice(medecins)
        
        # Date entre aujourd'hui et dans 30 jours
        days_offset = random.randint(-15, 30)
        date_rdv = datetime.now() + timedelta(days=days_offset)
        date_rdv = date_rdv.replace(hour=random.randint(8, 17), minute=random.choice([0, 15, 30, 45]))
        
        statut = random.choice(statuts)
        if days_offset < 0:
            statut = random.choice(['termine', 'absent', 'annule'])
        elif days_offset > 0:
            statut = random.choice(['planifie', 'confirme'])
        
        rdv = RendezVous.objects.create(
            patient=patient,
            user=medecin,
            datetime=date_rdv,
            statut=statut,
            notes=random.choice([
                'Consultation de routine',
                'Suivi de planification familiale',
                'Consultation de contrôle',
                'Première consultation',
                None
            ])
        )
        rendez_vous.append(rdv)
        print(f"✅ Rendez-vous créé : {rdv.patient.nom} - {rdv.datetime.strftime('%d/%m/%Y %H:%M')}")
    
    return rendez_vous

def create_consultations(patients, users, methodes):
    """Créer des consultations"""
    medecins = [u for u in users if u.role in ['medecin', 'sage_femme', 'infirmier']]
    if not medecins or not methodes:
        print("⚠️  Données insuffisantes pour créer des consultations")
        return []
    
    consultations = []
    anamneses = [
        'Patient en bonne santé générale',
        'Antécédents de grossesses multiples',
        'Désire une méthode contraceptive fiable',
        'Consultation de suivi',
        'Première consultation de planification familiale',
    ]
    examens = [
        'Examen gynécologique normal',
        'Tension artérielle normale',
        'Poids et taille dans les normes',
        'Examen clinique sans particularité',
    ]
    
    for i in range(40):
        patient = random.choice(patients)
        medecin = random.choice(medecins)
        methode = random.choice(methodes)
        
        # Date entre il y a 60 jours et aujourd'hui
        days_offset = random.randint(-60, 0)
        date_consult = datetime.now() + timedelta(days=days_offset)
        date_consult = date_consult.replace(hour=random.randint(8, 17), minute=random.choice([0, 15, 30, 45]))
        
        consultation = ConsultationPF.objects.create(
            patient=patient,
            user=medecin,
            date=date_consult,
            anamnese=random.choice(anamneses),
            examen=random.choice(examens),
            methode_proposee=methode,
            methode_prescite=methode if random.choice([True, False]) else None,
            methode_posee=random.choice([True, False]),
            effets_secondaires=random.choice([
                'Aucun effet secondaire',
                'Nausées légères',
                'Maux de tête occasionnels',
                None
            ]),
            notes=f'Consultation du {date_consult.strftime("%d/%m/%Y")}',
            observation=random.choice([
                'Patient satisfait de la méthode',
                'Suivi recommandé dans 3 mois',
                'Méthode bien tolérée',
                None
            ])
        )
        consultations.append(consultation)
        print(f"✅ Consultation créée : {consultation.patient.nom} - {consultation.date.strftime('%d/%m/%Y')}")
    
    return consultations

def create_stocks(methodes):
    """Créer des stocks"""
    stocks = []
    for methode in methodes:
        quantite = random.randint(0, 200)
        seuil = random.randint(10, 30)
        
        stock, created = StockItem.objects.get_or_create(
            methode=methode,
            defaults={'quantite': quantite, 'seuil': seuil}
        )
        if created:
            stocks.append(stock)
            print(f"✅ Stock créé : {methode.nom} - Quantité: {quantite}, Seuil: {seuil}")
    
    return stocks

def create_prescriptions(consultations, methodes):
    """Créer des prescriptions"""
    prescriptions = []
    for consultation in consultations[:20]:  # Prescriptions pour 20 consultations
        if consultation.methode_prescite:
            prescription = Prescription.objects.create(
                consultation=consultation,
                methode=consultation.methode_prescite,
                dosage=random.choice([
                    '1 comprimé par jour',
                    '1 injection tous les 3 mois',
                    'À prendre le matin',
                    'Selon les instructions du médecin',
                ]),
                remarque=random.choice([
                    'Prendre à heure fixe',
                    'En cas d\'oubli, consulter la notice',
                    'Suivi dans 3 mois',
                    None
                ])
            )
            prescriptions.append(prescription)
            print(f"✅ Prescription créée pour consultation #{consultation.id}")
    
    return prescriptions

def main():
    """Fonction principale pour charger toutes les données"""
    print("=" * 80)
    print("CHARGEMENT DES DONNÉES DE TEST")
    print("=" * 80)
    print()
    
    # Vérifier les utilisateurs
    users = list(User.objects.all())
    if not users:
        print("⚠️  Aucun utilisateur trouvé. Créez d'abord des utilisateurs avec create_test_user.py")
        return
    
    print(f"📊 {len(users)} utilisateur(s) trouvé(s)")
    print()
    
    # Créer les méthodes contraceptives
    print("1. Création des méthodes contraceptives...")
    methodes = create_methodes_contraceptives()
    print(f"   ✅ {len(methodes)} méthode(s) créée(s)\n")
    
    # Créer les patients
    print("2. Création des patients...")
    patients = create_patients()
    print(f"   ✅ {len(patients)} patient(s) créé(s)\n")
    
    # Créer les stocks
    print("3. Création des stocks...")
    stocks = create_stocks(methodes)
    print(f"   ✅ {len(stocks)} stock(s) créé(s)\n")
    
    # Créer les rendez-vous
    print("4. Création des rendez-vous...")
    rendez_vous = create_rendez_vous(patients, users)
    print(f"   ✅ {len(rendez_vous)} rendez-vous créé(s)\n")
    
    # Créer les consultations
    print("5. Création des consultations...")
    consultations = create_consultations(patients, users, methodes)
    print(f"   ✅ {len(consultations)} consultation(s) créée(s)\n")
    
    # Créer les prescriptions
    print("6. Création des prescriptions...")
    prescriptions = create_prescriptions(consultations, methodes)
    print(f"   ✅ {len(prescriptions)} prescription(s) créée(s)\n")
    
    print("=" * 80)
    print("✅ CHARGEMENT TERMINÉ AVEC SUCCÈS !")
    print("=" * 80)
    print()
    print("Résumé :")
    print(f"  - Méthodes contraceptives : {MethodeContraceptive.objects.count()}")
    print(f"  - Patients : {Patient.objects.count()}")
    print(f"  - Stocks : {StockItem.objects.count()}")
    print(f"  - Rendez-vous : {RendezVous.objects.count()}")
    print(f"  - Consultations : {ConsultationPF.objects.count()}")
    print(f"  - Prescriptions : {Prescription.objects.count()}")
    print()

if __name__ == '__main__':
    main()

