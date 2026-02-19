# Guide de Déploiement Django sur cPanel

Ce guide vous accompagne étape par étape pour déployer votre application Django (consulting_for_patient_backend) sur un serveur cPanel.

## Prérequis

- Accès cPanel avec SSH activé
- Python 3.6+ disponible sur le serveur (3.6.8 confirmé sur votre serveur)
- MySQL/MariaDB disponible
- Nom de domaine configuré (ex: api.votredomaine.com)

## ⚠️ IMPORTANT - Version Python

Votre serveur a **Python 3.6.8**. Django 5.2 nécessite Python 3.10+.

**Solution recommandée**: Utilisez `requirements_python36.txt` qui installe Django 4.2 LTS (compatible Python 3.6.8).

Voir le fichier `INSTALLER_PYTHON_CPANEL.md` pour plus de détails sur les options disponibles.

---

## Étape 1: Préparation de l'environnement local

### 1.1 Créer le fichier requirements.txt (si pas déjà fait)

```bash
cd consulting_for_patient_backend
pip freeze > requirements.txt
```

### 1.2 Préparer les fichiers de configuration

Créez un fichier `.env.production` avec vos variables d'environnement:

```env
pip install djangorestframework
```

---

## Étape 2: Configuration de la base de données MySQL

### 2.1 Créer la base de données via cPanel

1. Connectez-vous à cPanel
2. Allez dans **MySQL® Databases**
3. Créez une nouvelle base de données (ex: `cpanel_user_consulting`)
4. Créez un utilisateur MySQL avec un mot de passe fort
5. Associez l'utilisateur à la base de données avec tous les privilèges

### 2.2 Notez les informations de connexion

```
Nom de la base: cpanel_user_consulting
Utilisateur: cpanel_user_dbuser
Mot de passe: [votre mot de passe]
Hôte: localhost
```

---

## Étape 3: Connexion SSH et préparation du serveur

### 3.1 Se connecter en SSH

```bash
ssh votre_username@votredomaine.com
```

### 3.2 Vérifier la version de Python

```bash
python3 --version
# ou
python3.9 --version
python3.10 --version
```

### 3.3 Créer la structure de répertoires

```bash
cd ~
mkdir -p applications/consulting_backend
cd applications/consulting_backend
```

---

## Étape 4: Upload des fichiers

### Option A: Via Git (Recommandé)

```bash
# Sur le serveur
cd ~/applications/consulting_backend
git clone https://github.com/votre-repo/consulting_for_patient_backend.git .
```

### Option B: Via FTP/SFTP

1. Utilisez FileZilla ou un client SFTP
2. Uploadez tous les fichiers du projet dans `~/applications/consulting_backend/`
3. Excluez: `venv/`, `__pycache__/`, `.git/`, `*.pyc`, `media/` (si volumineux)

### Option C: Via cPanel File Manager

1. Compressez votre projet en `.zip` localement
2. Uploadez via cPanel File Manager
3. Extrayez dans `~/applications/consulting_backend/`

---

## Étape 5: Configuration de l'environnement virtuel Python

### 5.1 Créer l'environnement virtuel

```bash
cd ~/applications/consulting_backend
python3 -m venv venv
```

### 5.2 Activer l'environnement virtuel

```bash
source venv/bin/activate
```

### 5.3 Mettre à jour pip

```bash
pip install --upgrade pip
```

### 5.4 Installer les dépendances

**Pour Python 3.6.8 (votre cas):**

```bash
pip install -r requirements_python36.txt
```

**Pour Python 3.10+ (si disponible):**

```bash
pip install -r requirements.txt
```

Si vous rencontrez des erreurs, installez les paquets système nécessaires:

```bash
pip install mysqlclient
pip install gunicorn
pip install python-dotenv
```

---

## Étape 6: Configuration de Django pour la production

### 6.1 Modifier settings.py

Créez un fichier `mysite/settings_production.py`:

