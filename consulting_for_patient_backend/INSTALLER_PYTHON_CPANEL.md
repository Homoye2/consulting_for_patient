# Guide d'installation de Python 3.9+ sur cPanel

## Problème identifié

Votre serveur a Python 3.6.8, mais Django 5.2 nécessite Python 3.10+.

```bash
[onglsmjm@server305 ~]$ python3 --version
Python 3.6.8
```

**Versions requises:**
- Django 5.2 → Python 3.10, 3.11 ou 3.12
- Django 4.2 LTS → Python 3.8, 3.9, 3.10, 3.11 ou 3.12
- Django 3.2 LTS → Python 3.6, 3.7, 3.8, 3.9 ou 3.10

---

## Solution 1: Downgrade vers Django 4.2 LTS (Recommandé)

C'est la solution la plus simple et la plus stable.

### Avantages:
- Compatible avec Python 3.6.8
- Version LTS (Long Term Support) jusqu'en avril 2026
- Toutes vos fonctionnalités actuelles fonctionneront
- Pas besoin de compiler Python

### Étapes:

#### 1. Modifier requirements.txt localement

```bash
cd consulting_for_patient_backend
nano requirements.txt
```

Changez:
```
Django==5.2.8
```

En:
```
Django==4.2.11
```

#### 2. Tester localement (optionnel mais recommandé)

```bash
# Créer un nouvel environnement de test
python3 -m venv venv_test
source venv_test/bin/activate
pip install -r requirements.txt

# Tester les migrations
python manage.py check
python manage.py migrate --run-syncdb

# Si tout fonctionne, c'est bon!
deactivate
rm -rf venv_test
```

#### 3. Déployer sur le serveur

Suivez le guide `DEPLOIEMENT_CPANEL.md` normalement avec le nouveau `requirements.txt`.

---

## Solution 2: Installer Python 3.9+ via pyenv (Avancé)

Si vous avez besoin de Python 3.9+, vous pouvez l'installer avec pyenv.

### Prérequis

Vous devez avoir accès SSH et les outils de compilation.

### Étape 1: Vérifier les dépendances

```bash
ssh onglsmjm@server305.com

# Vérifier si gcc est disponible
gcc --version

# Vérifier si make est disponible
make --version
```

Si ces commandes échouent, contactez votre hébergeur pour activer les outils de compilation.

### Étape 2: Installer pyenv

```bash
cd ~
curl https://pyenv.run | bash
```

### Étape 3: Configurer le shell

Ajoutez à votre `~/.bashrc`:

```bash
nano ~/.bashrc
```

Ajoutez à la fin:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Rechargez:

```bash
source ~/.bashrc
```

### Étape 4: Installer Python 3.9

```bash
# Lister les versions disponibles
pyenv install --list | grep " 3.9"

# Installer Python 3.9.18 (dernière version 3.9)
pyenv install 3.9.18

# Définir comme version globale
pyenv global 3.9.18

# Vérifier
python --version
# Devrait afficher: Python 3.9.18
```

### Étape 5: Créer l'environnement virtuel

```bash
cd ~/applications/consulting_backend
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Étape 6: Mettre à jour passenger_wsgi.py

```python
import os
import sys

