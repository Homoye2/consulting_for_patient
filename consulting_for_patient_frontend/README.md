# Frontend - Application de Gestion de Planification Familiale

Application React + Vite.js pour la gestion de planification familiale au Centre Hospitalier Abass Ndao.

## 🚀 Technologies utilisées

- **React 19** - Bibliothèque UI
- **Vite** - Build tool et dev server
- **React Router** - Routing
- **TailwindCSS** - Framework CSS
- **shadcn/ui** - Composants UI (style Radix UI)
- **Axios** - Client HTTP
- **date-fns** - Manipulation de dates
- **Lucide React** - Icônes

## 📦 Installation

### Prérequis

- Node.js 18+ et npm

### Étapes

1. **Installer les dépendances**
```bash
npm install
```

2. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet :
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Gestion Planification Familiale
```

3. **Démarrer le serveur de développement**
```bash
npm run dev
```

L'application sera accessible sur `http://localhost:5173`

## 🏗️ Structure du projet

```
src/
├── components/          # Composants réutilisables
│   ├── ui/             # Composants UI de base (shadcn/ui)
│   ├── Layout.jsx      # Layout principal avec sidebar
│   └── ProtectedRoute.jsx
├── contexts/           # Contextes React
│   └── AuthContext.jsx # Contexte d'authentification
├── lib/                # Utilitaires
│   ├── api.js          # Configuration Axios
│   └── utils.js        # Fonctions utilitaires
├── pages/              # Pages de l'application
│   ├── Login.jsx
│   ├── Dashboard.jsx
│   ├── Patients.jsx
│   ├── Consultations.jsx
│   ├── RendezVous.jsx
│   ├── Stocks.jsx
│   └── Utilisateurs.jsx
├── services/           # Services API
│   ├── authService.js
│   └── apiService.js
├── App.jsx             # Composant principal
├── main.jsx            # Point d'entrée
└── index.css           # Styles globaux (TailwindCSS)
```

## 🎨 Design

L'application utilise un thème **vert sombre** comme couleur principale :
- Couleur primaire : Vert sombre (#22c55e)
- Fond : Noir/gris très sombre
- Texte : Blanc/gris clair
- Design moderne et responsive

## 📱 Fonctionnalités

### Authentification
- Connexion avec email/mot de passe
- Gestion des tokens JWT
- Rafraîchissement automatique des tokens
- Routes protégées

### Dashboard
- Statistiques générales
- Vue d'ensemble de l'activité
- Alertes et notifications

### Gestion des Patients
- CRUD complet
- Recherche et filtrage
- Affichage des informations détaillées

### Consultations
- Création et gestion des consultations PF
- Association avec les patients
- Gestion des méthodes contraceptives

### Rendez-vous
- Planification des rendez-vous
- Gestion des statuts (planifié, confirmé, terminé, etc.)
- Actions rapides (confirmer, annuler)

### Stocks
- Gestion des stocks de méthodes contraceptives
- Alertes de rupture de stock
- Mouvements de stock (entrées/sorties)

### Utilisateurs
- Gestion des utilisateurs du système
- Attribution des rôles
- Activation/désactivation des comptes

## 🔐 Rôles et permissions

L'application gère différents rôles :
- **Administrateur** : Accès complet
- **Médecin** : Gestion patients, consultations, rendez-vous
- **Sage-femme** : Gestion patients, consultations, rendez-vous
- **Infirmier(ère)** : Gestion patients, consultations, rendez-vous
- **Pharmacien** : Gestion des stocks
- **Agent d'enregistrement** : Gestion des rendez-vous

## 🛠️ Scripts disponibles

- `npm run dev` - Démarrer le serveur de développement
- `npm run build` - Construire pour la production
- `npm run preview` - Prévisualiser le build de production
- `npm run lint` - Linter le code

## 📝 Notes importantes

1. **Backend requis** : L'application nécessite que le backend Django soit démarré sur `http://localhost:8000`
2. **CORS** : Assurez-vous que le backend autorise les requêtes depuis `http://localhost:5173`
3. **Variables d'environnement** : Modifiez `.env` selon votre configuration

## 🎯 Prochaines améliorations possibles

- [ ] Pagination côté client
- [ ] Filtres avancés
- [ ] Export de données (PDF, Excel)
- [ ] Graphiques et visualisations
- [ ] Notifications en temps réel
- [ ] Mode hors ligne
- [ ] Tests unitaires et d'intégration

## 📄 Licence

Propriétaire - Tous droits réservés
