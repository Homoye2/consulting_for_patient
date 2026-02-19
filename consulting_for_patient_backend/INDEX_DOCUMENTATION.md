# 📚 Index de la documentation E-SORA

## 🚨 Vous avez une erreur? Commencez ici!

### Erreur 503 Service Unavailable
**Symptôme:** Le site affiche "503 Service Unavailable"  
**Erreur dans les logs:** `ModuleNotFoundError: No module named '/home/onglsmjm/e_sora'`

**📖 Lisez dans cet ordre:**
1. 🚀 **AIDE_RAPIDE_503.md** ← COMMENCEZ ICI (solution en 2 minutes)
2. 📋 **COMMANDES_RAPIDES_503.md** (commandes détaillées)
3. 📖 **SOLUTION_FINALE_503.md** (explication complète)
4. 🔍 **diagnostic_503.sh** (script de diagnostic)

---

### Erreur 403 Forbidden
**Symptôme:** Le site affiche "403 Forbidden"

**📖 Lisez:**
- **CORRECTION_ERREUR_403.md** (solution complète)

---

## 📁 Documentation par catégorie

### 🚀 Déploiement

#### Backend (Django)
- **DEPLOIEMENT_CPANEL.md** - Guide complet de déploiement sur cPanel
- **DEMARRAGE_RAPIDE_CPANEL.md** - Version courte pour démarrer rapidement
- **INSTALLER_PYTHON_CPANEL.md** - Installer Python 3.12 sur cPanel
- **RECREER_VENV_PYTHON312.md** - Recréer l'environnement virtuel

#### Frontend (React)
- **../GUIDE_DEPLOIEMENT_FRONTEND.md** - Déploiement des 3 applications frontend

#### Base de données
- **IMPORT_DATABASE_PHPMYADMIN.md** - Importer la base de données MySQL
- **e_sora_export.sql** - Export de la base (285 KB)
- **e_sora_export.sql.gz** - Export compressé (69 KB)

---

### 🔧 Résolution de problèmes

#### Erreur 503
- 🚀 **AIDE_RAPIDE_503.md** - Solution rapide (2 minutes)
- 📋 **COMMANDES_RAPIDES_503.md** - Commandes copier-coller
- 📖 **SOLUTION_FINALE_503.md** - Solution détaillée
- 🔍 **diagnostic_503.sh** - Script de diagnostic automatique

#### Erreur 403
- **CORRECTION_ERREUR_403.md** - Correction complète
- **CORRIGER_ERREUR_503.md** - Ancienne version (voir SOLUTION_FINALE_503.md)

#### Erreur Swagger
- **CORRECTION_SWAGGER.md** - Correction des erreurs de génération Swagger

---

### 📖 Documentation API

- **API_DOCUMENTATION_SWAGGER.md** - Documentation complète de l'API
  - 100+ endpoints documentés
  - Authentification et permissions
  - Exemples de requêtes/réponses
  - Codes d'erreur

- **API_COMPLETE_DOCUMENTATION.md** - Documentation alternative
- **API_SWAGGER_DOCUMENTATION.md** - Documentation Swagger

---

### 🏗️ Architecture

- **ARCHITECTURE_DIAGRAM.md** - Diagramme d'architecture du système
- **USERS_AND_ROLES_SUMMARY.md** - Résumé des utilisateurs et rôles

---

### 🧹 Maintenance

- **cleanup.sh** - Script de nettoyage automatique
- **FICHIERS_NETTOYES.md** - Rapport des fichiers nettoyés
- **.gitignore** - Fichiers à ignorer dans Git

---

### 📊 Améliorations

- **AMELIORATIONS_DOSSIERS_MEDICAUX.md** - Améliorations des dossiers médicaux

---

### 🗄️ Base de données

- **MIGRATION_MYSQL.md** - Guide de migration MySQL
- **e_sora_export.sql** - Export SQL (285 KB)
- **e_sora_export.sql.gz** - Export compressé (69 KB)
- **e_sora_backup_20260215_215548.sql** - Backup du 15 février

---

## 🎯 Guides par tâche

### Je veux déployer le backend sur cPanel
1. **DEPLOIEMENT_CPANEL.md** - Guide complet
2. **INSTALLER_PYTHON_CPANEL.md** - Installer Python 3.12
3. **IMPORT_DATABASE_PHPMYADMIN.md** - Importer la base de données

### Je veux déployer le frontend
1. **../GUIDE_DEPLOIEMENT_FRONTEND.md** - Guide complet pour les 3 apps

### J'ai une erreur 503
1. 🚀 **AIDE_RAPIDE_503.md** - Solution rapide
2. 📋 **COMMANDES_RAPIDES_503.md** - Commandes détaillées
3. 🔍 **diagnostic_503.sh** - Diagnostic automatique