```python
from .settings import *
import os
from pathlib import Path

# SECURITY
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'changez-moi-en-production')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://votredomaine.com",
    "https://www.votredomaine.com",
]

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 6.2 Créer le fichier .env

```bash
cd ~/applications/consulting_backend
nano .env
```

Collez vos variables d'environnement:

```env
DEBUG=False
SECRET_KEY=votre-cle-secrete-generee-aleatoirement
ALLOWED_HOSTS=api.votredomaine.com,votredomaine.com
DATABASE_NAME=cpanel_user_consulting
DATABASE_USER=cpanel_user_dbuser
DATABASE_PASSWORD=votre_mot_de_passe_mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DJANGO_SETTINGS_MODULE=mysite.settings_production
```

Sauvegardez avec `Ctrl+O`, puis `Ctrl+X`

---

## Étape 7: Migrations et collecte des fichiers statiques

### 7.1 Exporter les variables d'environnement

```bash
export $(cat .env | xargs)
```

### 7.2 Exécuter les migrations

```bash
python manage.py migrate --settings=mysite.settings_production
```

### 7.3 Créer un superutilisateur

```bash
python manage.py createsuperuser --settings=mysite.settings_production
```

### 7.4 Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput --settings=mysite.settings_production
```

---

## Étape 8: Configuration de l'application Python dans cPanel

### 8.1 Accéder à "Setup Python App"

1. Connectez-vous à cPanel
2. Cherchez **"Setup Python App"** dans la section Software
3. Cliquez sur **"Create Application"**

### 8.2 Configurer l'application

Remplissez les champs:

- **Python version**: 3.6 (selon disponibilité dans cPanel)
- **Application root**: `applications/consulting_backend`
- **Application URL**: `api.votredomaine.com` ou `/api`
- **Application startup file**: `passenger_wsgi.py`
- **Application Entry point**: `application`

**Note**: Si cPanel propose Python 3.8+, utilisez la version la plus récente disponible.

Cliquez sur **"Create"**

---

## Étape 9: Créer le fichier passenger_wsgi.py

### 9.1 Créer le fichier

```bash
cd ~/applications/consulting_backend
nano passenger_wsgi.py
```

### 9.2 Contenu du fichier

```python
import os
import sys
from pathlib import Path

# Ajouter le répertoire du projet au path
INTERP = os.path.join(os.environ['HOME'], 'applications', 'consulting_backend', 'venv', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ajouter le projet au path
sys.path.insert(0, os.path.join(os.environ['HOME'], 'applications', 'consulting_backend'))

# Charger les variables d'environnement
from dotenv import load_dotenv
env_path = Path(os.environ['HOME']) / 'applications' / 'consulting_backend' / '.env'
load_dotenv(dotenv_path=env_path)

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings_production')

# Importer l'application WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Sauvegardez avec `Ctrl+O`, puis `Ctrl+X`

---

## Étape 10: Configuration du domaine/sous-domaine

### 10.1 Créer un sous-domaine (optionnel)

1. Dans cPanel, allez dans **Domains** ou **Subdomains**
2. Créez `api.votredomaine.com`
3. Pointez le document root vers: `applications/consulting_backend/public`

### 10.2 Créer le répertoire public

```bash
cd ~/applications/consulting_backend
mkdir -p public
```

### 10.3 Créer un fichier .htaccess

```bash
nano public/.htaccess
```

Contenu:

```apache
PassengerEnabled On
PassengerAppRoot /home/votre_username/applications/consulting_backend
PassengerPython /home/votre_username/applications/consulting_backend/venv/bin/python
PassengerStartupFile passenger_wsgi.py

# Redirection pour les fichiers statiques
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^static/(.*)$ /home/votre_username/applications/consulting_backend/staticfiles/$1 [L]
RewriteRule ^media/(.*)$ /home/votre_username/applications/consulting_backend/media/$1 [L]
```

---

## Étape 11: Configuration SSL (HTTPS)

### 11.1 Activer SSL via cPanel

1. Allez dans **SSL/TLS Status**
2. Sélectionnez votre domaine `api.votredomaine.com`
3. Cliquez sur **"Run AutoSSL"** (Let's Encrypt gratuit)

### 11.2 Forcer HTTPS

Dans `public/.htaccess`, ajoutez au début:

```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## Étape 12: Permissions et sécurité

### 12.1 Définir les permissions correctes

```bash
cd ~/applications/consulting_backend
chmod 755 passenger_wsgi.py
chmod -R 755 media/
chmod -R 755 staticfiles/
chmod 600 .env
```

### 12.2 Protéger les fichiers sensibles

