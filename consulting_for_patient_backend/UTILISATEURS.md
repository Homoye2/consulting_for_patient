# Identifiants des Utilisateurs - Application de Planification Familiale

> **⚠️ ATTENTION : Ce fichier contient des informations sensibles. Ne le partagez pas publiquement.**

**Date de génération :** 14/11/2025 19:06:08

**Total d'utilisateurs :** 6

---

## Utilisateur #1

- **Nom :** Admin Principal
- **Email :** `admin@example.com`
- **Mot de passe :** `admin123`
- **Rôle :** Administrateur (`administrateur`)
- **Statut :** ✅ Actif
- **Staff :** Oui
- **Superuser :** Oui
- **Date d'inscription :** 14/11/2025 19:05:35
- **Dernière connexion :** Jamais

---

## Utilisateur #2

- **Nom :** Dr. Marie Dupont
- **Email :** `medecin@example.com`
- **Mot de passe :** `medecin123`
- **Rôle :** Médecin (`medecin`)
- **Statut :** ✅ Actif
- **Staff :** Non
- **Superuser :** Non
- **Date d'inscription :** 14/11/2025 19:05:39
- **Dernière connexion :** Jamais

---

## Utilisateur #3

- **Nom :** Sage-femme Sophie
- **Email :** `sagefemme@example.com`
- **Mot de passe :** `sagefemme123`
- **Rôle :** Sage-femme (`sage_femme`)
- **Statut :** ✅ Actif
- **Staff :** Non
- **Superuser :** Non
- **Date d'inscription :** 14/11/2025 19:05:42
- **Dernière connexion :** Jamais

---

## Utilisateur #4

- **Nom :** Infirmier Jean
- **Email :** `infirmier@example.com`
- **Mot de passe :** `infirmier123`
- **Rôle :** Infirmier(ère) (`infirmier`)
- **Statut :** ✅ Actif
- **Staff :** Non
- **Superuser :** Non
- **Date d'inscription :** 14/11/2025 19:05:44
- **Dernière connexion :** Jamais

---

## Utilisateur #5

- **Nom :** Pharmacien Paul
- **Email :** `pharmacien@example.com`
- **Mot de passe :** `pharmacien123`
- **Rôle :** Pharmacien (`pharmacien`)
- **Statut :** ✅ Actif
- **Staff :** Non
- **Superuser :** Non
- **Date d'inscription :** 14/11/2025 19:05:48
- **Dernière connexion :** Jamais

---

## Utilisateur #6

- **Nom :** Agent Sarah
- **Email :** `agent@example.com`
- **Mot de passe :** `agent123`
- **Rôle :** Agent d'enregistrement (`agent_enregistrement`)
- **Statut :** ✅ Actif
- **Staff :** Non
- **Superuser :** Non
- **Date d'inscription :** 14/11/2025 19:05:52
- **Dernière connexion :** Jamais

---

## Résumé rapide des identifiants

| Email | Mot de passe | Rôle |
|-------|-------------|------|
| `admin@example.com` | `admin123` | Administrateur |
| `medecin@example.com` | `medecin123` | Médecin |
| `sagefemme@example.com` | `sagefemme123` | Sage-femme |
| `infirmier@example.com` | `infirmier123` | Infirmier(ère) |
| `pharmacien@example.com` | `pharmacien123` | Pharmacien |
| `agent@example.com` | `agent123` | Agent d'enregistrement |

## Notes importantes

1. **Les mots de passe ne sont pas stockés en clair** dans la base de données.
2. **Ces identifiants sont pour le développement/test uniquement.** Changez-les en production !
3. Si vous avez oublié votre mot de passe, contactez un administrateur.
4. Pour créer un nouvel utilisateur, utilisez l'interface d'administration Django ou l'API.
5. Pour réinitialiser un mot de passe, utilisez la commande Django :
   ```bash
   python manage.py changepassword <email>
   ```
6. Pour créer de nouveaux utilisateurs de test, exécutez :
   ```bash
   python create_test_user.py
   ```

## Rôles disponibles

- **administrateur** : Accès complet à toutes les fonctionnalités
- **medecin** : Gestion des patients, consultations, rendez-vous
- **sage_femme** : Gestion des patients, consultations, rendez-vous
- **infirmier** : Gestion des patients, consultations, rendez-vous
- **pharmacien** : Gestion des stocks
- **agent_enregistrement** : Gestion des rendez-vous

