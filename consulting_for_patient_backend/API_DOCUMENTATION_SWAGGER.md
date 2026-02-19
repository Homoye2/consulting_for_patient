# Documentation API E-SORA - Swagger/OpenAPI

## Accès à la documentation interactive

### URLs de documentation

- **Swagger UI**: `https://e-sora.onglalumiere.org/api/swagger/`
- **ReDoc**: `https://e-sora.onglalumiere.org/api/redoc/`
- **Schema JSON**: `https://e-sora.onglalumiere.org/api/swagger.json`
- **Schema YAML**: `https://e-sora.onglalumiere.org/api/swagger.yaml`

---

## Configuration Swagger

La documentation API est générée automatiquement avec `drf-yasg` (Yet Another Swagger Generator).

### Informations de l'API

```yaml
title: E-SORA API
version: 1.0.0
description: API pour la gestion des consultations de planning familial, hôpitaux, pharmacies et ordonnances
contact:
  email: support@e-sora.onglalumiere.org
license:
  name: Propriétaire
```

---

## Authentification

### JWT (JSON Web Tokens)

Toutes les requêtes API (sauf les endpoints publics) nécessitent un token JWT.

#### Obtenir un token

**Endpoint**: `POST /api/auth/login/`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "nom": "John Doe",
    "role": "super_admin"
  }
}
```

#### Utiliser le token

Ajoutez le header à toutes vos requêtes:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Rafraîchir le token

**Endpoint**: `POST /api/auth/refresh/`

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Endpoints principaux

### 1. Authentification

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/api/auth/login/` | Connexion générale | Non |
| POST | `/api/auth/pharmacy-login/` | Connexion pharmacie | Non |
| POST | `/api/auth/hospital-login/` | Connexion hôpital | Non |
| POST | `/api/auth/refresh/` | Rafraîchir le token | Non |
| POST | `/api/auth/change-password/` | Changer le mot de passe | Oui |
| POST | `/api/auth/google/` | Authentification Google | Non |

### 2. Utilisateurs

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/users/` | Liste des utilisateurs | super_admin |
| POST | `/api/users/` | Créer un utilisateur | super_admin |
| GET | `/api/users/{id}/` | Détails utilisateur | Tous |
| PUT | `/api/users/{id}/` | Modifier utilisateur | super_admin, self |
| DELETE | `/api/users/{id}/` | Supprimer utilisateur | super_admin |
| GET | `/api/users/me/` | Profil actuel | Tous |
| POST | `/api/users/{id}/activate/` | Activer utilisateur | super_admin |
| POST | `/api/users/{id}/deactivate/` | Désactiver utilisateur | super_admin |

### 3. Patients

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/patients/` | Liste des patients | Médical |
| POST | `/api/patients/` | Créer un patient | Médical |
| GET | `/api/patients/{id}/` | Détails patient | Médical |
| PUT | `/api/patients/{id}/` | Modifier patient | Médical |
| DELETE | `/api/patients/{id}/` | Supprimer patient | super_admin |
| GET | `/api/patients/{id}/consultations/` | Consultations du patient | Médical |
| GET | `/api/patients/{id}/rendez-vous/` | RDV du patient | Médical |
| GET | `/api/patients/{id}/dossier-medical/` | Dossier médical | Médical |

### 4. Hôpitaux

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/hopitaux/` | Liste des hôpitaux | Public |
| POST | `/api/hopitaux/` | Créer un hôpital | super_admin |
| GET | `/api/hopitaux/{id}/` | Détails hôpital | Public |
| PUT | `/api/hopitaux/{id}/` | Modifier hôpital | admin_hopital |
| DELETE | `/api/hopitaux/{id}/` | Supprimer hôpital | super_admin |
| GET | `/api/hopitaux/proximite/` | Hôpitaux à proximité | Public |
| GET | `/api/hopitaux/{id}/specialistes/` | Spécialistes de l'hôpital | Public |
| GET | `/api/hopitaux/{id}/specialites/` | Spécialités de l'hôpital | Public |
| GET | `/api/hopitaux/{id}/statistiques/` | Statistiques hôpital | admin_hopital |

### 5. Spécialités

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/specialites/` | Liste des spécialités | Public |
| POST | `/api/specialites/` | Créer une spécialité | super_admin |
| GET | `/api/specialites/{id}/` | Détails spécialité | Public |
| PUT | `/api/specialites/{id}/` | Modifier spécialité | super_admin |
| DELETE | `/api/specialites/{id}/` | Supprimer spécialité | super_admin |
| GET | `/api/specialites/{id}/specialistes/` | Spécialistes de la spécialité | Public |

