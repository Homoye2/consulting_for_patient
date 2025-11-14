#!/usr/bin/env python
"""
Script pour tester la connexion via l'API
"""
import requests
import json

url = "http://127.0.0.1:8000/api/auth/login/"
data = {
    "email": "admin@example.com",
    "password": "admin123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except requests.exceptions.ConnectionError:
    print("❌ Erreur: Impossible de se connecter au serveur. Assurez-vous que le serveur Django est démarré.")
except Exception as e:
    print(f"❌ Erreur: {e}")

