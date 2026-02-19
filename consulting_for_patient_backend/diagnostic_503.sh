#!/bin/bash

# Script de diagnostic pour l'erreur 503
# À exécuter sur le serveur: bash diagnostic_503.sh

echo "=========================================="
echo "DIAGNOSTIC ERREUR 503 - E-SORA"
echo "=========================================="
echo ""

# 1. Vérifier la structure
echo "1. STRUCTURE DES FICHIERS"
echo "-------------------------"
cd /home/onglsmjm/e_sora.onglalumiere.org/
echo "Racine du domaine:"
ls -la | grep -E "^d|^-.*\.htaccess|^-.*backend"
echo ""

cd backend/
echo "Dossier backend:"
ls -la | grep -E "passenger_wsgi|manage\.py|mysite|venv|\.env"
echo ""

# 2. Vérifier Python
echo "2. VERSIONS PYTHON"
echo "------------------"
echo "Python système:"
python3 --version 2>/dev/null || echo "Python3 non trouvé"
echo ""

echo "Python 3.12:"
/opt/alt/python312/bin/python3.12 --version 2>/dev/null || echo "Python 3.12 non trouvé"
echo ""

echo "Python du venv:"
source venv/bin/activate
python --version
echo "Django version:"
python -c "import django; print(django.get_version())" 2>/dev/null || echo "Django non installé"
deactivate
echo ""

# 3. Vérifier .htaccess
echo "3. CONFIGURATION .HTACCESS"
echo "--------------------------"
cd /home/onglsmjm/e_sora.onglalumiere.org/
if [ -f .htaccess ]; then
    echo "Contenu .htaccess (10 premières lignes):"
    head -10 .htaccess
else
    echo "❌ .htaccess non trouvé!"
fi
echo ""

# 4. Vérifier passenger_wsgi.py
echo "4. PASSENGER_WSGI.PY"
echo "--------------------"
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
if [ -f passenger_wsgi.py ]; then
    echo "✅ passenger_wsgi.py existe"
    echo "Taille: $(wc -l < passenger_wsgi.py) lignes"
    echo ""
    echo "Contient os.execl()?"
    grep -n "os.execl" passenger_wsgi.py && echo "⚠️  PROBLÈME: os.execl() trouvé!" || echo "✅ Pas de os.execl()"
else
    echo "❌ passenger_wsgi.py non trouvé!"
fi
echo ""

# 5. Vérifier .env.production
echo "5. CONFIGURATION .ENV.PRODUCTION"
echo "--------------------------------"
if [ -f .env.production ]; then
    echo "✅ .env.production existe"
    echo "ALLOWED_HOSTS:"
    grep "ALLOWED_HOSTS" .env.production || echo "❌ ALLOWED_HOSTS non défini"
    echo "DEBUG:"
    grep "DEBUG" .env.production || echo "❌ DEBUG non défini"
else
    echo "❌ .env.production non trouvé!"
fi
echo ""

# 6. Vérifier les permissions
echo "6. PERMISSIONS"
echo "--------------"
cd /home/onglsmjm/e_sora.onglalumiere.org/
echo "Racine:"
ls -ld . | awk '{print $1, $3, $4, $9}'
echo ".htaccess:"
ls -l .htaccess 2>/dev/null | awk '{print $1, $3, $4, $9}' || echo "❌ .htaccess non trouvé"
echo ""
echo "Backend:"
ls -ld backend/ | awk '{print $1, $3, $4, $9}'
echo "passenger_wsgi.py:"
ls -l backend/passenger_wsgi.py 2>/dev/null | awk '{print $1, $3, $4, $9}' || echo "❌ passenger_wsgi.py non trouvé"
echo ""

# 7. Vérifier les logs
echo "7. DERNIÈRES ERREURS"
echo "--------------------"
echo "stderr.log (5 dernières lignes):"
tail -5 /home/onglsmjm/e_sora.onglalumiere.org/backend/stderr.log 2>/dev/null || echo "Pas de stderr.log"
echo ""

echo "passenger_error.log:"
cat /home/onglsmjm/e_sora.onglalumiere.org/backend/passenger_error.log 2>/dev/null || echo "Pas de passenger_error.log"
echo ""

echo "Apache error log (5 dernières lignes):"
tail -5 ~/logs/e-sora.onglalumiere.org-error_log 2>/dev/null || echo "Pas d'error_log"
echo ""

# 8. Test Django
echo "8. TEST DJANGO"
echo "--------------"
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
source venv/bin/activate
echo "Django check:"
python manage.py check 2>&1 | head -5
deactivate
echo ""

echo "=========================================="
echo "FIN DU DIAGNOSTIC"
echo "=========================================="
echo ""
echo "ANALYSE:"
echo "--------"

# Analyser les problèmes
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
if grep -q "os.execl" passenger_wsgi.py 2>/dev/null; then
    echo "❌ PROBLÈME TROUVÉ: passenger_wsgi.py contient os.execl()"
    echo "   Solution: Supprimer la section os.execl() du fichier"
    echo "   Voir: SOLUTION_FINALE_503.md"
fi

if ! grep -q "PassengerEnabled On" /home/onglsmjm/e_sora.onglalumiere.org/.htaccess 2>/dev/null; then
    echo "❌ PROBLÈME: PassengerEnabled On manquant dans .htaccess"
fi

if tail -5 stderr.log 2>/dev/null | grep -q "ModuleNotFoundError"; then
    echo "❌ PROBLÈME: Erreur ModuleNotFoundError détectée"
    echo "   Cause: Passenger essaie d'exécuter passenger_wsgi.py comme module"
    echo "   Solution: Corriger .htaccess et passenger_wsgi.py"
fi

echo ""
echo "Pour corriger, suivez: SOLUTION_FINALE_503.md"
