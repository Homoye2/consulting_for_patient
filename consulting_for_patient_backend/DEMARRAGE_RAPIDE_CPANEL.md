# Démarrage Rapide - Déploiement sur cPanel

Guide condensé pour déployer rapidement votre backend Django sur cPanel avec Python 3.6.8.

---

## Étape 1: Préparer les fichiers (Local)

```bash
cd consulting_for_patient_backend

# Exporter la base de données (déjà fait)
# Fichiers disponibles: e_sora_export.sql et e_sora_export.sql.gz

# Créer un fichier .env.production
cat > .env.production << EOF
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=api.votredomaine.com,votredomaine.com
DATABASE_NAME=votre_db_name
DATABASE_USER=votre_db_user
DATABASE_PASSWORD=votre_db_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
DJANGO_SETTINGS_MODULE=mysite.settings
EOF
```

---

## Étape 2: Créer la base de données MySQL (cPanel)

1. Connexion cPanel → **MySQL® Databases**
2. Créer base: `cpanel_user_esora` (utf8mb4_unicode_ci)
3. Créer utilisateur avec mot de passe fort
4. Associer utilisateur à la base (tous privilèges)
5. Noter les credentials

---

## Étape 3: Importer la base de données (phpMyAdmin)

1. cPanel → **phpMyAdmin**
2. Sélectionner la base `cpanel_user_esora`
3. Onglet **Importer**
4. Choisir `e_sora_export.sql.gz`
5. Cliquer **Exécuter**
6. Vérifier: ~30 tables créées

---

## Étape 4: Uploader les fichiers (SSH ou FTP)

### Via SSH (Recommandé):

```bash
# Sur votre machine locale
cd consulting_for_patient_backend
tar -czf backend.tar.gz --exclude='venv' --exclude='__pycache__' --exclude='.git' --exclude='*.pyc' .

# Uploader via SCP
scp backend.tar.gz onglsmjm@server305.com:~/

# Se connecter au serveur
ssh onglsmjm@server305.com

# Extraire
mkdir -p ~/applications/consulting_backend
cd ~/applications/consulting_backend
tar -xzf ~/backend.tar.gz
rm ~/backend.tar.gz
```

### Via FTP:
Utilisez FileZilla pour uploader tous les fichiers dans `~/applications/consulting_backend/`

---

## Étape 5: Configurer l'environnement Python (SSH)

```bash
ssh onglsmjm@server305.com
cd ~/applications/consulting_backend

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances (Python 3.6.8)
pip install --upgrade pip
pip install -r requirements_python36.txt
```

---

## Étape 6: Configurer Django

```bash
# Créer le fichier .env
nano .env
```

Coller:
```env
DEBUG=False
SECRET_KEY=votre-cle-secrete-aleatoire-tres-longue
ALLOWED_HOSTS=api.votredomaine.com,votredomaine.com
DATABASE_NAME=cpanel_user_esora
DATABASE_USER=cpanel_user_dbuser
DATABASE_PASSWORD=votre_mot_de_passe_mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

Sauvegarder: `Ctrl+O`, `Enter`, `Ctrl+X`

```bash
# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser
```

---

## Étape 7: Créer passenger_wsgi.py

```bash
nano passenger_wsgi.py
```

Coller:
```python
import os
import sys
from pathlib import Path

