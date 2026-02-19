#!/bin/bash

# Script pour créer et appliquer les migrations

echo "🔄 Création des migrations..."
python3 manage.py makemigrations

echo ""
echo "✅ Migrations créées !"
echo ""
echo "📋 Aperçu des migrations à appliquer..."
python3 manage.py showmigrations pf | tail -5

echo ""
echo "🚀 Application des migrations..."
python3 manage.py migrate

echo ""
echo "✅ Migrations appliquées avec succès !"
echo ""
echo "🎉 Le backend est prêt !"
