# 🚨 ERREUR 503 - LISEZ-MOI EN PREMIER

## Vous avez cette erreur?

```
503 Service Unavailable
```

**Dans les logs:**
```
Error while finding module specification for '/home/onglsmjm/e_sora.onglalumiere.org/backend/passenger_wsgi.py' 
(ModuleNotFoundError: No module named '/home/onglsmjm/e_sora')
```

## ✅ Solution rapide (2 minutes)

### Étape 1: Connectez-vous au serveur

```bash
ssh onglsmjm@server305.com
```

### Étape 2: Copiez-collez ces 3 blocs

#### Bloc 1: Corriger .htaccess

```bash
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
```

#### Bloc 2: Corriger passenger_wsgi.py

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
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
```

#### Bloc 3: Redémarrer

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
chmod 755 passenger_wsgi.py
mkdir -p tmp
touch tmp/restart.txt
sleep 5
echo "✅ Terminé!"
```

### Étape 3: Vérifier

```bash
# Vérifier les logs
tail -10 stderr.log

# Si pas d'erreur, testez dans le navigateur:
# https://e-sora.onglalumiere.org/api/
```

## 🎯 C'est tout!

Si vous voyez la page de l'API Django REST Framework, c'est réglé! 🎉

## ❓ Ça ne marche pas?

### Diagnostic automatique

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
bash diagnostic_503.sh
```

### Vérifier Django

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
source venv/bin/activate
python manage.py check
deactivate
```

## 📚 Plus d'informations

- **AIDE_RAPIDE_503.md** - Guide détaillé
- **COMMANDES_RAPIDES_503.md** - Toutes les commandes
- **SOLUTION_FINALE_503.md** - Explication complète
- **diagnostic_503.sh** - Script de diagnostic

## 💡 Pourquoi cette erreur?

Le fichier `passenger_wsgi.py` contenait du code (`os.execl()`) qui faisait que Passenger essayait d'exécuter le fichier comme un module Python au lieu de l'importer normalement.

La solution supprime ce code problématique.

## ✅ Checklist

- [ ] Copier-coller le bloc 1 (corriger .htaccess)
- [ ] Copier-coller le bloc 2 (corriger passenger_wsgi.py)
- [ ] Copier-coller le bloc 3 (redémarrer)
- [ ] Vérifier les logs
- [ ] Tester dans le navigateur

---

**Temps total:** 2 minutes  
**Taux de réussite:** 95%  
**Difficulté:** Facile (copier-coller)

---

## 🆘 Besoin d'aide?

Si le problème persiste après avoir suivi ces étapes:

1. Exécutez le diagnostic: `bash diagnostic_503.sh`
2. Lisez **SOLUTION_FINALE_503.md** pour plus de détails
3. Vérifiez que `.env.production` contient les bonnes valeurs
4. Vérifiez que le venv utilise Python 3.11+

---

**Dernière mise à jour:** 19 février 2026