### 6. Spécialistes

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/specialistes/` | Liste des spécialistes | Public |
| POST | `/api/specialistes/` | Créer un spécialiste | admin_hopital |
| GET | `/api/specialistes/{id}/` | Détails spécialiste | Public |
| PUT | `/api/specialistes/{id}/` | Modifier spécialiste | specialiste, admin_hopital |
| DELETE | `/api/specialistes/{id}/` | Supprimer spécialiste | admin_hopital |
| GET | `/api/specialistes/{id}/disponibilites/` | Disponibilités | Public |
| GET | `/api/specialistes/{id}/rendez-vous/` | RDV du spécialiste | specialiste |
| GET | `/api/specialistes/{id}/avis/` | Avis du spécialiste | Public |
| GET | `/api/specialistes/{id}/statistiques/` | Statistiques | specialiste |

### 7. Rendez-vous

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/rendez-vous/` | Liste des RDV | Médical |
| POST | `/api/rendez-vous/` | Créer un RDV | patient, agent |
| GET | `/api/rendez-vous/{id}/` | Détails RDV | Médical |
| PUT | `/api/rendez-vous/{id}/` | Modifier RDV | Médical |
| DELETE | `/api/rendez-vous/{id}/` | Supprimer RDV | Médical |
| POST | `/api/rendez-vous/{id}/confirmer/` | Confirmer RDV | specialiste |
| POST | `/api/rendez-vous/{id}/annuler/` | Annuler RDV | patient, specialiste |
| POST | `/api/rendez-vous/{id}/terminer/` | Terminer RDV | specialiste |

### 8. Consultations PF

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/consultations/` | Liste des consultations | Médical |
| POST | `/api/consultations/` | Créer une consultation | specialiste |
| GET | `/api/consultations/{id}/` | Détails consultation | Médical |
| PUT | `/api/consultations/{id}/` | Modifier consultation | specialiste |
| DELETE | `/api/consultations/{id}/` | Supprimer consultation | super_admin |
| GET | `/api/consultations/{id}/rapport/` | Rapport consultation | Médical |

### 9. Pharmacies

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/pharmacies/` | Liste des pharmacies | Public |
| POST | `/api/pharmacies/` | Créer une pharmacie | super_admin |
| GET | `/api/pharmacies/{id}/` | Détails pharmacie | Public |
| PUT | `/api/pharmacies/{id}/` | Modifier pharmacie | pharmacien |
| DELETE | `/api/pharmacies/{id}/` | Supprimer pharmacie | super_admin |
| POST | `/api/pharmacies/{id}/activer/` | Activer pharmacie | super_admin |
| POST | `/api/pharmacies/{id}/desactiver/` | Désactiver pharmacie | super_admin |
| GET | `/api/pharmacies/{id}/statistiques/` | Statistiques pharmacie | pharmacien |

### 10. Produits

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/produits/` | Liste des produits | Public |
| POST | `/api/produits/` | Créer un produit | super_admin |
| GET | `/api/produits/{id}/` | Détails produit | Public |
| PUT | `/api/produits/{id}/` | Modifier produit | super_admin |
| DELETE | `/api/produits/{id}/` | Supprimer produit | super_admin |
| GET | `/api/produits/search/` | Rechercher produits | Public |

### 11. Stocks

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/stocks-produits/` | Liste des stocks | pharmacien |
| POST | `/api/stocks-produits/` | Créer un stock | pharmacien |
| GET | `/api/stocks-produits/{id}/` | Détails stock | pharmacien |
| PUT | `/api/stocks-produits/{id}/` | Modifier stock | pharmacien |
| DELETE | `/api/stocks-produits/{id}/` | Supprimer stock | pharmacien |
| POST | `/api/stocks-produits/{id}/ajuster/` | Ajuster stock | pharmacien |
| GET | `/api/stocks-produits/rupture/` | Stocks en rupture | pharmacien |

