#!/bin/bash
# Script de nettoyage des fichiers inutiles

echo "🧹 Nettoyage des fichiers inutiles..."

# Supprimer les fichiers Python compilés
echo "Suppression des fichiers .pyc et __pycache__..."
find . -name "*.pyc" -type f -delete
find . -name "__pycache__" -type d -delete

# Supprimer les fichiers de backup
echo "Suppression des fichiers de backup..."
find . -name "*.bak" -type f -delete
find . -name "*~" -type f -delete

# Supprimer les logs
echo "Suppression des logs..."
find . -name "*.log" -type f -delete
find . -name "stderr.log" -type f -delete
find . -name "passenger_error.log" -type f -delete

# Supprimer les fichiers temporaires
echo "Suppression des fichiers temporaires..."
rm -f cookies.txt token.txt 2>/dev/null

# Supprimer les fichiers DS_Store (macOS)
echo "Suppression des fichiers .DS_Store..."
find . -name ".DS_Store" -type f -delete

# Supprimer les anciens venv (si présents)
echo "Suppression des anciens environnements virtuels..."
rm -rf venv_old* 2>/dev/null

# Nettoyer les migrations inutiles (optionnel - commenté par sécurité)
# echo "Nettoyage des migrations..."
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc" -delete

# Nettoyer le cache pip
echo "Nettoyage du cache pip..."
pip cache purge 2>/dev/null || true

# Afficher l'espace libéré
echo ""
echo "✅ Nettoyage terminé!"
echo ""
echo "Espace disque utilisé par le projet:"
du -sh .
echo ""
echo "Détails par répertoire:"
du -sh */ 2>/dev/null | sort -hr | head -10