# Python interpreter
INTERP = os.path.join(os.environ['HOME'], 'applications', 'consulting_backend', 'venv', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add project to path
sys.path.insert(0, os.path.join(os.environ['HOME'], 'applications', 'consulting_backend'))

# Load environment variables
from dotenv import load_dotenv
env_path = Path(os.environ['HOME']) / 'applications' / 'consulting_backend' / '.env'
load_dotenv(dotenv_path=env_path)

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Sauvegarder: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## Étape 8: Configurer cPanel Python App

1. cPanel → **Setup Python App**
2. **Create Application**:
   - Python version: **3.6**
   - Application root: `applications/consulting_backend`
   - Application URL: `api.votredomaine.com`
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`
3. Cliquer **Create**

---

## Étape 9: Configurer le domaine

### Créer sous-domaine:
1. cPanel → **Domains** ou **Subdomains**
2. Créer: `api.votredomaine.com`
3. Document Root: `applications/consulting_backend/public`

### Créer répertoire public et .htaccess:

```bash
cd ~/applications/consulting_backend
mkdir -p public
nano public/.htaccess
```

Coller:
```apache
PassengerEnabled On
PassengerAppRoot /home/onglsmjm/applications/consulting_backend
PassengerPython /home/onglsmjm/applications/consulting_backend/venv/bin/python
PassengerStartupFile passenger_wsgi.py

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^static/(.*)$ /home/onglsmjm/applications/consulting_backend/staticfiles/$1 [L]
RewriteRule ^media/(.*)$ /home/onglsmjm/applications/consulting_backend/media/$1 [L]
```

Sauvegarder et définir permissions:
```bash
chmod 755 passenger_wsgi.py
chmod 755 public/.htaccess
chmod -R 755 media/
chmod -R 755 staticfiles/
chmod 600 .env
```

---

## Étape 10: Activer SSL

1. cPanel → **SSL/TLS Status**
2. Sélectionner `api.votredomaine.com`
3. **Run AutoSSL** (Let's Encrypt gratuit)

---

## Étape 11: Redémarrer l'application

```bash
cd ~/applications/consulting_backend
mkdir -p tmp
touch tmp/restart.txt
```

Ou via cPanel → **Setup Python App** → **Restart**

---

## Étape 12: Tester

```bash
# Test API
curl https://api.votredomaine.com/api/

# Vérifier logs
tail -f ~/logs/api.votredomaine.com-error_log
```

Accéder à l'admin: `https://api.votredomaine.com/admin/`

---

## Dépannage rapide

### Erreur 500:
```bash
tail -f ~/logs/api.votredomaine.com-error_log
```

### Erreur base de données:
```bash
mysql -u votre_user -p votre_database -e "SHOW TABLES;"
```

### Redémarrer:
```bash
touch ~/applications/consulting_backend/tmp/restart.txt
```

### Permissions:
```bash
cd ~/applications/consulting_backend
chmod 755 passenger_wsgi.py
chmod -R 755 media/ staticfiles/
chmod 600 .env
```

---

## Mise à jour du code

```bash
cd ~/applications/consulting_backend
source venv/bin/activate

# Si vous utilisez Git
git pull origin main

# Ou re-uploader les fichiers modifiés via FTP

# Installer nouvelles dépendances
pip install -r requirements_python36.txt

# Migrations
python manage.py migrate

# Collecter statiques
python manage.py collectstatic --noinput

# Redémarrer
touch tmp/restart.txt
```

---

## Checklist

- [ ] Base de données MySQL créée
- [ ] Base de données importée (30+ tables)
- [ ] Fichiers uploadés sur serveur
- [ ] Environnement virtuel créé
- [ ] Dépendances installées (requirements_python36.txt)
- [ ] Fichier .env configuré
- [ ] Fichiers statiques collectés
- [ ] passenger_wsgi.py créé
- [ ] Python App configurée dans cPanel
- [ ] Sous-domaine créé
- [ ] Répertoire public et .htaccess créés
- [ ] SSL activé
- [ ] Permissions définies
- [ ] Application redémarrée
- [ ] API testée et fonctionnelle

---

## Commandes utiles

```bash
# Activer environnement
source ~/applications/consulting_backend/venv/bin/activate

# Voir logs
tail -f ~/logs/api.votredomaine.com-error_log

# Redémarrer app
touch ~/applications/consulting_backend/tmp/restart.txt

# Test connexion DB
mysql -u votre_user -p votre_database

# Migrations Django
python manage.py migrate

# Créer superuser
python manage.py createsuperuser

# Shell Django
python manage.py shell

# Backup DB
mysqldump -u votre_user -p votre_database > backup_$(date +%Y%m%d).sql
```

---

**Temps estimé**: 30-45 minutes

**Support**: Voir `DEPLOIEMENT_CPANEL.md` pour le guide détaillé et `INSTALLER_PYTHON_CPANEL.md` pour les options Python.
