"""
Script pour créer plusieurs patients avec leurs consultations et rendez-vous
"""
import os
import django
from datetime import datetime, timedelta
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.utils import timezone
from pf.models import (
    User, Patient, MethodeContraceptive, RendezVous,
    ConsultationPF
)

def create_patient_with_user(nom, prenom, email, password, dob, sexe, telephone=None, adresse=None):
    """Crée un patient avec un compte utilisateur associé"""
    # Créer l'utilisateur
    user = User.objects.create_user(
        email=email,
        password=password,
        nom=nom,
        role='agent_enregistrement'  # Rôle temporaire, on le changera après
    )
    
    # Créer le patient
    patient = Patient.objects.create(
        nom=nom,
        prenom=prenom,
        dob=dob,
        sexe=sexe,
        telephone=telephone,
        email=email,
        adresse=adresse,
        user=user
    )
    
    return patient, user

def create_consultations_for_patient(patient, count=5):
    """Crée des consultations pour un patient"""
    consultations = []
    methodes = list(MethodeContraceptive.objects.all())
    professionnels = list(User.objects.filter(role__in=['medecin', 'sage_femme', 'infirmier']))
    
    if not methodes:
        print("⚠️  Aucune méthode contraceptive trouvée. Création de quelques méthodes...")
        methodes = [
            MethodeContraceptive.objects.create(nom="Pilule", categorie="hormonale"),
            MethodeContraceptive.objects.create(nom="Implant", categorie="hormonale"),
            MethodeContraceptive.objects.create(nom="DIU", categorie="iud"),
            MethodeContraceptive.objects.create(nom="Préservatif", categorie="barriere"),
        ]
    
    if not professionnels:
        print("⚠️  Aucun professionnel trouvé. Utilisation d'un admin par défaut...")
        professionnels = [User.objects.filter(role='administrateur').first()]
        if not professionnels:
            professionnels = [User.objects.first()]
    
    for i in range(count):
        date_consultation = timezone.now() - timedelta(days=random.randint(0, 180))
        professionnel = random.choice(professionnels) if professionnels else None
        
        methode_prescite = random.choice(methodes) if methodes else None
        methode_posee = random.choice([True, False])
        
        consultation = ConsultationPF.objects.create(
            patient=patient,
            user=professionnel,
            date=date_consultation,
            anamnese=f"Consultation de suivi #{i+1}. Patient se présente pour suivi de planification familiale.",
            examen=f"Examen clinique normal. Tension artérielle: {random.randint(100, 140)}/{random.randint(60, 90)} mmHg.",
            methode_proposee=random.choice(methodes) if methodes else None,
            methode_prescite=methode_prescite,
            methode_posee=methode_posee,
            effets_secondaires=random.choice([
                None,
                "Légers maux de tête",
                "Nausées légères",
                "Aucun effet secondaire",
                "Irregularités menstruelles"
            ]),
            notes=f"Patient suit bien le traitement. Prochaine consultation recommandée dans 3 mois.",
            observation=f"Patient informé des différentes options. Consentement éclairé obtenu."
        )
        consultations.append(consultation)
    
    return consultations

