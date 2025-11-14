# Cahier des charges — Application de gestion de la planification familiale

**Projet :** Application de gestion de la planification familiale

**Cas :** Centre Hospitalier Abass Ndao

**Stack proposée :** Backend — Django (Django REST Framework) | Frontend — React (Vite.js)

---

## 1. Contexte et objectifs

Le Centre Hospitalier Abass Ndao souhaite disposer d'une application web pour :
- Gérer les dossiers patients liés à la planification familiale (PF)
- Suivre les consultations PF et l'historique des méthodes contraceptives
- Gérer les rendez-vous et l'agenda des professionnels de santé
- Contrôler les stocks de contraceptifs et générer des alertes de rupture
- Produire des rapports statistiques (mensuels/annuels)

**Objectifs fonctionnels principaux :**
1. Centraliser les informations patients et leur historique PF.
2. Faciliter la prise de rendez-vous et le suivi des consultations.
3. Garantir la traçabilité des actes et prescriptions.
4. Gérer les stocks et alertes de ruptures.
5. Fournir des tableaux de bord et rapports pour la prise de décision.


## 2. Périmètre fonctionnel

### 2.1 Gestion des patients
- Création, lecture, mise à jour, suppression (CRUD) des dossiers patients.
- Fiche patient détaillée (informations personnelles, antécédents, allergies, grossesses, etc.).
- Recherche avancée et filtrage.

### 2.2 Consultations PF
- Enregistrement des consultations (anamnèse, examen, méthode proposée/posée, effets secondaires).
- Archivage des notes et pièces jointes (PDF, images).

### 2.3 Rendez-vous
- Prise de rendez-vous par le personnel (et, si souhaité, par les patients via un futur portail).
- Agenda par professionnel.
- Notifications / rappels (optionnel).

### 2.4 Gestion des méthodes contraceptives et stocks
- Catalogue des méthodes contraceptives.
- Gestion du stock (entrées, sorties, inventaire périodique).
- Alertes de rupture de stock (seuil configurable).

### 2.5 Utilisateurs et rôles
- Comptes pour : administrateur, médecin, sage-femme, infirmier(ère), pharmacien, agent d’enregistrement.
- Gestion des permissions (CRUD limité selon rôle).

### 2.6 Rapports et statistiques
- Nombre de consultations par période.
- Distribution des méthodes utilisées.
- Taux d’assiduité des rendez-vous.


## 3. Exigences non-fonctionnelles

- **Sécurité des données :** chiffrement au repos et en transit (HTTPS), gestion rigoureuse des accès, journaux d’audit.
- **Confidentialité :** conformité aux bonnes pratiques pour les données de santé (respect de la confidentialité).
- **Performance :** pagination pour listes volumineuses, indexes DB sur champs fréquemment recherchés.
- **Scalabilité :** architecture modulaire backend RESTful et frontend découplé.
- **Maintenabilité :** code propre, tests unitaires et documentation API (Swagger).


## 4. Architecture technique proposée

- **Backend :** Django + Django REST Framework, PostgreSQL, SimpleJWT pour l’authentification, Celery + Redis (pour tâches en arrière-plan comme notifications).
- **Frontend :** React + Vite, TailwindCSS ou MUI, Axios pour appels API.
- **Déploiement :** Docker, CI/CD (GitHub Actions), hébergement sur VPS/Cloud (DigitalOcean, AWS, ou cPanel selon besoins).


## 5. Modèles de données (principaux)
- **User (Custom)** : id, nom, email, rôle, hashed_password, is_active
- **Patient** : id, nom, prénom, dob, sexe, téléphone, adresse, antécédents
- **ConsultationPF** : id, patient_id, professionnel_id, date, notes, méthode_prescrite_id, observation
- **MethodeContraceptive** : id, nom, catégorie, description
- **StockItem** : id, methode_id, quantité_disponible, seuil_alerte
- **RendezVous** : id, patient_id, professionnel_id, date_heure, statut
- **Prescription / Acte** : id, consultation_id, produit_id, dosage, remarque

*(Les schémas UML détaillés sont fournis en fichiers PNG accompagnant ce cahier de charges.)*


## 6. Sécurité et conformité
- HTTPS obligatoire.
- Authentification JWT (access + refresh tokens).
- Roles & permissions granulaire.
- Sauvegardes régulières de la base de données.
- Logs d’accès et d’audit.


## 7. Plan de déploiement et livrables
- **Phase 1 (MVP, 4–6 semaines)** : Authentification, CRUD patients, consultations, rendez-vous, gestion simple des stocks, dashboard minimal.
- **Phase 2 (6–8 semaines)** : Notifications, rapports avancés, import/export données, tests et sécurité améliorée.
- **Livrables** : code source (backend + frontend), documentation technique, documentation utilisateur, jeux de données de test, schémas UML.


## 8. Tests et validation
- Tests unitaires pour le backend (pytest / Django tests).
- Tests d’intégration pour API.
- Tests manuels de cas métier (prise de RDV, pose méthode, sortie stock).


## 9. Maintenance
- Contrat de maintenance (option) : correctifs, mises à jour de sécurité, évolution fonctionnelle.


## 10. Annexes
- Diagrammes UML fournis :
  - `class_diagram.png` (Diagramme de classes / modèle de données)
  - `usecase_diagram.png` (Diagramme des cas d'utilisation)
  - `sequence_consultation.png` (Diagramme de séquence - consultation PF)


---

*Fin du cahier des charges.*

