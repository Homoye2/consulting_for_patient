# Guide d'utilisation de Swagger

## Accès à Swagger

Une fois le serveur Django démarré, accédez à la documentation Swagger via :

- **Swagger UI** (Interface interactive) : `http://localhost:8000/swagger/`
- **ReDoc** (Documentation alternative) : `http://localhost:8000/redoc/`

## Utilisation de Swagger UI

### 1. Authentification

1. Cliquez sur le bouton **"Authorize"** en haut à droite
2. Dans le champ "Value", entrez : `Bearer <votre_token_jwt>`
   - Exemple : `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
3. Cliquez sur **"Authorize"** puis **"Close"**

### 2. Obtenir un token JWT

1. Trouvez l'endpoint `/api/auth/login/` dans la section "Authentification"
2. Cliquez sur **"Try it out"**
3. Entrez vos identifiants :
   ```json
   {
     "email": "votre_email@example.com",
     "password": "votre_mot_de_passe"
   }
   ```
4. Cliquez sur **"Execute"**
5. Copiez le `access` token de la réponse
6. Utilisez ce token dans le bouton "Authorize" (étape 1)

### 3. Tester une API

1. Trouvez l'endpoint que vous souhaitez tester (ex: `/api/patients/`)
2. Cliquez sur **"Try it out"**
3. Remplissez les paramètres si nécessaire
4. Pour les requêtes POST/PUT, remplissez le body JSON
5. Cliquez sur **"Execute"**
6. Consultez la réponse dans la section "Responses"

## Fonctionnalités de Swagger

### Documentation automatique
- Tous les endpoints sont documentés automatiquement
- Les schémas de requête/réponse sont générés automatiquement
- Les paramètres de requête sont listés avec leurs descriptions

### Test interactif
- Testez directement les APIs depuis l'interface
- Pas besoin d'outils externes (Postman, cURL, etc.)
- Les réponses sont affichées avec le code de statut HTTP

### Schémas OpenAPI
- Exportez le schéma en JSON : `http://localhost:8000/swagger.json`
- Exportez le schéma en YAML : `http://localhost:8000/swagger.yaml`
- Utilisez ces schémas pour générer des clients API

## Exemple : Créer un patient

1. Authentifiez-vous (voir étape 1)
2. Trouvez `POST /api/patients/`
3. Cliquez sur **"Try it out"**
4. Remplissez le body :
   ```json
   {
     "nom": "Dupont",
     "prenom": "Marie",
     "dob": "1990-05-15",
     "sexe": "F",
     "telephone": "+221771234567"
   }
   ```
5. Cliquez sur **"Execute"**
6. Vérifiez la réponse (code 201 si succès)

## Exemple : Lister les patients

1. Authentifiez-vous
2. Trouvez `GET /api/patients/`
3. Cliquez sur **"Try it out"**
4. Optionnel : Ajoutez des paramètres de recherche/filtrage
5. Cliquez sur **"Execute"**
6. Consultez la liste des patients dans la réponse

## Astuces

- **Filtrage** : Utilisez les paramètres de requête pour filtrer les résultats
- **Pagination** : Les listes sont paginées (20 éléments par page)
- **Recherche** : Utilisez le paramètre `search` pour rechercher dans les champs
- **Tri** : Utilisez le paramètre `ordering` pour trier les résultats

## Résolution de problèmes

### Erreur 401 (Unauthorized)
- Vérifiez que vous êtes authentifié
- Vérifiez que votre token n'a pas expiré (durée de vie : 1 heure)
- Rafraîchissez votre token via `/api/auth/refresh/`

### Erreur 403 (Forbidden)
- Vérifiez que votre utilisateur a les permissions nécessaires
- Seuls les administrateurs peuvent gérer les utilisateurs
- Certaines APIs sont réservées à certains rôles

### Erreur 400 (Bad Request)
- Vérifiez le format JSON de votre requête
- Vérifiez que tous les champs requis sont présents
- Consultez la réponse pour les détails de l'erreur

## ReDoc

ReDoc offre une documentation alternative plus lisible :
- Accès : `http://localhost:8000/redoc/`
- Interface plus simple et épurée
- Meilleure pour la lecture de la documentation
- Pas de fonctionnalité de test interactif