# Utiliser Python de pyenv
INTERP = os.path.join(os.environ['HOME'], '.pyenv', 'versions', '3.9.18', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# ... reste du fichier
```

---

## Solution 3: Demander à l'hébergeur d'installer Python 3.9+

Contactez le support de votre hébergeur et demandez:

```
Bonjour,

Je souhaite déployer une application Django 5.2 qui nécessite Python 3.10+.
Actuellement, le serveur a Python 3.6.8.

Pourriez-vous installer Python 3.10 ou 3.11 sur le serveur?
Ou activer Python 3.10+ dans "Setup Python App" de cPanel?

Merci
```

Beaucoup d'hébergeurs peuvent activer des versions plus récentes de Python.

---

## Solution 4: Utiliser un hébergement compatible (Alternative)

Si aucune des solutions ci-dessus ne fonctionne, considérez ces alternatives:

### A. PythonAnywhere
- Python 3.10, 3.11, 3.12 disponibles
- Déploiement Django simplifié
- Plan gratuit disponible
- https://www.pythonanywhere.com

### B. Heroku
- Support Python 3.11+
- Déploiement via Git
- Plan gratuit disponible (avec limitations)
- https://www.heroku.com

### C. DigitalOcean App Platform
- Python 3.11+ supporté
- Déploiement automatisé
- À partir de 5$/mois
- https://www.digitalocean.com

### D. Railway
- Python 3.11+ supporté
- Déploiement via Git
- Plan gratuit disponible
- https://railway.app

---

## Recommandation finale

**Pour votre cas (Python 3.6.8 sur cPanel):**

### Option 1 (Recommandée): Downgrade vers Django 4.2 LTS

✅ **Avantages:**
- Fonctionne immédiatement avec Python 3.6.8
- Stable et supporté jusqu'en 2026
- Aucune modification majeure du code
- Pas de compilation nécessaire

❌ **Inconvénients:**
- Pas les toutes dernières fonctionnalités de Django 5.2
- Mais toutes vos fonctionnalités actuelles fonctionneront

### Option 2: Installer Python 3.9 via pyenv

✅ **Avantages:**
- Garde Django 5.2
- Contrôle total sur la version Python

❌ **Inconvénients:**
- Nécessite des outils de compilation
- Plus complexe à maintenir
- Peut prendre 30-60 minutes pour compiler

### Option 3: Changer d'hébergeur

✅ **Avantages:**
- Environnement moderne
- Meilleures performances
- Support Python récent

❌ **Inconvénients:**
- Coût potentiel
- Migration nécessaire

---

## Modifications nécessaires pour Django 4.2

Si vous choisissez l'Option 1 (recommandée), voici les modifications à faire:

### 1. requirements.txt

```txt
Django==4.2.11
djangorestframework==3.14.0
django-cors-headers==4.3.1
mysqlclient==2.2.4
Pillow==10.2.0
PyJWT==2.8.0
python-dotenv==1.0.1
drf-yasg==1.21.7
qrcode==7.4.2
gunicorn==21.2.0
psutil==5.9.8
```

### 2. Vérifier la compatibilité

Django 4.2 est presque identique à Django 5.2 pour votre usage. Les différences principales:

**Ce qui change:**
- Quelques nouvelles fonctionnalités de Django 5.2 ne seront pas disponibles
- Syntaxe légèrement différente pour certaines fonctionnalités avancées

**Ce qui reste identique:**
- Models, Views, Serializers
- Django REST Framework
- Authentification
- Migrations
- Admin
- Toutes vos APIs

### 3. Tester les migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py check
```

Si tout passe, vous êtes prêt pour le déploiement!

---

## Script de vérification de compatibilité

Créez ce script pour vérifier la compatibilité:

```bash
#!/bin/bash
# check_compatibility.sh

echo "=== Vérification de compatibilité Django 4.2 ==="
echo ""

# Vérifier Python
echo "Version Python:"
python3 --version
echo ""

# Vérifier Django
echo "Version Django:"
python3 -c "import django; print(django.get_version())"
echo ""

# Vérifier les dépendances
echo "Vérification des dépendances:"
python3 manage.py check --deploy
echo ""

# Vérifier les migrations
echo "Vérification des migrations:"
python3 manage.py showmigrations
echo ""

echo "=== Vérification terminée ==="
```

Exécutez:
```bash
chmod +x check_compatibility.sh
./check_compatibility.sh
```

---

## Support

Si vous avez des questions ou des problèmes:

1. Vérifiez les logs d'erreur
2. Testez localement d'abord
3. Contactez le support de votre hébergeur
4. Consultez la documentation Django: https://docs.djangoproject.com/en/4.2/

---

## Checklist de décision

- [ ] J'ai vérifié la version Python sur mon serveur
- [ ] J'ai choisi ma solution (Django 4.2 / Python 3.9+ / Changer d'hébergeur)
- [ ] J'ai testé localement avec la nouvelle configuration
- [ ] J'ai mis à jour requirements.txt
- [ ] J'ai vérifié que toutes les migrations fonctionnent
- [ ] Je suis prêt pour le déploiement

---

**Note importante**: Django 4.2 LTS est la version recommandée pour la production. Elle est stable, bien testée, et supportée jusqu'en avril 2026.
