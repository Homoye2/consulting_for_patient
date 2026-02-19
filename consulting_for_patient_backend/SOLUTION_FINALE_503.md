# Solution finale pour l'erreur 503

## Problème identifié

```
Error while finding module specification for '/home/onglsmjm/e_sora.onglalumiere.org/backend/passenger_wsgi.py' 
(ModuleNotFoundError: No module named '/home/onglsmjm/e_sora')
```

**Cause:** Passenger essaie d'exécuter `passenger_wsgi.py` comme un module Python (`-m`) au lieu de l'exécuter directement.

**Solution:** Corriger la configuration `.htaccess` et `passenger_wsgi.py`.

---

## Solution immédiate

### Étape 1: Corriger le .htaccess

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/
nano .htaccess
```

**Remplacez TOUT le contenu par:**

```apache
PassengerEnabled On
PassengerAppRoot /home/onglsmjm/e_sora.onglalumiere.org/backend
PassengerPython /home/onglsmjm/e_sora.onglalumiere.org/backend/venv/bin/python3
PassengerStartupFile passenger_wsgi.py
Options -Indexes

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    
    # Ne pas rediriger les fichiers statiques et media
    RewriteCond %{REQUEST_URI} ^/static/ [OR]
    RewriteCond %{REQUEST_URI} ^/media/
    RewriteRule ^ - [L]
    
    # Rediriger tout le reste vers l'application
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . - [L]
</IfModule>

# Alias pour les fichiers statiques
Alias /static /home/onglsmjm/e_sora.onglalumiere.org/backend/staticfiles
Alias /media /home/onglsmjm/e_sora.onglalumiere.org/backend/media

<Directory /home/onglsmjm/e_sora.onglalumiere.org/backend/staticfiles>
    Require all granted
    Options -Indexes
</Directory>

<Directory /home/onglsmjm/e_sora.onglalumiere.org/backend/media>
    Require all granted
    Options -Indexes
</Directory>

# Protéger les fichiers sensibles
<FilesMatch "\.(py|pyc|pyo|env|ini|log)$">
    Require all denied
</FilesMatch>

<Files ".env">
    Require all denied
</Files>

<Files ".env.production">
    Require all denied
</Files>

<Files "passenger_wsgi.py">
    Require all granted
</Files>
```

Sauvegarder: `Ctrl+O`, `Enter`, `Ctrl+X`

---

### Étape 2: Simplifier passenger_wsgi.py

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
nano passenger_wsgi.py
```

**Remplacez TOUT le contenu par cette version simplifiée:**

```python
import os
import sys

# Ajouter le répertoire du projet au path
project_home = '/home/onglsmjm/e_sora.onglalumiere.org/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Changer vers le répertoire du projet
os.chdir(project_home)

# Charger les variables d'environnement depuis .env.production
env_file = os.path.join(project_home, '.env.production')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Importer et démarrer l'application WSGI Django
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # Logger l'erreur
    import traceback
    error_log = os.path.join(project_home, 'passenger_error.log')
    with open(error_log, 'w') as f:
        f.write(f"Erreur de démarrage Django:\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Python executable: {sys.executable}\n")
        f.write(f"PYTHONPATH: {sys.path}\n\n")
        f.write(f"Erreur: {str(e)}\n\n")
        f.write(traceback.format_exc())
    
    # Re-raise pour que Passenger voie l'erreur
    raise
```

Sauvegarder: `Ctrl+O`, `Enter`, `Ctrl+X`

**Note:** J'ai supprimé la partie `os.execl()` qui causait le problème.

---

### Étape 3: Vérifier .env.production

```bash
nano .env.production
```

**Contenu minimum requis:**

```env
DEBUG=False
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
ALLOWED_HOSTS=e-sora.onglalumiere.org,www.e-sora.onglalumiere.org,162.0.215.194
DATABASE_NAME=votre_nom_base
DATABASE_USER=votre_user_mysql
DATABASE_PASSWORD=votre_mot_de_passe
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

**Important:** Vérifiez que `ALLOWED_HOSTS` contient votre domaine avec le tiret: `e-sora.onglalumiere.org`

---

### Étape 4: Définir les permissions

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/
chmod 755 .
chmod 644 .htaccess

cd backend/
chmod 755 .
chmod 755 passenger_wsgi.py
chmod -R 755 media staticfiles 2>/dev/null
chmod 600 .env.production 2>/dev/null
```

---

### Étape 5: Redémarrer l'application

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
mkdir -p tmp
touch tmp/restart.txt

# Attendre 5 secondes
sleep 5
```

---

### Étape 6: Vérifier les logs

```bash
# Vérifier stderr.log
tail -20 /home/onglsmjm/e_sora.onglalumiere.org/backend/stderr.log

# Vérifier passenger_error.log
cat /home/onglsmjm/e_sora.onglalumiere.org/backend/passenger_error.log 2>/dev/null

