#!/usr/bin/env python
"""
Script pour créer des produits de test dans les pharmacies
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from pf.models import Produit, Pharmacie

def seed_produits():
    print("\n" + "="*60)
    print("🌱 CRÉATION DES PRODUITS DE TEST")
    print("="*60)
    
    pharmacies = Pharmacie.objects.filter(actif=True)
    
    if not pharmacies.exists():
        print("\n❌ Aucune pharmacie active trouvée!")
        print("💡 Exécutez d'abord: python3 seed_database.py")
        return
    
    print(f"\n📊 {pharmacies.count()} pharmacie(s) active(s) trouvée(s)")
    
    produits_data = [
        {
            'nom': 'Paracétamol 500mg',
            'description': 'Antidouleur et antipyrétique. Boîte de 20 comprimés.',
            'prix': '2500',
            'categorie': 'medicament',
            'prescription_requise': False,
        },
        {
            'nom': 'Ibuprofène 400mg',
            'description': 'Anti-inflammatoire non stéroïdien. Boîte de 20 comprimés.',
            'prix': '3000',
            'categorie': 'medicament',
            'prescription_requise': False,
        },
        {
            'nom': 'Amoxicilline 1g',
            'description': 'Antibiotique à large spectre. Boîte de 12 comprimés.',
            'prix': '5000',
            'categorie': 'medicament',
            'prescription_requise': True,
        },
        {
            'nom': 'Doliprane 1000mg',
            'description': 'Paracétamol dosage fort. Boîte de 8 comprimés.',
            'prix': '3500',
            'categorie': 'medicament',
            'prescription_requise': False,
        },
        {
            'nom': 'Vitamine C 1000mg',
            'description': 'Complément alimentaire. Boîte de 30 comprimés effervescents.',
            'prix': '4000',
            'categorie': 'complement',
            'prescription_requise': False,
        },
        {
            'nom': 'Aspirine 500mg',
            'description': 'Antiagrégant plaquettaire. Boîte de 20 comprimés.',
            'prix': '2000',
            'categorie': 'medicament',
            'prescription_requise': False,
        },
        {
            'nom': 'Sirop contre la toux',
            'description': 'Sirop expectorant. Flacon de 125ml.',
            'prix': '3500',
            'categorie': 'medicament',
            'prescription_requise': False,
        },
        {
            'nom': 'Crème hydratante',
            'description': 'Crème pour peaux sèches. Tube de 100ml.',
            'prix': '5500',
            'categorie': 'parapharmacie',
            'prescription_requise': False,
        },
        {
            'nom': 'Thermomètre digital',
            'description': 'Thermomètre électronique précis.',
            'prix': '8000',
            'categorie': 'materiel',
            'prescription_requise': False,
        },
        {
            'nom': 'Masques chirurgicaux',
            'description': 'Boîte de 50 masques jetables.',
            'prix': '6000',
            'categorie': 'materiel',
            'prescription_requise': False,
        }
    ]
    
    print(f"\n📦 Création de {len(produits_data)} produits par pharmacie...")
    print("-"*60)
    
    created_count = 0
    updated_count = 0
    
    for pharmacie in pharmacies:
        print(f"\n🏪 {pharmacie.nom}")
        for p_data in produits_data:
            # Vérifier si le produit existe déjà
            produit, created = Produit.objects.get_or_create(
                nom=p_data['nom'],
                pharmacie=pharmacie,
                defaults={
                    **p_data,
                    'en_stock': True
                }
            )
            
            if created:
                created_count += 1
                print(f"   ✅ {p_data['nom']} - {p_data['prix']} FCFA")
            else:
                # Mettre à jour le produit existant
                for key, value in p_data.items():
                    setattr(produit, key, value)
                produit.en_stock = True
                produit.save()
                updated_count += 1
                print(f"   🔄 {p_data['nom']} (mis à jour)")
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    print(f"✅ Produits créés: {created_count}")
    print(f"🔄 Produits mis à jour: {updated_count}")
    print(f"📦 Total dans la base: {Produit.objects.count()}")
    print("\n💡 Vous pouvez maintenant ajouter ces produits au panier et passer des commandes!")
    print("="*60 + "\n")

if __name__ == '__main__':
    seed_produits()