### 12. Ventes

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/ventes/` | Liste des ventes | pharmacien |
| POST | `/api/ventes/` | Créer une vente | pharmacien, employe |
| GET | `/api/ventes/{id}/` | Détails vente | pharmacien |
| PUT | `/api/ventes/{id}/` | Modifier vente | pharmacien |
| DELETE | `/api/ventes/{id}/` | Supprimer vente | pharmacien |
| POST | `/api/ventes/{id}/annuler/` | Annuler vente | pharmacien |
| GET | `/api/ventes/{id}/recu/` | Générer reçu | pharmacien |

### 13. Commandes

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/commandes/` | Liste des commandes | pharmacien |
| POST | `/api/commandes/` | Créer une commande | pharmacien |
| GET | `/api/commandes/{id}/` | Détails commande | pharmacien |
| PUT | `/api/commandes/{id}/` | Modifier commande | pharmacien |
| DELETE | `/api/commandes/{id}/` | Supprimer commande | pharmacien |
| POST | `/api/commandes/{id}/valider/` | Valider commande | pharmacien |
| POST | `/api/commandes/{id}/livrer/` | Livrer commande | pharmacien |
| POST | `/api/commandes/{id}/annuler/` | Annuler commande | pharmacien |

### 14. Ordonnances

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/ordonnances/` | Liste des ordonnances | Médical |
| POST | `/api/ordonnances/` | Créer une ordonnance | specialiste |
| GET | `/api/ordonnances/{id}/` | Détails ordonnance | Médical |
| PUT | `/api/ordonnances/{id}/` | Modifier ordonnance | specialiste |
| DELETE | `/api/ordonnances/{id}/` | Supprimer ordonnance | super_admin |
| GET | `/api/ordonnances/scan-qr/` | Scanner QR code | pharmacien |
| POST | `/api/ordonnances/{id}/dispenser/` | Dispenser ordonnance | pharmacien |
| GET | `/api/ordonnances/{id}/pdf/` | Télécharger PDF | Médical |

### 15. Dossiers Médicaux

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/dossiers-medicaux/` | Liste des dossiers | Médical |
| POST | `/api/dossiers-medicaux/` | Créer un dossier | specialiste |
| GET | `/api/dossiers-medicaux/{id}/` | Détails dossier | Médical |
| PUT | `/api/dossiers-medicaux/{id}/` | Modifier dossier | specialiste |
| DELETE | `/api/dossiers-medicaux/{id}/` | Supprimer dossier | super_admin |
| POST | `/api/dossiers-medicaux/{id}/upload-fichier/` | Upload fichier | specialiste |
| GET | `/api/dossiers-medicaux/{id}/fichiers/` | Liste fichiers | Médical |

### 16. Employés Pharmacie

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/employes/` | Liste des employés | pharmacien |
| POST | `/api/employes/` | Créer un employé | pharmacien |
| GET | `/api/employes/{id}/` | Détails employé | pharmacien |
| PUT | `/api/employes/{id}/` | Modifier employé | pharmacien |
| DELETE | `/api/employes/{id}/` | Supprimer employé | pharmacien |
| POST | `/api/employes/{id}/activer/` | Activer employé | pharmacien |
| POST | `/api/employes/{id}/desactiver/` | Désactiver employé | pharmacien |

### 17. Fournisseurs

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/fournisseurs/` | Liste des fournisseurs | pharmacien |
| POST | `/api/fournisseurs/` | Créer un fournisseur | super_admin |
| GET | `/api/fournisseurs/{id}/` | Détails fournisseur | pharmacien |
| PUT | `/api/fournisseurs/{id}/` | Modifier fournisseur | super_admin |
| DELETE | `/api/fournisseurs/{id}/` | Supprimer fournisseur | super_admin |
| POST | `/api/fournisseurs/{id}/activer/` | Activer fournisseur | super_admin |
| POST | `/api/fournisseurs/{id}/desactiver/` | Désactiver fournisseur | super_admin |
| POST | `/api/fournisseurs/{id}/creer-compte/` | Créer compte utilisateur | super_admin |

