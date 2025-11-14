#!/usr/bin/env python
"""
Script pour charger les données initiales de la landing page
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from pf.models import LandingPageContent, Service, Value

def load_initial_data():
    """Charge les données initiales de la landing page"""
    
    # Créer ou récupérer le contenu principal
    content, created = LandingPageContent.objects.get_or_create(
        pk=1,
        defaults={
            'logo_text': 'Hôpital Abass Ndao',
            'hero_title': 'Bienvenue à l\'Hôpital Abass Ndao',
            'hero_description': 'Votre partenaire de confiance pour la santé et le bien-être. Nous offrons des services médicaux de qualité avec un personnel dévoué et des équipements modernes.',
            'hero_button_primary': 'Accéder à l\'application',
            'hero_button_secondary': 'En savoir plus',
            'about_title': 'À propos de l\'Hôpital Abass Ndao',
            'about_description_1': 'L\'Hôpital Abass Ndao est un établissement de santé moderne et bien équipé, dédié à offrir des soins médicaux de qualité à la communauté. Fondé avec une vision de service public et d\'excellence médicale, nous nous engageons à fournir des soins accessibles et professionnels.',
            'about_description_2': 'Notre équipe médicale expérimentée travaille avec dévouement pour assurer le bien-être de nos patients. Nous mettons l\'accent sur la prévention, le traitement et le suivi continu de la santé.',
            'about_stat_1_value': '15+',
            'about_stat_1_label': 'Années d\'expérience',
            'about_stat_2_value': '50+',
            'about_stat_2_label': 'Professionnels',
            'services_title': 'Nos Services',
            'services_subtitle': 'Nous offrons une gamme complète de services médicaux pour répondre à tous vos besoins de santé',
            'values_title': 'Pourquoi nous choisir ?',
            'values_subtitle': 'Des valeurs qui font la différence dans nos soins',
            'footer_about_text': 'Votre partenaire de confiance pour la santé et le bien-être de la communauté.',
            'footer_address': 'Abass Ndao, Dakar, Sénégal',
            'footer_phone': '+221 33 XXX XX XX',
            'footer_email': 'contact@abassndao.sn',
        }
    )
    
    if created:
        print("✅ Contenu de la landing page créé")
    else:
        print("ℹ️  Contenu de la landing page existe déjà")
    
    # Créer les services
    services_data = [
        {'titre': 'Planification Familiale', 'description': 'Consultation et suivi en planification familiale avec des méthodes contraceptives modernes et sûres.', 'icone': 'Heart', 'ordre': 1},
        {'titre': 'Consultations Médicales', 'description': 'Consultations générales et spécialisées avec nos médecins qualifiés et expérimentés.', 'icone': 'Stethoscope', 'ordre': 2},
        {'titre': 'Prise de Rendez-vous', 'description': 'Système de prise de rendez-vous en ligne pour faciliter votre accès aux soins.', 'icone': 'Calendar', 'ordre': 3},
        {'titre': 'Suivi des Consultations', 'description': 'Suivi médical continu avec historique complet de vos consultations et prescriptions.', 'icone': 'FileText', 'ordre': 4},
        {'titre': 'Gestion des Stocks', 'description': 'Gestion optimisée des stocks médicaux pour garantir la disponibilité des produits.', 'icone': 'Package', 'ordre': 5},
        {'titre': 'Gestion des Patients', 'description': 'Dossier médical électronique sécurisé pour chaque patient avec historique complet.', 'icone': 'Users', 'ordre': 6},
    ]
    
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            landing_page=content,
            titre=service_data['titre'],
            defaults=service_data
        )
        if created:
            print(f"✅ Service créé : {service_data['titre']}")
    
    # Créer les valeurs
    values_data = [
        {'titre': 'Confidentialité', 'description': 'Vos données médicales sont protégées et traitées avec la plus grande confidentialité.', 'icone': 'Shield', 'ordre': 1},
        {'titre': 'Excellence', 'description': 'Des standards de qualité élevés et un personnel médical hautement qualifié.', 'icone': 'Award', 'ordre': 2},
        {'titre': 'Disponibilité', 'description': 'Accès facile aux soins avec un système de rendez-vous flexible et efficace.', 'icone': 'Clock', 'ordre': 3},
        {'titre': 'Empathie', 'description': 'Une approche humaine et bienveillante pour chaque patient.', 'icone': 'Heart', 'ordre': 4},
    ]
    
    for value_data in values_data:
        value, created = Value.objects.get_or_create(
            landing_page=content,
            titre=value_data['titre'],
            defaults=value_data
        )
        if created:
            print(f"✅ Valeur créée : {value_data['titre']}")
    
    print("\n✅ Données de la landing page chargées avec succès !")

if __name__ == '__main__':
    load_initial_data()

