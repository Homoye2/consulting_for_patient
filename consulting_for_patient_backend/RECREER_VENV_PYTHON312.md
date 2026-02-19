# Recréer le venv avec Python 3.12.12

## Problème identifié

Votre venv utilise Python 3.6.8 au lieu de Python 3.12.12:

```bash
(venv) [onglsmjm@server305 backend]$ python3 --version
Python 3.6.8  # ❌ Mauvaise version dans le venv

# Mais Python 3.12.12 est disponible:
(venv) [onglsmjm@server305 backend]$ /opt/alt/python312/bin/python3.12 --version
Python 3.12.12  # ✅ Version correcte disponible
```

**Conséquence:** Django 5.2 ne peut pas fonctionner avec Python 3.6.8 (nécessite Python 3.10+)

---

## Solution: Recréer le venv avec Python 3.12.12

### Étape 1: Désactiver et sauvegarder l'ancien venv

```bash
# Désactiver le venv actuel
deactivate

# Aller dans le répertoire backend
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/

# Sauvegarder l'ancien venv (au cas où)
mv venv venv_old_python36

# Vérifier
ls -la
# Vous devriez voir: venv_old_python36/
```

---

### Étape 2: Créer un nouveau venv avec Python 3.12.12

```bash
# Créer le nouveau venv avec Python 3.12
/opt/alt/python312/bin/python3.12 -m venv venv

# Vérifier que le venv a été créé
ls -la venv/

# Activer le nouveau venv
source venv/bin/activate

# Vérifier la version Python (IMPORTANT!)
python3 --version
# Devrait afficher: Python 3.12.12 ✅

# Si "python" ne fonctionne pas, créer un lien symbolique
cd venv/bin/
ln -s python3 python
cd ../..

# Vérifier à nouveau
python --version
# Devrait afficher: Python 3.12.12 ✅
```

---

### Étape 3: Mettre à jour pip

```bash
# Toujours dans le venv activé
python -m pip install --upgrade pip

# Vérifier pip
pip --version
# Devrait afficher: pip XX.X.X (python 3.12)
```

---

### Étape 4: Installer les dépendances Django 5.2

```bash
# Option A: Si vous avez requirements.txt
pip install -r requirements.txt

# Option B: Installation manuelle des packages principaux
pip install Django==5.2.8
pip install djangorestframework==3.14.0
pip install djangorestframework-simplejwt==5.3.0
pip install django-cors-headers==4.3.0
pip install django-filter==23.0
pip install drf-yasg==1.21.7
pip install Pillow==10.0.0
pip install google-auth==2.23.0
pip install requests==2.31.0
pip install mysqlclient==2.2.0
pip install faker==20.1.0
pip install mysql-connector-python==8.0.0
pip install python-dotenv==1.0.0
pip install qrcode==7.4.2
pip install psutil==5.9.8
pip install gunicorn==21.2.0
pip install pytz==2023.3

# Vérifier l'installation
pip list | grep -i django
```

---

### Étape 5: Vérifier que Django fonctionne

```bash
# Toujours dans le venv
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/

# Vérifier Django
python -c "import django; print(f'Django {django.get_version()} avec Python {django.VERSION}')"

# Vérifier la configuration
python manage.py check

# Si tout est OK, vous devriez voir:
# System check identified no issues (0 silenced).
```

---

### Étape 6: Mettre à jour passenger_wsgi.py

Le fichier doit pointer vers le nouveau venv:

```bash
nano passenger_wsgi.py
```

**Vérifiez que cette ligne est correcte:**

```python
INTERP = os.path.join(project_home, 'venv', 'bin', 'python3')
```

Le fichier complet:

```python
import os
import sys
from pathlib import Path

project_home = '/home/onglsmjm/e_sora.onglalumiere.org/backend'
INTERP = os.path.join(project_home, 'venv', 'bin', 'python3')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

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
```

Sauvegarder: `Ctrl+O`, `Enter`, `Ctrl+X`

---

### Étape 7: Mettre à jour .htaccess

Vérifiez que le .htaccess pointe vers le bon venv:

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/
nano .htaccess
```

**Vérifiez cette ligne:**

```apache
PassengerPython /home/onglsmjm/e_sora.onglalumiere.org/backend/venv/bin/python3
```

---

### Étape 8: Collecter les fichiers statiques

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
source venv/bin/activate
python manage.py collectstatic --noinput
```

---

### Étape 9: Redémarrer l'application

```bash
# Créer le fichier restart
mkdir -p tmp
touch tmp/restart.txt

# Ou via cPanel: Setup Python App → Restart
```

