# Migration de SQLite vers MySQL

Ce guide vous accompagne dans la migration de la base de données SQLite vers MySQL.

## 📋 Prérequis

### 1. Installation de MySQL
```bash
# macOS avec Homebrew
brew install mysql
brew services start mysql

# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql

# Windows
# Téléchargez MySQL depuis https://dev.mysql.com/downloads/mysql/
```

### 2. Configuration initiale de MySQL
```bash
# Sécuriser l'installation MySQL
sudo mysql_secure_installation

# Se connecter à MySQL
mysql -u root -p
```

### 3. Dépendances Python
```bash
# Installer le client MySQL pour Python
pip install mysqlclient

# Alternative si mysqlclient pose problème
pip install PyMySQL
```

## 🚀 Processus de Migration

### Étape 1: Configuration automatique
```bash
# Lancer le script de configuration
python setup_mysql.py
```

### Étape 2: Configuration manuelle (si nécessaire)

#### Créer la base de données manuellement
```sql
-- Se connecter à MySQL
mysql -u root -p

-- Créer la base de données
CREATE DATABASE e_sora CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Créer un utilisateur dédié (optionnel)
CREATE USER 'e_sora_user'@'localhost' IDENTIFIED BY 'e_sora_password';
GRANT ALL PRIVILEGES ON e_sora.* TO 'e_sora_user'@'localhost';
FLUSH PRIVILEGES;

-- Quitter MySQL
EXIT;
```

#### Modifier settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'e_sora',
        'USER': 'root',  # ou 'e_sora_user'
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '8888',  # Port MAMP/XAMPP
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### Étape 3: Migrations Django
```bash
# Supprimer les anciens fichiers de migration (optionnel)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Créer de nouvelles migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### Étape 4: Seeding des données
```bash
# Lancer le seeder complet
python seed_database.py
```

## 🔧 Configuration Avancée

### Optimisation MySQL pour Django
Ajoutez ces paramètres dans votre fichier MySQL (`my.cnf` ou `my.ini`):

```ini
[mysqld]
# Optimisations pour Django
innodb_file_per_table = 1
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
innodb_flush_log_at_trx_commit = 2
innodb_thread_concurrency = 8

# Encodage
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Connexions
max_connections = 200
wait_timeout = 28800
interactive_timeout = 28800
```

### Variables d'environnement (recommandé)
Créez un fichier `.env` :
```env
DB_NAME=e_sora
DB_USER=e_sora_user
DB_PASSWORD=e_sora_password
DB_HOST=localhost
DB_PORT=8888
```

Puis modifiez `settings.py` :
```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## 📊 Données de Test

Le seeder crée automatiquement :

### Utilisateurs de test
- **Super Admin**: `admin@system.sn` / `admin123`
- **Admin Hôpital**: `admin.abassndao@hopital.sn` / `admin123`
- **Spécialiste**: `dr.aissatou.diallo@hopital.sn` / `doc123`
- **Pharmacien**: `abdou.diouf@pharma.sn` / `pharma123`
- **Patients**: Emails générés automatiquement / `patient123`

### Données créées
- 70+ utilisateurs (admins, spécialistes, pharmaciens, patients)
- 3 hôpitaux avec leurs spécialistes
- 8 spécialités médicales
- 14 méthodes contraceptives
- 5 pharmacies avec stocks
- 100 rendez-vous
- 50 consultations
- 30 commandes de pharmacie
- 50 notifications
- Contenu de la landing page

## 🔍 Vérification

### Vérifier la connexion
```bash
python manage.py dbshell
```

### Vérifier les données
```bash
python manage.py shell
```

```python
from pf.models import User, Patient, Hopital, Specialiste
print(f"Utilisateurs: {User.objects.count()}")
print(f"Patients: {Patient.objects.count()}")
print(f"Hôpitaux: {Hopital.objects.count()}")
print(f"Spécialistes: {Specialiste.objects.count()}")
```

### Tester l'API
```bash
# Démarrer le serveur
python manage.py runserver

# Tester la connexion
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@system.sn", "password": "admin123"}'
```

## 🚨 Dépannage

### Erreur de connexion MySQL
```bash
# Vérifier que MySQL fonctionne
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS

# Redémarrer MySQL
sudo systemctl restart mysql  # Linux
brew services restart mysql  # macOS
```

### Erreur mysqlclient
```bash
# Sur macOS
brew install mysql-client
export PATH="/usr/local/opt/mysql-client/bin:$PATH"

# Sur Ubuntu
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# Alternative: utiliser PyMySQL
pip install PyMySQL
```

Puis ajoutez dans `settings.py` :
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Erreur d'encodage
Assurez-vous que votre base MySQL utilise `utf8mb4` :
```sql
ALTER DATABASE e_sora CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Problème de permissions
```sql
GRANT ALL PRIVILEGES ON e_sora.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

## 📈 Performance

### Index recommandés
Le seeder crée automatiquement les index définis dans les modèles Django. Pour des performances optimales, surveillez les requêtes lentes :

```sql
-- Activer le log des requêtes lentes
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
```

### Monitoring
```sql
-- Vérifier les performances
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Slow_queries';
```

## 🔄 Sauvegarde

### Sauvegarde automatique
```bash
# Créer un dump de la base
mysqldump -P 8888 -u root -p e_sora > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurer depuis un dump
mysql -P 8888 -u root -p e_sora < backup_file.sql
```

### Script de sauvegarde
```bash
#!/bin/bash
# backup_db.sh
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -P 8888 -u root -p e_sora > "backups/backup_$DATE.sql"
echo "Sauvegarde créée: backup_$DATE.sql"
```

## ✅ Checklist de Migration

- [ ] MySQL installé et configuré
- [ ] Base de données créée
- [ ] Dépendances Python installées
- [ ] Configuration Django mise à jour
- [ ] Migrations exécutées
- [ ] Seeder lancé avec succès
- [ ] Tests de connexion réussis
- [ ] API fonctionnelle
- [ ] Sauvegarde configurée

La migration est maintenant terminée ! Votre application utilise MySQL avec des données de test complètes.