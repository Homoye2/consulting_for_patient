#!/bin/bash

echo "🚀 Démarrage du serveur Django E-Sora"
echo "======================================"
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé"
    echo "   Exécutez ce script depuis le dossier consulting_for_patient_backend"
    exit 1
fi

# Afficher l'adresse IP locale
echo "📡 Adresses réseau disponibles:"
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print "   - " $2}'
echo ""

# Démarrer le serveur sur toutes les interfaces
echo "🌐 Démarrage du serveur sur 0.0.0.0:8000"
echo "   Accessible depuis:"
echo "   - http://localhost:8000 (local)"
echo "   - http://192.168.1.2:8000 (réseau)"
echo ""
echo "📱 L'application mobile peut maintenant se connecter"
echo ""
echo "⏹️  Pour arrêter le serveur: Ctrl+C"
echo ""

python3 manage.py runserver 0.0.0.0:8000