### 18. Factures Fournisseurs

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/factures-fournisseurs/` | Liste des factures | pharmacien |
| POST | `/api/factures-fournisseurs/` | Créer une facture | pharmacien |
| GET | `/api/factures-fournisseurs/{id}/` | Détails facture | pharmacien |
| PUT | `/api/factures-fournisseurs/{id}/` | Modifier facture | pharmacien |
| DELETE | `/api/factures-fournisseurs/{id}/` | Supprimer facture | pharmacien |
| POST | `/api/factures-fournisseurs/{id}/valider/` | Valider facture | pharmacien |
| POST | `/api/factures-fournisseurs/{id}/payer/` | Payer facture | pharmacien |

### 19. Notifications

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/notifications/` | Liste des notifications | Tous |
| GET | `/api/notifications/{id}/` | Détails notification | Tous |
| POST | `/api/notifications/{id}/marquer-lue/` | Marquer comme lue | Tous |
| POST | `/api/notifications/marquer-toutes-lues/` | Tout marquer comme lu | Tous |
| GET | `/api/notifications/non-lues/` | Notifications non lues | Tous |

### 20. Statistiques

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/statistiques/` | Statistiques générales | Médical |
| GET | `/api/statistiques/consultations/` | Stats consultations | Médical |
| GET | `/api/statistiques/rendez-vous/` | Stats rendez-vous | Médical |
| GET | `/api/statistiques/stocks/` | Stats stocks | pharmacien |
| GET | `/api/analytics/dashboard/` | Analytics dashboard | super_admin |

### 21. Admin Dashboard

| Méthode | Endpoint | Description | Rôles |
|---------|----------|-------------|-------|
| GET | `/api/admin/system-health/` | Santé du système | super_admin |
| GET | `/api/admin/recent-activity/` | Activité récente | super_admin |
| GET | `/api/admin/system-alerts/` | Alertes système | super_admin |
| GET | `/api/admin/security-stats/` | Stats sécurité | super_admin |
| GET | `/api/admin/security-alerts/` | Alertes sécurité | super_admin |
| GET | `/api/admin/login-attempts/` | Tentatives de connexion | super_admin |
| POST | `/api/admin/broadcast-notification/` | Diffuser notification | super_admin |

---

## Rôles et permissions

### Rôles disponibles

1. **super_admin**: Accès complet à toutes les fonctionnalités
2. **admin_hopital**: Gestion d'un hôpital spécifique
3. **specialiste**: Médecin spécialiste
4. **pharmacien**: Propriétaire de pharmacie
5. **employe_pharmacie**: Employé de pharmacie
6. **agent_enregistrement**: Agent d'enregistrement
7. **patient**: Patient
8. **fournisseur**: Fournisseur de produits

### Matrice de permissions

| Ressource | super_admin | admin_hopital | specialiste | pharmacien | employe | agent | patient |
|-----------|-------------|---------------|-------------|------------|---------|-------|---------|
| Utilisateurs | CRUD | R | R | R | R | R | R (self) |
| Hôpitaux | CRUD | RU (own) | R | R | R | R | R |
| Spécialistes | CRUD | CRUD (own) | RU (self) | R | R | R | R |
| Patients | CRUD | CRUD | CRUD | R | R | CRUD | R (self) |
| RDV | CRUD | R | CRUD (own) | R | R | CRUD | CRUD (own) |
| Consultations | CRUD | R | CRUD (own) | R | R | R | R (own) |
| Pharmacies | CRUD | R | R | RU (own) | R (own) | R | R |
| Produits | CRUD | R | R | R | R | R | R |
| Stocks | CRUD | R | R | CRUD (own) | RU (own) | - | - |
| Ventes | CRUD | R | R | CRUD (own) | CRU (own) | - | - |
| Ordonnances | CRUD | R | CRUD (own) | R | R | - | R (own) |
| Dossiers | CRUD | R | CRUD (own) | R | R | - | R (own) |

**Légende**: C=Create, R=Read, U=Update, D=Delete, (own)=Propres ressources uniquement

---

## Codes de statut HTTP

| Code | Signification | Description |
|------|---------------|-------------|
| 200 | OK | Requête réussie |
| 201 | Created | Ressource créée avec succès |
| 204 | No Content | Suppression réussie |
| 400 | Bad Request | Données invalides |
| 401 | Unauthorized | Non authentifié |
| 403 | Forbidden | Accès refusé |
| 404 | Not Found | Ressource introuvable |
| 500 | Internal Server Error | Erreur serveur |

---

## Pagination

Les listes sont paginées par défaut (50 éléments par page).

**Paramètres de requête**:
- `page`: Numéro de page (défaut: 1)
- `page_size`: Nombre d'éléments par page (max: 100)

**Exemple**:
```
GET /api/patients/?page=2&page_size=20
```

**Response**:
```json
{
  "count": 150,
  "next": "https://api.example.com/api/patients/?page=3",
  "previous": "https://api.example.com/api/patients/?page=1",
  "results": [...]
}
```

---

## Filtrage et recherche

### Filtres

Utilisez les paramètres de requête pour filtrer:

```
GET /api/patients/?sexe=F&age_min=18&age_max=45
GET /api/produits/?categorie=contraceptif&actif=true
GET /api/ventes/?date_debut=2026-01-01&date_fin=2026-01-31
```

### Recherche

Utilisez le paramètre `search`:

```
GET /api/patients/?search=Marie
GET /api/produits/?search=pilule
GET /api/hopitaux/?search=Dakar
```

### Tri

Utilisez le paramètre `ordering`:

```
GET /api/patients/?ordering=nom
GET /api/ventes/?ordering=-date_vente  # Décroissant
GET /api/produits/?ordering=prix_unitaire
```

---

## Exemples de requêtes

### Créer un patient

```bash
curl -X POST https://e-sora.onglalumiere.org/api/patients/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Diallo",
    "prenom": "Fatou",
    "date_naissance": "1995-03-15",
    "sexe": "F",
    "telephone": "+221771234567",
    "email": "fatou.diallo@example.com",
    "adresse": "Dakar, Sénégal"
  }'
