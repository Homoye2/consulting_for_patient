#!/usr/bin/env python3
"""
Script de test pour l'API des registres
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_login():
    """Test de connexion avec un spécialiste"""
    login_data = {
        "email": "aissatou.diallo@hopital.sn",
        "password": "doc123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code == 200:
        data = response.json()
        print("✅ Connexion réussie")
        print(f"Utilisateur: {data['user']['nom']} ({data['user']['role']})")
        return data['access']
    else:
        print("❌ Erreur de connexion:", response.text)
        return None

def test_recherche_patient(token, numero_cni=None, numero_cne=None):
    """Test de recherche de patient"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {}
    if numero_cni:
        params['numero_cni'] = numero_cni
    if numero_cne:
        params['numero_cne'] = numero_cne
    
    response = requests.get(f"{BASE_URL}/registres/rechercher_patient/", 
                          headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['trouve']:
            print(f"✅ Patient trouvé: {data['patient']['nom']} {data['patient']['prenom']}")
            return data['patient']
        else:
            print("ℹ️ Aucun patient trouvé")
            return None
    else:
        print("❌ Erreur recherche patient:", response.text)
        return None

def test_create_registre(token):
    """Test de création d'un registre"""
    headers = {"Authorization": f"Bearer {token}"}
    
    registre_data = {
        "nom": "Test",
        "prenom": "Patient",
        "sexe": "M",
        "age": 30,
        "residence": "Dakar",
        "ethnie": "Wolof",
        "profession": "Ingénieur",
        "numero_cni": "1234567890123",  # Patient existant (Aminata Diallo)
        "telephone": "221771234567",
        "email": "test.patient@example.com",
        "consultation_nc": "oui",
        "consultation_ac": "non",
        "consultation_refere_asc": "non",
        "poids_kg": 70.5,
        "taille_cm": 175.0,
        "motif_symptomes": "Consultation de routine",
        "examen_labo_type": "negatif",
        "diagnostic": "Patient en bonne santé"
    }
    
    response = requests.post(f"{BASE_URL}/registres/", 
                           headers=headers, json=registre_data)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Registre créé avec succès - ID: {data.get('id', 'N/A')}")
        print(f"Patient lié: {data.get('patient_nom_complet', 'Nouveau patient')}")
        print(f"Réponse complète: {json.dumps(data, indent=2)}")
        return data
    else:
        print("❌ Erreur création registre:", response.text)
        print(f"Status code: {response.status_code}")
        return None

def main():
    print("🧪 Test de l'API des registres")
    print("=" * 40)
    
    # 1. Test de connexion
    token = test_login()
    if not token:
        return
    
    print("\n" + "=" * 40)
    
    # 2. Test de recherche de patients existants
    print("🔍 Test de recherche de patients existants:")
    test_recherche_patient(token, numero_cni="1234567890123")
    test_recherche_patient(token, numero_cne="CNE123456789")
    test_recherche_patient(token, numero_cni="INEXISTANT")
    
    print("\n" + "=" * 40)
    
    # 3. Test de création de registre
    print("📝 Test de création de registre:")
    registre = test_create_registre(token)
    
    print("\n" + "=" * 40)
    print("✅ Tests terminés")

if __name__ == "__main__":
    main()