#!/bin/bash

echo "🔧 Correction de l'erreur 500..."
echo ""

echo "📋 Étape 1 : Vérification des migrations existantes"
python3 manage.py showmigrations pf | tail -5

echo ""
echo "🔄 Étape 2 : Application de la migration des factures fournisseurs"
python3 manage.py migrate pf 0999_add_factures_fournisseurs

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Erreur lors de la migration, tentative avec --fake-initial"
    python3 manage.py migrate --fake-initial
fi

echo ""
echo "✅ Étape 3 : Vérification des migrations appliquées"
python3 manage.py showmigrations pf | grep 0999

echo ""
echo "🎉 Migration terminée !"
echo ""
echo "📝 Prochaines étapes :"
echo "1. Redémarrez le serveur : python3 manage.py runserver"
echo "2. Rafraîchissez le navigateur : Ctrl+Shift+R"
echo ""