```

### Créer un rendez-vous

```bash
curl -X POST https://e-sora.onglalumiere.org/api/rendez-vous/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "specialiste": 2,
    "date_heure": "2026-02-20T10:00:00Z",
    "motif": "Consultation de planning familial",
    "type_consultation": "premiere_visite"
  }'
```

### Créer une vente

```bash
curl -X POST https://e-sora.onglalumiere.org/api/ventes/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pharmacie": 1,
    "client_nom": "Marie Sow",
    "lignes": [
      {
        "produit": 5,
        "quantite": 2,
        "prix_unitaire": 5000
      }
    ],
    "mode_paiement": "especes"
  }'
```

---

## Gestion des erreurs

### Format des erreurs

```json
{
  "error": "Description de l'erreur",
  "detail": "Détails supplémentaires",
  "code": "error_code"
}
```

### Erreurs de validation

```json
{
  "nom": ["Ce champ est requis."],
  "email": ["Entrez une adresse e-mail valide."],
  "date_naissance": ["La date ne peut pas être dans le futur."]
}
```

---

## Rate Limiting

- **Limite**: 1000 requêtes par heure par utilisateur
- **Header de réponse**: `X-RateLimit-Remaining`

---

## Webhooks (À venir)

Les webhooks permettront de recevoir des notifications en temps réel pour:
- Nouveaux rendez-vous
- Commandes validées
- Stocks en rupture
- Nouvelles consultations

---

## Support

- **Email**: support@e-sora.onglalumiere.org
- **Documentation**: https://docs.e-sora.onglalumiere.org
- **Status**: https://status.e-sora.onglalumiere.org

---

**Version**: 1.0.0  
**Dernière mise à jour**: 19 février 2026  
**Format**: OpenAPI 3.0