---

### Étape 10: Vérifier que tout fonctionne

```bash
# Vérifier le venv
source venv/bin/activate
python --version
# Doit afficher: Python 3.12.12 ✅

python -c "import django; print(django.get_version())"
# Doit afficher: 5.2.8 ✅

# Vérifier Django
python manage.py check
# Doit afficher: System check identified no issues

deactivate
```

---

### Étape 11: Tester via navigateur

Visitez: `https://e-sora.onglalumiere.org/api/`

Si vous voyez une erreur, vérifiez les logs:

```bash
tail -50 ~/logs/e-sora.onglalumiere.org-error_log
cat /home/onglsmjm/e_sora.onglalumiere.org/backend/passenger_error.log
```

---

## Commandes complètes (copier-coller)

```bash
# 1. Désactiver et sauvegarder l'ancien venv
deactivate
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
mv venv venv_old_python36

# 2. Créer nouveau venv avec Python 3.12
/opt/alt/python312/bin/python3.12 -m venv venv

# 3. Activer et vérifier
source venv/bin/activate
python3 --version  # Doit afficher: Python 3.12.12

# 4. Créer lien symbolique python → python3
cd venv/bin/
ln -s python3 python
cd ../..

# 5. Mettre à jour pip
python -m pip install --upgrade pip

# 6. Installer Django et dépendances
pip install Django==5.2.8 djangorestframework==3.14.0 djangorestframework-simplejwt==5.3.0 django-cors-headers==4.3.0 django-filter==23.0 drf-yasg==1.21.7 Pillow==10.0.0 google-auth==2.23.0 requests==2.31.0 mysqlclient==2.2.0 faker==20.1.0 mysql-connector-python==8.0.0 python-dotenv==1.0.0 qrcode==7.4.2 psutil==5.9.8 gunicorn==21.2.0 pytz==2023.3

# 7. Vérifier Django
python -c "import django; print(f'Django {django.get_version()}')"
python manage.py check

# 8. Collecter statiques
python manage.py collectstatic --noinput

# 9. Redémarrer
mkdir -p tmp
touch tmp/restart.txt

# 10. Vérifier les logs
tail -20 ~/logs/e-sora.onglalumiere.org-error_log
```

---

## Vérification finale

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
source venv/bin/activate

echo "=== Vérification Python ==="
python --version
python3 --version

echo ""
echo "=== Vérification Django ==="
python -c "import django; print(f'Django version: {django.get_version()}')"

echo ""
echo "=== Vérification modules ==="
python -c "import rest_framework; print('✅ DRF installé')"
python -c "import MySQLdb; print('✅ mysqlclient installé')"
python -c "import PIL; print('✅ Pillow installé')"

echo ""
echo "=== Vérification Django ==="
python manage.py check

deactivate
```

---

## Supprimer l'ancien venv (optionnel)

Une fois que tout fonctionne:

```bash
cd /home/onglsmjm/e_sora.onglalumiere.org/backend/
rm -rf venv_old_python36
```

---

## Checklist

- [ ] Ancien venv désactivé et renommé
- [ ] Nouveau venv créé avec `/opt/alt/python312/bin/python3.12`
- [ ] Venv activé et Python 3.12.12 confirmé
- [ ] Lien symbolique `python` → `python3` créé
- [ ] pip mis à jour
- [ ] Django 5.2.8 et dépendances installées
- [ ] `python manage.py check` réussi
- [ ] Fichiers statiques collectés
- [ ] Application redémarrée
- [ ] Site accessible via navigateur

---

## Erreurs possibles

### Erreur: "No module named 'MySQLdb'"

```bash
source venv/bin/activate
pip install mysqlclient
deactivate
touch tmp/restart.txt
```

### Erreur: "No module named 'PIL'"

```bash
source venv/bin/activate
pip install Pillow
deactivate
touch tmp/restart.txt
```

### Erreur: "command 'gcc' failed"

Si l'installation de mysqlclient échoue:

```bash
# Installer les headers MySQL (demander au support cPanel)
# Ou utiliser mysql-connector-python à la place:
pip uninstall mysqlclient
pip install mysql-connector-python
```

Puis dans `mysite/settings.py`, changez:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',  # Au lieu de django.db.backends.mysql
        # ... reste de la config
    }
}
```

---

**Temps estimé:** 10-15 minutes

**Note importante:** Après avoir recréé le venv, l'application devrait fonctionner correctement avec Django 5.2 et Python 3.12.12.