Créez un fichier `public/.htaccess` pour bloquer l'accès:

```apache
<Files ".env">
    Order allow,deny
    Deny from all
</Files>

<Files "*.py">
    Order allow,deny
    Deny from all
</Files>
```

---

## Étape 13: Redémarrage de l'application

### 13.1 Via cPanel

1. Retournez dans **"Setup Python App"**
2. Cliquez sur **"Restart"** à côté de votre application

### 13.2 Via SSH (méthode alternative)

```bash
cd ~/applications/consulting_backend
touch tmp/restart.txt
```

---

## Étape 14: Tests et vérification

### 14.1 Tester l'API

```bash
curl https://api.votredomaine.com/api/
```

### 14.2 Vérifier les logs

```bash
tail -f ~/logs/api.votredomaine.com-error_log
```

### 14.3 Accéder à l'admin Django

Visitez: `https://api.votredomaine.com/admin/`

---

## Étape 15: Configuration des tâches CRON (optionnel)

Si vous avez des tâches planifiées:

### 15.1 Créer un script de tâche

```bash
nano ~/applications/consulting_backend/run_task.sh
```

Contenu:

```bash
#!/bin/bash
cd /home/votre_username/applications/consulting_backend
source venv/bin/activate
export $(cat .env | xargs)
python manage.py votre_commande --settings=mysite.settings_production
```

### 15.2 Ajouter au CRON

Dans cPanel, allez dans **Cron Jobs** et ajoutez:

```
0 2 * * * /home/votre_username/applications/consulting_backend/run_task.sh
```

---

## Dépannage

### Erreur 500 - Internal Server Error

1. Vérifiez les logs:
```bash
tail -f ~/logs/api.votredomaine.com-error_log
```

2. Vérifiez les permissions:
```bash
ls -la ~/applications/consulting_backend/
```

3. Testez manuellement:
```bash
cd ~/applications/consulting_backend
source venv/bin/activate
python passenger_wsgi.py
```

### Erreur de base de données

1. Vérifiez les credentials dans `.env`
2. Testez la connexion MySQL:
```bash
mysql -u votre_user -p -h localhost votre_database
```

### Fichiers statiques non chargés

1. Re-collectez les fichiers statiques:
```bash
python manage.py collectstatic --clear --noinput --settings=mysite.settings_production
```

2. Vérifiez les permissions:
```bash
chmod -R 755 staticfiles/
```

### L'application ne redémarre pas

1. Créez le fichier restart:
```bash
mkdir -p tmp
touch tmp/restart.txt
```

2. Redémarrez via cPanel Python App Manager

---

## Maintenance

### Mise à jour du code

```bash
cd ~/applications/consulting_backend
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=mysite.settings_production
python manage.py collectstatic --noinput --settings=mysite.settings_production
touch tmp/restart.txt
```

### Sauvegarde de la base de données

```bash
mysqldump -u votre_user -p votre_database > backup_$(date +%Y%m%d).sql
```

### Restauration de la base de données

```bash
mysql -u votre_user -p votre_database < backup_20260215.sql
```

---

## Checklist finale

- [ ] Base de données MySQL créée et configurée
- [ ] Fichiers uploadés sur le serveur
- [ ] Environnement virtuel créé et dépendances installées
- [ ] Fichier `.env` configuré avec les bonnes valeurs
- [ ] Migrations exécutées
- [ ] Fichiers statiques collectés
- [ ] `passenger_wsgi.py` créé et configuré
- [ ] Application Python configurée dans cPanel
- [ ] Domaine/sous-domaine configuré
- [ ] SSL activé (HTTPS)
- [ ] Permissions correctes définies
- [ ] Application redémarrée
- [ ] Tests effectués (API accessible)
- [ ] Admin Django accessible

---

## Support et ressources

- Documentation Django: https://docs.djangoproject.com/
- Documentation cPanel: https://docs.cpanel.net/
- Passenger (serveur WSGI): https://www.phusionpassenger.com/

---

**Note importante**: Remplacez tous les `votre_username`, `votredomaine.com`, et autres valeurs d'exemple par vos vraies valeurs.

**Sécurité**: Ne partagez jamais votre fichier `.env` ou vos credentials de base de données. Utilisez des mots de passe forts et uniques.
