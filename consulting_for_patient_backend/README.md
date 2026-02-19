# Système de Gestion Hospitalière Multi-Tenant

Application Django REST API pour la gestion d'un système hospitalier multi-tenant avec focus sur la planification familiale.

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- MySQL 8.0+
- pip

### Configuration MySQL
```bash
# 1. Installer et configurer MySQL
# macOS
brew install mysql
brew services start mysql

# Ubuntu
sudo apt install mysql-server
sudo systemctl start mysql

# 2. Configuration automatique
python setup_mysql.py
```

### Installation des dépendances
```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration de la base de données
```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Seeder avec données de test
python seed_database.py
```

### Lancement du serveur
```bash
python manage.py runserver
```

## 📊 Base de Données

### Migration vers MySQL
Ce projet utilise maintenant MySQL au lieu de SQLite pour de meilleures performances et une meilleure scalabilité.

Voir [MIGRATION_MYSQL.md](MIGRATION_MYSQL.md) pour le guide complet de migration.

### Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'e_sora',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '8888',
    }
}
```

## 🔑 Comptes de Test

Le seeder crée automatiquement des comptes de test :

- **Super Admin**: `admin@system.sn` / `admin123`
- **Admin Hôpital**: `admin.abassndao@hopital.sn` / `admin123`  
- **Spécialiste**: `dr.aissatou.diallo@hopital.sn` / `doc123`
- **Pharmacien**: `abdou.diouf@pharma.sn` / `pharma123`
- **Patients**: Emails générés / `patient123`

## 📚 Documentation

- [Documentation API Complète](API_COMPLETE_DOCUMENTATION.md) - Guide complet de toutes les APIs
- [Guide de Migration MySQL](MIGRATION_MYSQL.md) - Migration de SQLite vers MySQL
- [Documentation Swagger](http://localhost:8000/swagger/) - Interface interactive

## 🛠️ Scripts Utiles

### Gestionnaire de base de données
```bash
python manage_db.py
```
Menu interactif pour :
- Afficher les statistiques
- Créer des sauvegardes
- Vérifier la santé de la DB
- Relancer le seeder

### Seeder personnalisé
```bash
python seed_database.py
```
Crée des données réalistes :
- 70+ utilisateurs (tous rôles)
- 3 hôpitaux avec spécialistes
- 50 patients avec historique
- 100 rendez-vous
- 50 consultations
- 30 commandes pharmacie
- Stocks et produits

## 🏗️ Architecture

### Modèles Principaux
- **User** - Système d'authentification multi-rôles
- **Hopital** - Gestion des établissements
- **Specialiste** - Médecins et leurs spécialités
- **Patient** - Profils patients
- **RendezVous** - Système de rendez-vous
- **ConsultationPF** - Consultations planification familiale
- **Pharmacie** - Gestion des pharmacies
- **CommandePharmacie** - Commandes et livraisons

### Rôles Utilisateurs
- `super_admin` - Accès complet système
- `admin_hopital` - Gestion d'un hôpital
- `specialiste` - Médecin spécialiste
- `pharmacien` - Gestion pharmacie
- `agent_enregistrement` - Saisie données
- `patient` - Accès patient

## 🔐 Sécurité

- Authentification JWT
- Permissions basées sur les rôles
- Validation des données
- Protection CORS configurée
- Hashage sécurisé des mots de passe

## 📈 Fonctionnalités

### Gestion Hospitalière
- Multi-tenant (plusieurs hôpitaux)
- Gestion des spécialistes et disponibilités
- Système de rendez-vous intelligent
- Consultations et rapports médicaux

### Planification Familiale
- Méthodes contraceptives
- Suivi des consultations PF
- Prescriptions et recommandations
- Statistiques et rapports

### Pharmacie
- Gestion des stocks
- Commandes en ligne
- Suivi des livraisons
- Alertes de rupture

### Système de Notifications
- Notifications temps réel
- Rappels de rendez-vous
- Alertes de stock
- Communications patient-médecin

## 🧪 Tests

```bash
# Lancer les tests
python manage.py test

# Tests avec couverture
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📱 API REST

### Endpoints Principaux
- `/api/auth/` - Authentification
- `/api/users/` - Gestion utilisateurs
- `/api/patients/` - Gestion patients
- `/api/hopitaux/` - Gestion hôpitaux
- `/api/specialistes/` - Gestion spécialistes
- `/api/rendez-vous/` - Gestion rendez-vous
- `/api/consultations/` - Consultations PF
- `/api/pharmacies/` - Gestion pharmacies
- `/api/commandes-pharmacie/` - Commandes

### Documentation Interactive
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## 🔧 Maintenance

### Sauvegarde
```bash
# Sauvegarde manuelle
mysqldump -P 8888 -u root -p e_sora > backup.sql

# Restauration
mysql -P 8888 -u root -p e_sora < backup.sql
```

### Monitoring
```bash
# Statistiques de la DB
python manage_db.py

# Logs Django
tail -f logs/django.log
```

## 🚀 Déploiement

### Variables d'environnement
```env
DEBUG=False
SECRET_KEY=your-secret-key
DB_NAME=e_sora
DB_USER=e_sora_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=8888
```

### Production
- Utiliser un serveur WSGI (Gunicorn)
- Configurer un reverse proxy (Nginx)
- Activer HTTPS
- Configurer les logs
- Mettre en place la surveillance

## 📞 Support

Pour toute question ou problème :
1. Consultez la documentation
2. Vérifiez les logs
3. Utilisez le script de diagnostic : `python manage_db.py`

## 📄 Licence

Ce projet est sous licence MIT.

