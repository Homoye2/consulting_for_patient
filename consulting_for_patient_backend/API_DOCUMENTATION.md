# Documentation API - Application de Gestion de Planification Familiale

## Base URL
```
http://localhost:8000/api/
```

## Authentification

Toutes les APIs (sauf l'authentification) nécessitent un token JWT dans le header :
```
Authorization: Bearer <access_token>
```

### Endpoints d'authentification

#### 1. Connexion (Login)
```
POST /api/auth/login/
```

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "nom": "Nom Utilisateur",
    "role": "medecin"
  }
}
```

#### 2. Rafraîchir le token (Refresh)
```
POST /api/auth/refresh/
```

**Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## APIs CRUD

### 1. Utilisateurs (`/api/users/`)

**Permissions:** Administrateurs uniquement

#### Liste des utilisateurs
```
GET /api/users/
```

**Query Parameters:**
- `search`: Recherche par nom ou email
- `ordering`: Tri (nom, email, date_joined)

#### Détails d'un utilisateur
```
GET /api/users/{id}/
```

#### Créer un utilisateur
```
POST /api/users/
```

**Body:**
```json
{
  "nom": "Nom",
  "email": "email@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "role": "medecin",
  "actif": true
}
```

**Rôles disponibles:**
- `administrateur`
- `medecin`
- `sage_femme`
- `infirmier`
- `pharmacien`
- `agent_enregistrement`

#### Mettre à jour un utilisateur
```
PUT /api/users/{id}/
PATCH /api/users/{id}/
```

#### Supprimer un utilisateur
```
DELETE /api/users/{id}/
```

#### Actions personnalisées
- `GET /api/users/me/` - Informations de l'utilisateur connecté
- `POST /api/users/{id}/activate/` - Activer un utilisateur
- `POST /api/users/{id}/deactivate/` - Désactiver un utilisateur

---

### 2. Patients (`/api/patients/`)

**Permissions:** Personnel médical et administrateurs

#### Liste des patients
```
GET /api/patients/
```

**Query Parameters:**
- `sexe`: Filtrer par sexe (M, F)
- `search`: Recherche par nom, prénom, téléphone
- `ordering`: Tri (nom, prenom, dob, created_at)

#### Détails d'un patient
```
GET /api/patients/{id}/
```

#### Créer un patient
```
POST /api/patients/
```

**Body:**
```json
{
  "nom": "Dupont",
  "prenom": "Marie",
  "dob": "1990-05-15",
  "sexe": "F",
  "telephone": "+221771234567",
  "adresse": "Adresse complète",
  "antecedents": "Antécédents médicaux",
  "allergies": "Allergies connues"
}
```

#### Mettre à jour un patient
```
PUT /api/patients/{id}/
PATCH /api/patients/{id}/
```

#### Supprimer un patient
```
DELETE /api/patients/{id}/
```

#### Actions personnalisées
- `GET /api/patients/{id}/consultations/` - Consultations d'un patient
- `GET /api/patients/{id}/rendez_vous/` - Rendez-vous d'un patient

---

### 3. Méthodes Contraceptives (`/api/methodes-contraceptives/`)

**Permissions:** Lecture pour tous, écriture pour administrateurs

#### Liste des méthodes
```
GET /api/methodes-contraceptives/
```

**Query Parameters:**
- `categorie`: Filtrer par catégorie
- `search`: Recherche par nom ou description
- `ordering`: Tri (nom, categorie)

**Catégories disponibles:**
- `hormonale`
- `barriere`
- `iud`
- `permanent`
- `naturelle`

#### Créer une méthode
```
POST /api/methodes-contraceptives/
```

**Body:**
```json
{
  "nom": "Pilule contraceptive",
  "categorie": "hormonale",
  "description": "Description de la méthode"
}
```

---

### 4. Rendez-vous (`/api/rendez-vous/`)

**Permissions:** Personnel médical, agents d'enregistrement et administrateurs

#### Liste des rendez-vous
```
GET /api/rendez-vous/
```

**Query Parameters:**
- `statut`: Filtrer par statut
- `patient`: ID du patient
- `user`: ID du professionnel
- `date_debut`: Date de début (YYYY-MM-DD)
- `date_fin`: Date de fin (YYYY-MM-DD)
- `search`: Recherche par nom patient ou notes
- `ordering`: Tri (datetime, created_at)

**Statuts disponibles:**
- `planifie`
- `confirme`
- `en_cours`
- `termine`
- `annule`
- `absent`

#### Créer un rendez-vous
```
POST /api/rendez-vous/
```

**Body:**
```json
{
  "patient": 1,
  "user": 2,
  "datetime": "2025-11-20T10:00:00Z",
  "statut": "planifie",
  "notes": "Notes optionnelles"
}
```

#### Actions personnalisées
- `GET /api/rendez-vous/agenda/` - Agenda d'un professionnel
  - Query params: `user_id`, `date` (YYYY-MM-DD)
- `POST /api/rendez-vous/{id}/confirmer/` - Confirmer un RDV
- `POST /api/rendez-vous/{id}/annuler/` - Annuler un RDV

---

### 5. Consultations PF (`/api/consultations/`)

**Permissions:** Personnel médical et administrateurs

#### Liste des consultations
```
GET /api/consultations/
```

**Query Parameters:**
- `patient`: ID du patient
- `user`: ID du professionnel
- `methode_prescite`: ID de la méthode
- `methode_posee`: Boolean
- `date_debut`: Date de début
- `date_fin`: Date de fin
- `search`: Recherche par nom patient, notes, anamnèse
- `ordering`: Tri (date, created_at)

#### Créer une consultation
```
POST /api/consultations/
```

**Body:**
```json
{
  "patient": 1,
  "user": 2,
  "date": "2025-11-20T10:00:00Z",
  "anamnese": "Anamnèse du patient",
  "examen": "Examen clinique",
  "methode_proposee": 1,
  "methode_prescite": 1,
  "methode_posee": true,
  "effets_secondaires": "Aucun",
  "notes": "Notes de consultation",
  "observation": "Observations"
}
```

#### Actions personnalisées
- `GET /api/consultations/{id}/prescriptions/` - Prescriptions d'une consultation

---

### 6. Stocks (`/api/stocks/`)

**Permissions:** Administrateurs et pharmaciens

#### Liste des stocks
```
GET /api/stocks/
```

**Query Parameters:**
- `methode`: ID de la méthode
- `search`: Recherche par nom de méthode
- `ordering`: Tri (quantite, methode__nom)

#### Créer un stock
```
POST /api/stocks/
```

**Body:**
```json
{
  "methode": 1,
  "quantite": 100,
  "seuil": 10
}
```

#### Actions personnalisées
- `GET /api/stocks/alertes/` - Stocks en alerte (sous seuil)
- `GET /api/stocks/ruptures/` - Stocks en rupture

---

### 7. Prescriptions (`/api/prescriptions/`)

**Permissions:** Personnel médical et administrateurs

#### Liste des prescriptions
```
GET /api/prescriptions/
```

**Query Parameters:**
- `consultation`: ID de la consultation
- `methode`: ID de la méthode
- `ordering`: Tri (date_prescription)

#### Créer une prescription
```
POST /api/prescriptions/
```

**Body:**
```json
{
  "consultation": 1,
  "methode": 1,
  "dosage": "1 comprimé par jour",
  "remarque": "Prendre le matin"
}
```

---

### 8. Mouvements de Stock (`/api/mouvements-stock/`)

**Permissions:** Administrateurs et pharmaciens

#### Liste des mouvements
```
GET /api/mouvements-stock/
```

**Query Parameters:**
- `type_mouvement`: Type (entree, sortie, inventaire, perte)
- `stock_item`: ID de l'article de stock
- `ordering`: Tri (date_mouvement)

#### Créer un mouvement
```
POST /api/mouvements-stock/
```

**Body:**
```json
{
  "stock_item": 1,
  "type_mouvement": "entree",
  "quantite": 50,
  "motif": "Réapprovisionnement"
}
```

**Types de mouvement:**
- `entree`: Augmente le stock
- `sortie`: Diminue le stock
- `inventaire`: Met à jour le stock à la quantité spécifiée
- `perte`: Diminue le stock (perte/casse)

**Note:** Le stock est automatiquement mis à jour lors de la création d'un mouvement.

---

## APIs Statistiques

### 1. Statistiques générales
```
GET /api/statistiques/
```

**Permissions:** Tous les utilisateurs authentifiés

**Response:**
```json
{
  "total_patients": 150,
  "total_consultations": 500,
  "total_rendez_vous": 300,
  "total_stocks": 20,
  "consultations_30j": 45,
  "rendez_vous_a_venir": 25,
  "stocks_alerte": 3
}
```

---

### 2. Statistiques des consultations
```
GET /api/statistiques/consultations/
```

**Permissions:** Personnel médical et administrateurs

**Query Parameters:**
- `date_debut`: Date de début (YYYY-MM-DD)
- `date_fin`: Date de fin (YYYY-MM-DD)

**Response:**
```json
{
  "total_consultations": 500,
  "methodes_distribution": [
    {"methode_prescite__nom": "Pilule", "count": 200},
    {"methode_prescite__nom": "DIU", "count": 150}
  ],
  "methodes_posees": 350,
  "taux_pose": 70.0
}
```

---

### 3. Statistiques des rendez-vous
```
GET /api/statistiques/rendez-vous/
```

**Permissions:** Personnel médical, agents et administrateurs

**Query Parameters:**
- `date_debut`: Date de début
- `date_fin`: Date de fin

**Response:**
```json
{
  "total_rendez_vous": 300,
  "par_statut": [
    {"statut": "termine", "count": 200},
    {"statut": "absent", "count": 20}
  ],
  "termines": 200,
  "absents": 20,
  "taux_assiduite": 90.91
}
```

---

### 4. Statistiques des stocks
```
GET /api/statistiques/stocks/
```

**Permissions:** Administrateurs et pharmaciens

**Response:**
```json
{
  "stocks_rupture": 2,
  "stocks_sous_seuil": 5,
  "total_quantite": 1500,
  "mouvements_7j": 15
}
```

---

## Pagination

Toutes les listes sont paginées avec 20 éléments par page par défaut.

**Response avec pagination:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/patients/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Codes de statut HTTP

- `200 OK`: Succès
- `201 Created`: Ressource créée
- `400 Bad Request`: Erreur de validation
- `401 Unauthorized`: Non authentifié
- `403 Forbidden`: Permission refusée
- `404 Not Found`: Ressource non trouvée
- `500 Internal Server Error`: Erreur serveur

---

## Exemples d'utilisation

### Exemple avec cURL

```bash
# Connexion
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'

# Liste des patients
curl -X GET http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer <access_token>"

# Créer un patient
curl -X POST http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Marie",
    "dob": "1990-05-15",
    "sexe": "F",
    "telephone": "+221771234567"
  }'
```

---

## Notes importantes

1. **Sécurité:** Toutes les APIs nécessitent une authentification JWT (sauf `/auth/login/`)
2. **Permissions:** Les permissions sont basées sur les rôles des utilisateurs
3. **Pagination:** Toutes les listes sont paginées
4. **Filtrage:** Utilisez les query parameters pour filtrer et rechercher
5. **Dates:** Format ISO 8601 (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SSZ)