def create_rendez_vous_for_patient(patient, count=8):
    """Crée des rendez-vous pour un patient"""
    rendez_vous = []
    professionnels = list(User.objects.filter(role__in=['medecin', 'sage_femme', 'infirmier']))
    
    if not professionnels:
        professionnels = [User.objects.filter(role='administrateur').first()]
        if not professionnels:
            professionnels = [User.objects.first()]
    
    # Rendez-vous passés
    for i in range(count // 2):
        datetime_rdv = timezone.now() - timedelta(days=random.randint(1, 90))
        statut = random.choice(['termine', 'confirme', 'annule'])
        professionnel = random.choice(professionnels) if professionnels else None
        
        rdv = RendezVous.objects.create(
            patient=patient,
            user=professionnel,
            datetime=datetime_rdv,
            statut=statut,
            notes=f"Rendez-vous pour consultation de planification familiale."
        )
        rendez_vous.append(rdv)
    
    # Rendez-vous à venir
    for i in range(count // 2):
        datetime_rdv = timezone.now() + timedelta(days=random.randint(1, 60))
        statut = random.choice(['en_attente', 'confirme'])
        professionnel = random.choice(professionnels) if professionnels else None
        
        rdv = RendezVous.objects.create(
            patient=patient,
            user=professionnel,
            datetime=datetime_rdv,
            statut=statut,
            notes=f"Rendez-vous de suivi demandé par le patient."
        )
        rendez_vous.append(rdv)
    
    return rendez_vous

def main():
    print("=" * 60)
    print("Création de patients avec consultations et rendez-vous")
    print("=" * 60)
    
    # Liste de patients à créer
    patients_data = [
        {
            'nom': 'Diallo',
            'prenom': 'Aissatou',
            'email': 'aissatou.diallo@example.com',
            'password': 'patient123',
            'dob': datetime(1995, 3, 15).date(),
            'sexe': 'F',
            'telephone': '+221 77 123 45 67',
            'adresse': 'Dakar, Almadies'
        },
        {
            'nom': 'Ndiaye',
            'prenom': 'Moussa',
            'email': 'moussa.ndiaye@example.com',
            'password': 'patient123',
            'dob': datetime(1992, 7, 22).date(),
            'sexe': 'M',
            'telephone': '+221 77 234 56 78',
            'adresse': 'Dakar, Plateau'
        },
        {
            'nom': 'Ba',
            'prenom': 'Fatou',
            'email': 'fatou.ba@example.com',
            'password': 'patient123',
            'dob': datetime(1998, 11, 8).date(),
            'sexe': 'F',
            'telephone': '+221 77 345 67 89',
            'adresse': 'Dakar, Ouakam'
        },
        {
            'nom': 'Sarr',
            'prenom': 'Ibrahima',
            'email': 'ibrahima.sarr@example.com',
            'password': 'patient123',
            'dob': datetime(1990, 5, 30).date(),
            'sexe': 'M',
            'telephone': '+221 77 456 78 90',
            'adresse': 'Dakar, Yoff'
        },
        {
            'nom': 'Diop',
            'prenom': 'Aminata',
            'email': 'aminata.diop@example.com',
            'password': 'patient123',
            'dob': datetime(1996, 9, 12).date(),
            'sexe': 'F',
            'telephone': '+221 77 567 89 01',
            'adresse': 'Dakar, Mermoz'
        },
        {
            'nom': 'Fall',
            'prenom': 'Ousmane',
            'email': 'ousmane.fall@example.com',
            'password': 'patient123',
            'dob': datetime(1993, 1, 25).date(),
            'sexe': 'M',
            'telephone': '+221 77 678 90 12',
            'adresse': 'Dakar, Sacré-Cœur'
        },
        {
            'nom': 'Thiam',
            'prenom': 'Mariama',
            'email': 'mariama.thiam@example.com',
            'password': 'patient123',
            'dob': datetime(1997, 4, 18).date(),
            'sexe': 'F',
            'telephone': '+221 77 789 01 23',
            'adresse': 'Dakar, Fann'
        },
        {
            'nom': 'Cissé',
            'prenom': 'Mamadou',
            'email': 'mamadou.cisse@example.com',
            'password': 'patient123',
            'dob': datetime(1991, 8, 5).date(),
            'sexe': 'M',
            'telephone': '+221 77 890 12 34',
            'adresse': 'Dakar, Point E'
        },
        {
            'nom': 'Kane',
            'prenom': 'Khadija',
            'email': 'khadija.kane@example.com',
            'password': 'patient123',
            'dob': datetime(1994, 12, 20).date(),
            'sexe': 'F',
            'telephone': '+221 77 901 23 45',
            'adresse': 'Dakar, Liberté 6'
        },
        {
            'nom': 'Sy',
            'prenom': 'Modou',
            'email': 'modou.sy@example.com',
            'password': 'patient123',
            'dob': datetime(1989, 6, 14).date(),
            'sexe': 'M',
            'telephone': '+221 77 012 34 56',
            'adresse': 'Dakar, Grand Yoff'
        },
    ]
    
    total_patients = 0
    total_consultations = 0
    total_rendez_vous = 0
    
    for patient_data in patients_data:
        try:
            # Vérifier si le patient existe déjà
            if Patient.objects.filter(email=patient_data['email']).exists():
                print(f"⚠️  Patient {patient_data['nom']} {patient_data['prenom']} existe déjà. Passage au suivant...")
                continue
            
            # Créer le patient avec son compte utilisateur
            patient, user = create_patient_with_user(**patient_data)
            total_patients += 1
            print(f"✅ Patient créé: {patient.nom} {patient.prenom} ({patient.email})")
            
            # Créer des consultations
            consultations = create_consultations_for_patient(patient, count=random.randint(3, 8))
            total_consultations += len(consultations)
            print(f"   📋 {len(consultations)} consultations créées")
            
            # Créer des rendez-vous
            rendez_vous = create_rendez_vous_for_patient(patient, count=random.randint(5, 12))
            total_rendez_vous += len(rendez_vous)
            print(f"   📅 {len(rendez_vous)} rendez-vous créés")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du patient {patient_data['nom']}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("Résumé:")
    print(f"  • {total_patients} patients créés")
    print(f"  • {total_consultations} consultations créées")
    print(f"  • {total_rendez_vous} rendez-vous créés")
    print("=" * 60)
    print("\n✅ Données chargées avec succès !")
    print("\n📝 Identifiants de connexion (tous avec le mot de passe: patient123):")
    for patient_data in patients_data:
        print(f"   • {patient_data['email']} - {patient_data['nom']} {patient_data['prenom']}")

if __name__ == '__main__':
    main()