### J'ai une erreur 403
1. **CORRECTION_ERREUR_403.md** - Solution complète

### Je veux comprendre l'API
1. **API_DOCUMENTATION_SWAGGER.md** - Documentation complète

### Je veux nettoyer le projet
1. **cleanup.sh** - Exécuter le script de nettoyage

### Je veux recréer l'environnement virtuel
1. **RECREER_VENV_PYTHON312.md** - Guide complet

---

## 📝 Scripts utiles

### Scripts shell
- **cleanup.sh** - Nettoyage automatique
- **diagnostic_503.sh** - Diagnostic erreur 503
- **create_migrations.sh** - Créer les migrations
- **fix_error_500.sh** - Corriger erreur 500
- **start_server.sh** - Démarrer le serveur

### Scripts Python
- **manage.py** - Script Django principal
- **seed_database.py** - Peupler la base de données
- **seed_produits.py** - Peupler les produits
- **setup_mysql.py** - Configuration MySQL
- **verify_config.py** - Vérifier la configuration
- **diagnostic.py** - Diagnostic Python
- **generate_diagram.py** - Générer le diagramme d'architecture

---

## 🆘 Aide rapide par symptôme

| Symptôme | Document à lire |
|----------|----------------|
| 503 Service Unavailable | 🚀 **AIDE_RAPIDE_503.md** |
| 403 Forbidden | **CORRECTION_ERREUR_403.md** |
| 500 Internal Server Error | Vérifier les logs Django |
| Erreur Swagger | **CORRECTION_SWAGGER.md** |
| Problème Python | **INSTALLER_PYTHON_CPANEL.md** |
| Problème base de données | **IMPORT_DATABASE_PHPMYADMIN.md** |
| Problème déploiement | **DEPLOIEMENT_CPANEL.md** |

---

## 📞 Ordre de lecture recommandé

### Pour un nouveau déploiement:
1. **DEPLOIEMENT_CPANEL.md** - Comprendre le processus
2. **INSTALLER_PYTHON_CPANEL.md** - Installer Python
3. **IMPORT_DATABASE_PHPMYADMIN.md** - Importer la base
4. **DEMARRAGE_RAPIDE_CPANEL.md** - Démarrer rapidement

### Pour résoudre une erreur 503:
1. 🚀 **AIDE_RAPIDE_503.md** - Solution immédiate
2. 📋 **COMMANDES_RAPIDES_503.md** - Si besoin de plus de détails
3. 🔍 **diagnostic_503.sh** - Si le problème persiste

### Pour comprendre l'API:
1. **API_DOCUMENTATION_SWAGGER.md** - Documentation complète
2. Accéder à `/api/swagger/` sur le serveur

---

## 🎓 Niveau de difficulté

| Document | Difficulté | Temps |
|----------|-----------|-------|
| 🚀 AIDE_RAPIDE_503.md | ⭐ Facile | 2 min |
| COMMANDES_RAPIDES_503.md | ⭐ Facile | 5 min |
| DEMARRAGE_RAPIDE_CPANEL.md | ⭐⭐ Moyen | 15 min |
| DEPLOIEMENT_CPANEL.md | ⭐⭐⭐ Avancé | 30 min |
| API_DOCUMENTATION_SWAGGER.md | ⭐⭐ Moyen | Référence |

---

## 📦 Fichiers de données

- **e_sora_export.sql** (285 KB) - Export base de données
- **e_sora_export.sql.gz** (69 KB) - Export compressé
- **e_sora_backup_20260215_215548.sql** - Backup du 15 février
- **requirements.txt** - Dépendances Python
- **requirements_python36.txt** - Dépendances Python 3.6

---

## 🔗 Liens rapides

### Sur le serveur
- API: `https://e-sora.onglalumiere.org/api/`
- Swagger: `https://e-sora.onglalumiere.org/api/swagger/`
- Admin: `https://e-sora.onglalumiere.org/admin/`

### Documentation en ligne
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- cPanel: https://docs.cpanel.net/

---

## 📅 Dernière mise à jour

**Date:** 19 février 2026  
**Version:** 1.0.0  
**Status:** ✅ Documentation complète

---

## 💡 Conseil

**Vous avez une erreur 503?**  
👉 Commencez par **AIDE_RAPIDE_503.md** - c'est le plus rapide!

**Vous déployez pour la première fois?**  
👉 Lisez **DEPLOIEMENT_CPANEL.md** en entier d'abord.

**Vous voulez juste que ça marche?**  
👉 Suivez **DEMARRAGE_RAPIDE_CPANEL.md** étape par étape.
