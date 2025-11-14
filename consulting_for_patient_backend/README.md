# Application de Gestion de Planification Familiale

Application web complète pour la gestion de la planification familiale au Centre Hospitalier Abass Ndao.

## Stack Technique

- **Backend:** Django 5.2.8 + Django REST Framework
- **Authentification:** JWT (SimpleJWT)
- **Base de données:** SQLite (développement) / PostgreSQL (production)
- **Frontend:** React + Vite (à venir)

## Installation

### Prérequis

- Python 3.10+
- pip

### Étapes d'installation

1. **Cloner le projet** (si applicable)

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations**
```bash
python manage.py migrate
```

5. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

Le serveur sera accessible sur `http://localhost:8000`

## Structure du Projet

```
consulting_for_patient/
├── mysite/              # Configuration Django
│   ├── settings.py      # Paramètres du projet
│   └── urls.py         # URLs principales
├── pf/                  # Application principale
│   ├── models.py       # Modèles de données
│   ├── serializers.py  # Serializers DRF
│   ├── views.py        # Viewsets et views
│   ├── permissions.py  # Permissions personnalisées
│   ├── urls.py         # URLs de l'application
│   └── admin.py        # Configuration admin Django
├── requirements.txt    # Dépendances Python
└── API_DOCUMENTATION.md # Documentation complète des APIs
```

## Modèles de Données

### User (Utilisateur personnalisé)
- Gestion des utilisateurs avec rôles
- Rôles: administrateur, médecin, sage-femme, infirmier, pharmacien, agent d'enregistrement

### Patient
- Informations personnelles des patients
- Antécédents, allergies, historique

### ConsultationPF
- Consultations de planification familiale
- Anamnèse, examen, méthodes prescrites/posées

### RendezVous
- Gestion des rendez-vous
- Statuts: planifié, confirmé, en cours, terminé, annulé, absent

### MethodeContraceptive
- Catalogue des méthodes contraceptives
- Catégories: hormonale, barrière, DIU, permanent, naturelle

### StockItem
- Gestion des stocks de méthodes contraceptives
- Alertes de rupture et seuils

### Prescription
- Prescriptions liées aux consultations

### MouvementStock
- Traçabilité des mouvements de stock (entrées/sorties)

## Documentation API (Swagger)

La documentation interactive des APIs est disponible via Swagger UI :

- **Swagger UI** : `http://localhost:8000/swagger/`
- **ReDoc** : `http://localhost:8000/redoc/`
- **Schema JSON** : `http://localhost:8000/swagger.json`
- **Schema YAML** : `http://localhost:8000/swagger.yaml`

Vous pouvez tester toutes les APIs directement depuis l'interface Swagger.

## APIs Disponibles

### Authentification
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/refresh/` - Rafraîchir le token

### CRUD
- `/api/users/` - Gestion des utilisateurs
- `/api/patients/` - Gestion des patients
- `/api/methodes-contraceptives/` - Méthodes contraceptives
- `/api/rendez-vous/` - Rendez-vous
- `/api/consultations/` - Consultations PF
- `/api/stocks/` - Gestion des stocks
- `/api/prescriptions/` - Prescriptions
- `/api/mouvements-stock/` - Mouvements de stock

### Statistiques
- `/api/statistiques/` - Statistiques générales
- `/api/statistiques/consultations/` - Stats consultations
- `/api/statistiques/rendez-vous/` - Stats rendez-vous
- `/api/statistiques/stocks/` - Stats stocks

**Voir `API_DOCUMENTATION.md` pour la documentation complète.**

**Ou accéder directement à la documentation interactive Swagger : `http://localhost:8000/swagger/`**

## Permissions par Rôle

### Administrateur
- Accès complet à toutes les fonctionnalités

### Médecin / Sage-femme / Infirmier
- Gestion des patients
- Gestion des consultations
- Gestion des rendez-vous
- Consultation des stocks

### Pharmacien
- Gestion des stocks
- Mouvements de stock
- Consultation des prescriptions

### Agent d'enregistrement
- Gestion des rendez-vous
- Consultation des patients

## Développement

### Créer une migration
```bash
python manage.py makemigrations
```

### Appliquer les migrations
```bash
python manage.py migrate
```

### Accéder à l'admin Django
```
http://localhost:8000/admin/
```

### Créer des données de test
Utilisez l'interface admin Django ou les APIs pour créer des données de test.

## Configuration

### Variables d'environnement (recommandé pour la production)

Créer un fichier `.env` avec:
```
SECRET_KEY=votre_secret_key
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### CORS

Les origines autorisées sont configurées dans `settings.py`. Pour la production, modifiez `CORS_ALLOWED_ORIGINS`.

## Tests

```bash
python manage.py test
```

## Déploiement

1. Configurer les variables d'environnement
2. Changer `DEBUG = False` dans `settings.py`
3. Configurer une base de données PostgreSQL
4. Collecter les fichiers statiques: `python manage.py collectstatic`
5. Utiliser un serveur WSGI (Gunicorn, uWSGI)
6. Configurer un serveur web (Nginx, Apache)

## Documentation

- **Documentation API complète:** `API_DOCUMENTATION.md`
- **Cahier des charges:** `cahier_des_charges_pf.md`
- **Diagrammes UML:** Voir les fichiers PNG dans le projet

## Auteur

Développé pour le Centre Hospitalier Abass Ndao

## Licence

Propriétaire - Tous droits réservés

