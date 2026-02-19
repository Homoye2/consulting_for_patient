# Documentation Complète des APIs - Système de Gestion Hospitalière Multi-Tenant

## Base URL
```
http://localhost:8000/api/
```

## Authentification

Toutes les APIs (sauf certaines publiques) nécessitent un token JWT dans le header :
```
Authorization: Bearer <access_token>
```
---

## 📋 Table des Matières

1. [Authentification](#authentification)
2. [Gestion des Utilisateurs](#gestion-des-utilisateurs)
3. [Gestion des Patients](#gestion-des-patients)
4. [Système Hospitalier](#système-hospitalier)
5. [Spécialistes et Spécialités](#spécialistes-et-spécialités)
6. [Rendez-vous et Consultations](#rendez-vous-et-consultations)
7. [Rendez-vous et Consultations](#rendez-vous-et-consultations)
8. [Pharmacies et Produits](#pharmacies-et-produits)
9. [Gestion des Stocks](#gestion-des-stocks)
10. [Commandes Pharmacie](#commandes-pharmacie)
11. [Notifications](#notifications)
12. [Rapports et Avis](#rapports-et-avis)
13. [Statistiques](#statistiques)
14. [Landing Page](#landing-page)
15. [Messages de Contact](#messages-de-contact)

---

## 🔐 Authentification

### Connexion (Login)
```
POST /api/auth/login/
```
**Utilisateurs :** Tous  
**Body :**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Rafraîchir le token
```
POST /api/auth/refresh/
```
**Utilisateurs :** Tous authentifiés  
**Body :**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 👥 Gestion des Utilisateurs

### Base : `/api/users/`
**Utilisateurs autorisés :** Super Admin, Admin Hôpital (pour leurs utilisateurs)

#### Endpoints principaux
- `GET /api/users/` - Liste des utilisateurs
- `POST /api/users/` - Créer un utilisateur
- `GET /api/users/{id}/` - Détails d'un utilisateur
- `PUT/PATCH /api/users/{id}/` - Modifier un utilisateur
- `DELETE /api/users/{id}/` - Supprimer un utilisateur

#### Actions spéciales
- `GET /api/users/me/` - Profil de l'utilisateur connecté
- `POST /api/users/{id}/activate/` - Activer un utilisateur
- `POST /api/users/{id}/deactivate/` - Désactiver un utilisateur

#### Rôles disponibles
- `super_admin` - Super administrateur
- `admin_hopital` - Administrateur d'hôpital
- `specialiste` - Médecin spécialiste
- `pharmacien` - Pharmacien
- `agent_enregistrement` - Agent d'enregistrement
- `patient` - Patient

#### Exemple de création
```json
{
  "nom": "Dr. Dupont",
  "email": "dupont@hopital.sn",
  "password": "password123",
  "password_confirm": "password123",
  "role": "specialiste",
  "actif": true
}
```

---

## 🏥 Patients

### Base : `/api/patients/`
**Utilisateurs autorisés :** Personnel médical, Agents, Admins

#### Endpoints principaux
- `GET /api/patients/` - Liste des patients
- `POST /api/patients/` - Créer un patient
- `GET /api/patients/{id}/` - Détails d'un patient
- `PUT/PATCH /api/patients/{id}/` - Modifier un patient
- `DELETE /api/patients/{id}/` - Supprimer un patient

#### Actions spéciales
- `GET /api/patients/me/` - Profil du patient connecté (patients uniquement)
- `GET /api/patients/{id}/consultations/` - Consultations d'un patient
- `GET /api/patients/{id}/rendez_vous/` - Rendez-vous d'un patient

#### Filtres disponibles
- `sexe` : M ou F
- `search` : nom, prénom, téléphone
- `ordering` : nom, prenom, dob, created_at

#### Exemple de création
```json
{
  "nom": "Diallo",
  "prenom": "Fatou",
  "dob": "1990-05-15",
  "sexe": "F",
  "telephone": "+221771234567",
  "email": "fatou@email.com",
  "adresse": "Dakar, Sénégal",
  "ville_actuelle": "Dakar",
  "antecedents": "Aucun",
  "allergies": "Pénicilline"
}
```

---

## 🏥 Système Hospitalier

### Hôpitaux : `/api/hopitaux/`
**Utilisateurs autorisés :** Super Admin (CRUD), Admin Hôpital (lecture de son hôpital), Public (lecture des hôpitaux actifs)

#### Endpoints principaux
- `GET /api/hopitaux/` - Liste des hôpitaux
- `POST /api/hopitaux/` - Créer un hôpital (Super Admin)
- `GET /api/hopitaux/{id}/` - Détails d'un hôpital
- `PUT/PATCH /api/hopitaux/{id}/` - Modifier un hôpital
- `DELETE /api/hopitaux/{id}/` - Supprimer un hôpital

#### Actions spéciales
- `GET /api/hopitaux/proximite/` - Hôpitaux proches (public)
  - Query params : `lat`, `lng`, `rayon` (km)
- `GET /api/hopitaux/mon_hopital/` - Hôpital de l'admin connecté
- `GET /api/hopitaux/{id}/specialistes/` - Spécialistes d'un hôpital
- `GET /api/hopitaux/{id}/specialites/` - Spécialités disponibles
- `POST /api/hopitaux/{id}/activer/` - Activer un hôpital (Super Admin)
- `POST /api/hopitaux/{id}/suspendre/` - Suspendre un hôpital (Super Admin)

#### Filtres
- `ville` : Filtrer par ville
- `actif` : true/false
- `search` : nom, code_hopital, ville

#### Exemple de création
```json
{
  "nom": "Hôpital Abass Ndao",
  "code_hopital": "HAN001",
  "adresse": "Route de l'aéroport, Dakar",
  "ville": "Dakar",
  "pays": "Sénégal",
  "telephone": "+221338234567",
  "email": "contact@abassndao.sn",
  "latitude": "14.6937",
  "longitude": "-17.4441",
  "couleur_theme": "#2563eb",
  "description": "Hôpital de référence",
  "admin_hopital": 2
}
```

---

## 👨‍⚕️ Spécialistes et Spécialités

### Spécialités : `/api/specialites/`
**Utilisateurs autorisés :** Tous (lecture), Super Admin (écriture)

#### Endpoints
- `GET /api/specialites/` - Liste des spécialités
- `POST /api/specialites/` - Créer une spécialité (Super Admin)
- `GET /api/specialites/{id}/` - Détails d'une spécialité
- `PUT/PATCH /api/specialites/{id}/` - Modifier (Super Admin)
- `DELETE /api/specialites/{id}/` - Supprimer (Super Admin)

### Spécialistes : `/api/specialistes/`
**Utilisateurs autorisés :** Tous (lecture des actifs), Admin Hôpital (ses spécialistes), Spécialiste (son profil)

#### Endpoints principaux
- `GET /api/specialistes/` - Liste des spécialistes
- `POST /api/specialistes/` - Créer un spécialiste
- `GET /api/specialistes/{id}/` - Détails d'un spécialiste
- `PUT/PATCH /api/specialistes/{id}/` - Modifier un spécialiste

#### Actions spéciales
- `GET /api/specialistes/me/` - Profil du spécialiste connecté
- `GET /api/specialistes/{id}/disponibilites/` - Disponibilités d'un spécialiste
- `GET /api/specialistes/{id}/creneaux_libres/` - Créneaux libres pour une date
  - Query param : `date` (YYYY-MM-DD)
- `GET /api/specialistes/{id}/avis/` - Avis sur un spécialiste
- `GET /api/specialistes/{id}/statistiques/` - Statistiques d'un spécialiste

#### Filtres
- `hopital` : ID de l'hôpital
- `specialite` : ID de la spécialité
- `actif` : true/false
- `search` : nom, email, numéro d'ordre

### Disponibilités : `/api/disponibilites/`
**Utilisateurs autorisés :** Spécialistes (leurs disponibilités), Admins

#### Endpoints
- `GET /api/disponibilites/` - Liste des disponibilités
- `POST /api/disponibilites/` - Créer une disponibilité
- `POST /api/disponibilites/bulk_create/` - Créer plusieurs disponibilités

#### Exemple de disponibilité
```json
{
  "specialiste": 1,
  "jour_semaine": "lundi",
  "heure_debut": "08:00",
  "heure_fin": "12:00",
  "actif": true
}
```

---

## 📅 Rendez-vous et Consultations

### Rendez-vous : `/api/rendez-vous/`
**Utilisateurs autorisés :** Personnel médical, Patients (leurs RDV), Admins

#### Endpoints principaux
- `GET /api/rendez-vous/` - Liste des rendez-vous
- `POST /api/rendez-vous/` - Créer un rendez-vous
- `GET /api/rendez-vous/{id}/` - Détails d'un rendez-vous
- `PUT/PATCH /api/rendez-vous/{id}/` - Modifier un rendez-vous
- `DELETE /api/rendez-vous/{id}/` - Supprimer un rendez-vous

#### Actions spéciales
- `GET /api/rendez-vous/agenda/` - Agenda d'un spécialiste
  - Query params : `specialiste_id`, `date`
- `POST /api/rendez-vous/{id}/confirmer/` - Confirmer un RDV
- `POST /api/rendez-vous/{id}/annuler/` - Annuler un RDV

#### Statuts disponibles
- `en_attente` - En attente de confirmation
- `confirme` - Confirmé par le spécialiste
- `refuse` - Refusé
- `annule` - Annulé
- `termine` - Terminé

#### Filtres
- `statut` : Statut du RDV
- `patient` : ID du patient
- `specialiste` : ID du spécialiste
- `date_debut`, `date_fin` : Période
- `search` : nom patient, notes

### Consultations PF : `/api/consultations/`
**Utilisateurs autorisés :** Personnel médical, Patients (leurs consultations), Admins

#### Endpoints principaux
- `GET /api/consultations/` - Liste des consultations
- `POST /api/consultations/` - Créer une consultation
- `GET /api/consultations/{id}/` - Détails d'une consultation
- `PUT/PATCH /api/consultations/{id}/` - Modifier une consultation
- `DELETE /api/consultations/{id}/` - Supprimer une consultation

#### Exemple de consultation
```json
{
  "patient": 1,
  "specialiste": 2,
  "hopital": 1,
  "rendez_vous": 5,
  "date": "2025-12-25T10:00:00Z",
  "anamnese": "Patiente souhaite une contraception",
  "examen": "Examen normal",
  "methode_posee": true,
  "notes": "Suivi dans 3 mois"
}
```

---

## 🏪 Pharmacies et Produits

### Pharmacies : `/api/pharmacies/`
**Utilisateurs autorisés :** Super Admin (toutes), Pharmaciens (leurs pharmacies)

#### Endpoints principaux
- `GET /api/pharmacies/` - Liste des pharmacies
- `POST /api/pharmacies/` - Créer une pharmacie
- `GET /api/pharmacies/{id}/` - Détails d'une pharmacie
- `PUT/PATCH /api/pharmacies/{id}/` - Modifier
- `DELETE /api/pharmacies/{id}/` - Supprimer

#### Actions spéciales
- `GET /api/pharmacies/mes_pharmacies/` - Pharmacies du pharmacien connecté
- `POST /api/pharmacies/{id}/activer/` - Activer une pharmacie
- `POST /api/pharmacies/{id}/desactiver/` - Désactiver une pharmacie

### Produits : `/api/produits/`
**Utilisateurs autorisés :** Tous (lecture des actifs), Super Admin et Pharmaciens (écriture)

#### Endpoints principaux
- `GET /api/produits/` - Liste des produits
- `POST /api/produits/` - Créer un produit
- `GET /api/produits/{id}/` - Détails d'un produit
- `PUT/PATCH /api/produits/{id}/` - Modifier
- `DELETE /api/produits/{id}/` - Supprimer

#### Actions spéciales
- `GET /api/produits/recherche/` - Recherche avancée
  - Query params : `q` (terme), `categorie`
- `GET /api/produits/{id}/disponibilite/` - Pharmacies où le produit est disponible

#### Catégories de produits
- `medicament` - Médicaments
- `contraceptif` - Contraceptifs
- `supplement` - Suppléments
- `materiel_medical` - Matériel médical
- `hygiene` - Produits d'hygiène
- `autre` - Autres

---

## 📦 Gestion des Stocks

### Stocks Produits : `/api/stocks-produits/`
**Utilisateurs autorisés :** Super Admin (tous), Pharmaciens (leurs stocks)

#### Endpoints
- `GET /api/stocks-produits/` - Liste des stocks de produits
- `POST /api/stocks-produits/` - Créer un stock
- `GET /api/stocks-produits/{id}/` - Détails
- `PUT/PATCH /api/stocks-produits/{id}/` - Modifier
- `DELETE /api/stocks-produits/{id}/` - Supprimer

#### Actions spéciales
- `GET /api/stocks-produits/alertes/` - Stocks en alerte
- `GET /api/stocks-produits/expirations/` - Produits proches d'expiration

---

## 🛒 Commandes Pharmacie

### Base : `/api/commandes-pharmacie/`
**Utilisateurs autorisés :** Super Admin (toutes), Pharmaciens (leurs commandes), Patients (leurs commandes)

#### Endpoints principaux
- `GET /api/commandes-pharmacie/` - Liste des commandes
- `POST /api/commandes-pharmacie/` - Créer une commande
- `GET /api/commandes-pharmacie/{id}/` - Détails d'une commande
- `PUT/PATCH /api/commandes-pharmacie/{id}/` - Modifier
- `DELETE /api/commandes-pharmacie/{id}/` - Supprimer

#### Actions spéciales
- `GET /api/commandes-pharmacie/mes_commandes/` - Commandes du patient connecté
- `GET /api/commandes-pharmacie/pharmacie/` - Commandes d'une pharmacie
  - Query param : `pharmacie_id`
- `POST /api/commandes-pharmacie/{id}/confirmer/` - Confirmer une commande
- `POST /api/commandes-pharmacie/{id}/preparer/` - Marquer comme préparée
- `POST /api/commandes-pharmacie/{id}/prete/` - Marquer comme prête
- `POST /api/commandes-pharmacie/{id}/recuperer/` - Marquer comme récupérée
- `POST /api/commandes-pharmacie/{id}/annuler/` - Annuler une commande

#### Statuts des commandes
- `en_attente` - En attente de confirmation
- `confirmee` - Confirmée par la pharmacie
- `preparee` - En cours de préparation
- `prete` - Prête à être récupérée
- `recuperee` - Récupérée par le patient
- `annulee` - Annulée

---

## 🔔 Notifications

### Base : `/api/notifications/`
**Utilisateurs autorisés :** Chaque utilisateur voit ses propres notifications

#### Endpoints
- `GET /api/notifications/` - Liste des notifications
- `POST /api/notifications/` - Créer une notification
- `GET /api/notifications/{id}/` - Détails d'une notification
- `PUT/PATCH /api/notifications/{id}/` - Modifier
- `DELETE /api/notifications/{id}/` - Supprimer

#### Actions spéciales
- `GET /api/notifications/non_lues/` - Nombre de notifications non lues
- `POST /api/notifications/{id}/marquer_lu/` - Marquer comme lue
- `POST /api/notifications/marquer_toutes_lues/` - Marquer toutes comme lues

#### Types de notifications
- `rendez_vous_nouveau` - Nouveau rendez-vous
- `rendez_vous_confirme` - RDV confirmé
- `rendez_vous_refuse` - RDV refusé
- `rendez_vous_rappel` - Rappel de RDV
- `commande_confirmee` - Commande confirmée
- `commande_prete` - Commande prête
- `consultation_rapport` - Rapport disponible
- `stock_alerte` - Alerte de stock
- `autre` - Autre type

---

## 📋 Rapports et Avis

### Rapports de Consultation : `/api/rapports-consultations/`
**Utilisateurs autorisés :** Spécialistes (leurs rapports), Patients (leurs rapports), Admins

#### Endpoints
- `GET /api/rapports-consultations/` - Liste des rapports
- `POST /api/rapports-consultations/` - Créer un rapport
- `GET /api/rapports-consultations/{id}/` - Détails
- `PUT/PATCH /api/rapports-consultations/{id}/` - Modifier
- `DELETE /api/rapports-consultations/{id}/` - Supprimer

#### Actions spéciales
- `POST /api/rapports-consultations/{id}/envoyer_patient/` - Envoyer au patient

### Avis Spécialistes : `/api/avis-specialistes/`
**Utilisateurs autorisés :** Tous (lecture), Patients (création d'avis)

#### Endpoints
- `GET /api/avis-specialistes/` - Liste des avis
- `POST /api/avis-specialistes/` - Créer un avis (patients uniquement)
- `GET /api/avis-specialistes/{id}/` - Détails
- `PUT/PATCH /api/avis-specialistes/{id}/` - Modifier
- `DELETE /api/avis-specialistes/{id}/` - Supprimer

#### Exemple d'avis
```json
{
  "specialiste": 1,
  "rendez_vous": 5,
  "note": 5,
  "commentaire": "Excellent médecin, très à l'écoute",
  "ponctualite": 5,
  "ecoute": 5,
  "explication": 5,
  "recommande": true
}
```

---

## 📊 Statistiques

### Statistiques Générales : `/api/statistiques/`
**Utilisateurs autorisés :** Tous les utilisateurs authentifiés

**Response :**
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

### Statistiques des Consultations : `/api/statistiques/consultations/`
**Utilisateurs autorisés :** Personnel médical, Admins

**Query Parameters :**
- `date_debut`, `date_fin` : Période d'analyse

### Statistiques des Rendez-vous : `/api/statistiques/rendez-vous/`
**Utilisateurs autorisés :** Personnel médical, Agents, Admins

### Statistiques des Stocks : `/api/statistiques/stocks/`
**Utilisateurs autorisés :** Admins, Pharmaciens

---

## 🌐 Landing Page

### Contenu : `/api/landing-page/`
**Utilisateurs autorisés :** Admins (écriture), Public (lecture)

#### Endpoints
- `GET /api/landing-page/` - Contenu de la landing page
- `PUT/PATCH /api/landing-page/{id}/` - Modifier le contenu
- `GET /api/landing-page/public/` - Endpoint public (sans auth)

### Services : `/api/services/`
**Utilisateurs autorisés :** Admins (écriture), Public (lecture)

#### Endpoints
- `GET /api/services/` - Liste des services
- `POST /api/services/` - Créer un service
- `GET /api/services/public/` - Endpoint public

### Valeurs : `/api/values/`
**Utilisateurs autorisés :** Admins (écriture)

---

## 💬 Messages de Contact

### Base : `/api/contact-messages/`
**Utilisateurs autorisés :** Personnel médical et Admins (lecture), Patients (leurs messages), Public (création)

#### Endpoints
- `GET /api/contact-messages/` - Liste des messages
- `POST /api/contact-messages/` - Créer un message
- `GET /api/contact-messages/{id}/` - Détails
- `PUT/PATCH /api/contact-messages/{id}/` - Modifier
- `DELETE /api/contact-messages/{id}/` - Supprimer

#### Exemple de message
```json
{
  "nom": "Jean Dupont",
  "email": "jean@email.com",
  "sujet": "Demande d'information",
  "message": "Je souhaite prendre rendez-vous..."
}
```

---

## 🔧 Informations Techniques

### Pagination
Toutes les listes sont paginées (20 éléments par page par défaut).

### Filtrage et Recherche
- Utilisez `search` pour la recherche textuelle
- Utilisez les champs spécifiques pour le filtrage exact
- Utilisez `ordering` pour le tri

### Codes de Statut HTTP
- `200 OK` : Succès
- `201 Created` : Ressource créée
- `400 Bad Request` : Erreur de validation
- `401 Unauthorized` : Non authentifié
- `403 Forbidden` : Permission refusée
- `404 Not Found` : Ressource non trouvée
- `500 Internal Server Error` : Erreur serveur

### Format des Dates
- Dates : `YYYY-MM-DD`
- DateTime : `YYYY-MM-DDTHH:MM:SSZ`

---

## 🚀 Exemples d'Utilisation

### Workflow Patient
1. **Inscription** : `POST /api/users/` (rôle patient)
2. **Création profil** : `POST /api/patients/`
3. **Recherche spécialiste** : `GET /api/specialistes/?specialite=1`
4. **Vérification créneaux** : `GET /api/specialistes/1/creneaux_libres/?date=2025-12-26`
5. **Prise de RDV** : `POST /api/rendez-vous/`
6. **Suivi notifications** : `GET /api/notifications/`

### Workflow Spécialiste
1. **Connexion** : `POST /api/auth/login/`
2. **Profil** : `GET /api/specialistes/me/`
3. **Agenda** : `GET /api/rendez-vous/agenda/?date=2025-12-26`
4. **Confirmation RDV** : `POST /api/rendez-vous/5/confirmer/`
5. **Consultation** : `POST /api/consultations/`
6. **Rapport** : `POST /api/rapports-consultations/`

### Workflow Pharmacien
1. **Mes pharmacies** : `GET /api/pharmacies/mes_pharmacies/`
2. **Stocks** : `GET /api/stocks-produits/?pharmacie=1`
3. **Alertes** : `GET /api/stocks-produits/alertes/`
4. **Commandes** : `GET /api/commandes-pharmacie/pharmacie/?pharmacie_id=1`
5. **Traitement** : `POST /api/commandes-pharmacie/10/confirmer/`

---

## 🔒 Sécurité et Permissions

### Niveaux d'accès
1. **Public** : Landing page, services, recherche hôpitaux
2. **Patient** : Ses données, RDV, consultations, commandes
3. **Spécialiste** : Ses patients, RDV, consultations, rapports
4. **Pharmacien** : Ses pharmacies, stocks, commandes
5. **Admin Hôpital** : Données de son hôpital
6. **Super Admin** : Accès complet

### Bonnes Pratiques
- Toujours vérifier les permissions avant l'accès
- Utiliser HTTPS en production
- Renouveler les tokens régulièrement
- Logger les actions sensibles
- Valider toutes les entrées utilisateur

---

Cette documentation couvre l'ensemble des APIs disponibles dans le système. Pour des détails spécifiques sur les schémas de données, consultez la documentation Swagger à `/swagger/`.