# Vérifier logs Apache
tail -20 ~/logs/e-sora.onglalumiere.org-error_log
```

---

### Étape 7: Tester dans le navigateur

Visitez: `https://e-sora.onglalumiere.org/api/`

---

## Commandes complètes (copier-coller)

```bash
# 1. Corriger .htaccess
cd /home/onglsmjm/e_sora.onglalumiere.org/
cat > .htaccess << 'EOF'
PassengerEnabled On
PassengerAppRoot /home/onglsmjm/e_sora.onglalumiere.org/backend
PassengerPython /home/onglsmjm/e_sora.onglalumiere.org/backend/venv/bin/python3
PassengerStartupFile passenger_wsgi.py
Options -Indexes

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteCond %{REQUEST_URI} ^/static/ [OR]
    RewriteCond %{REQUEST_URI} ^/media/
    RewriteRule ^ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . - [L]
</IfModule>

Alias /static /home/onglsmjm/e_sora.onglalumiere.org/backend/staticfiles
Alias /media /home/onglsmjm/e_sora.onglalumiere.org/backend/media

<Directory /home/onglsmjm/e_sora.onglalumiere.org/backend/staticfiles>
    Require all granted
    Options -Indexes
</Directory>

<Directory /home/onglsmjm/e_sora.onglalumiere.org/backend/media>
    Require all granted
    Options -Indexes
</Directory>

<FilesMatch "\.(py|pyc|pyo|env|ini|log)$">
    Require all denied
</FilesMatch>

<Files ".env">
    Require all denied
</Files>

<Files ".env.production">
    Require all denied
</Files>

<Files "passenger_wsgi.py">
    Require all granted
</Files>
EOF

# 2. Corriger passenger_wsgi.py
cd backend/
cat > passenger_wsgi.py << 'EOF'
import os
import sys

project_home = '/home/onglsmjm/e_sora.onglalumiere.org/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

env_file = os.path.join(project_home, '.env.production')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    import traceback
    error_log = os.path.join(project_home, 'passenger_error.log')
    with open(error_log, 'w') as f:
        f.write(f"Erreur de démarrage Django:\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Python executable: {sys.executable}\n")
        f.write(f"PYTHONPATH: {sys.path}\n\n")
        f.write(f"Erreur: {str(e)}\n\n")
        f.write(traceback.format_exc())
    raise
EOF

# 3. Permissions
cd /home/onglsmjm/e_sora.onglalumiere.org/
chmod 755 . && chmod 644 .htaccess
cd backend/
chmod 755 . passenger_wsgi.py
chmod -R 755 media staticfiles 2>/dev/null
chmod 600 .env.production 2>/dev/null

# 4. Redémarrer
mkdir -p tmp
touch tmp/restart.txt
sleep 5

# 5. Vérifier logs
echo "=== Vérification stderr.log ==="
tail -20 stderr.log 2>/dev/null || echo "Pas de stderr.log"
echo ""
echo "=== Vérification passenger_error.log ==="
cat passenger_error.log 2>/dev/null || echo "Pas de passenger_error.log"
echo ""
echo "=== Vérification logs Apache ==="
tail -20 ~/logs/e-sora.onglalumiere.org-error_log

echo ""
echo "✅ Configuration terminée!"
echo "Testez: https://e-sora.onglalumiere.org/api/"
```

---

## Si l'erreur persiste

### Vérifier que Django fonctionne manuellement

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
source venv/bin/activate

# Tester WSGI directement
python -c "
import os, sys
sys.path.insert(0, '/home/onglsmjm/e_sora.onglalumiere.org/backend')
os.chdir('/home/onglsmjm/e_sora.onglalumiere.org/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
print('✅ WSGI fonctionne!')
"

deactivate
```

---

## Alternative: Utiliser un sous-répertoire /api

Si le problème persiste, configurez l'application sur un sous-répertoire:

**Dans cPanel Python App:**
- Application URL: `e-sora.onglalumiere.org/api`

**Dans .htaccess:**
```apache
PassengerEnabled On
PassengerAppRoot /home/onglsmjm/e_sora.onglalumiere.org/backend
PassengerPython /home/onglsmjm/e_sora.onglalumiere.org/backend/venv/bin/python3
PassengerStartupFile passenger_wsgi.py
PassengerBaseURI /api
```

---

## Checklist finale

- [ ] `.htaccess` corrigé (sans `SetEnv PYTHONPATH`, sans `os.execl()`)
- [ ] `passenger_wsgi.py` simplifié
- [ ] `.env.production` avec `ALLOWED_HOSTS` correct
- [ ] Permissions correctes
- [ ] Application redémarrée
- [ ] Logs vérifiés (pas d'erreur ModuleNotFoundError)
- [ ] Site accessible

---

**Note:** Le problème venait de `os.execl()` dans `passenger_wsgi.py` qui faisait que Passenger essayait d'exécuter le fichier comme un module Python au lieu de l'importer normalement.
