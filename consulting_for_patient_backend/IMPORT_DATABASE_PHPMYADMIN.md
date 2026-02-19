# Guide d'importation de la base de données dans phpMyAdmin

## Fichiers disponibles

Deux fichiers d'export ont été créés:

1. **e_sora_export.sql** (285 KB) - Fichier SQL non compressé
2. **e_sora_export.sql.gz** (69 KB) - Fichier SQL compressé (recommandé pour l'upload)

---

## Méthode 1: Import via phpMyAdmin (Recommandé)

### Étape 1: Créer la base de données

1. Connectez-vous à **phpMyAdmin** sur votre cPanel
2. Cliquez sur l'onglet **"Bases de données"** ou **"Databases"**
3. Dans "Créer une base de données", entrez: `e_sora` (ou le nom de votre choix)
4. Sélectionnez l'interclassement: **utf8mb4_unicode_ci**
5. Cliquez sur **"Créer"**

### Étape 2: Sélectionner la base de données

1. Dans le panneau de gauche, cliquez sur la base de données `e_sora` que vous venez de créer
2. La base devrait être vide (0 tables)

### Étape 3: Importer le fichier SQL

1. Cliquez sur l'onglet **"Importer"** ou **"Import"** en haut
2. Cliquez sur **"Choisir un fichier"** ou **"Choose File"**
3. Sélectionnez le fichier **e_sora_export.sql** ou **e_sora_export.sql.gz**
4. Laissez les options par défaut:
   - Format: SQL
   - Jeu de caractères: utf8
5. Cliquez sur **"Exécuter"** ou **"Go"** en bas de la page

### Étape 4: Vérification

1. Attendez que l'import se termine (peut prendre 1-2 minutes)
2. Vous devriez voir un message de succès: "Import réussi"
3. Vérifiez que les tables ont été créées (environ 30+ tables)
4. Cliquez sur quelques tables pour vérifier que les données sont présentes

---

## Méthode 2: Import via ligne de commande SSH (Alternative)

Si le fichier est trop volumineux pour phpMyAdmin:

### Étape 1: Uploader le fichier

Uploadez `e_sora_export.sql.gz` dans votre répertoire home via FTP/SFTP

### Étape 2: Se connecter en SSH

```bash
ssh votre_username@votredomaine.com
```

### Étape 3: Créer la base de données

```bash
mysql -u votre_user -p -e "CREATE DATABASE e_sora CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Étape 4: Importer le fichier

Pour le fichier compressé:
```bash
gunzip < e_sora_export.sql.gz | mysql -u votre_user -p e_sora
```

Pour le fichier non compressé:
```bash
mysql -u votre_user -p e_sora < e_sora_export.sql
```

### Étape 5: Vérifier l'import

```bash
mysql -u votre_user -p e_sora -e "SHOW TABLES;"
```

---

## Méthode 3: Import par morceaux (Si fichier trop volumineux)

Si phpMyAdmin a une limite d'upload (ex: 50MB), vous pouvez diviser le fichier:

### Étape 1: Diviser le fichier SQL

Sur votre machine locale:

```bash
cd consulting_for_patient_backend
split -l 5000 e_sora_export.sql e_sora_part_
```

Cela créera plusieurs fichiers: `e_sora_part_aa`, `e_sora_part_ab`, etc.

### Étape 2: Importer chaque partie

Dans phpMyAdmin, importez chaque fichier dans l'ordre:
1. e_sora_part_aa
2. e_sora_part_ab
3. e_sora_part_ac
4. etc.

---

## Problèmes courants et solutions

### Erreur: "Fichier trop volumineux"

**Solution 1**: Utilisez le fichier compressé `.gz` (phpMyAdmin supporte les fichiers compressés)

**Solution 2**: Augmentez la limite d'upload dans php.ini (via cPanel):
- Allez dans **Select PHP Version** ou **MultiPHP INI Editor**
- Augmentez `upload_max_filesize` à 100M
- Augmentez `post_max_size` à 100M
- Augmentez `max_execution_time` à 300

**Solution 3**: Utilisez la méthode SSH (Méthode 2)

### Erreur: "Timeout lors de l'import"

**Solution**: Augmentez `max_execution_time` dans php.ini ou utilisez SSH

### Erreur: "Table déjà existante"

**Solution**: Supprimez toutes les tables existantes ou supprimez la base et recréez-la

```sql
DROP DATABASE e_sora;
CREATE DATABASE e_sora CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Erreur: "Erreur de syntaxe SQL"

**Solution**: Vérifiez que vous utilisez MySQL 5.7+ ou MariaDB 10.2+

### Erreur: "Caractères mal encodés (é, à, etc.)"

**Solution**: 
1. Assurez-vous que la base de données utilise `utf8mb4_unicode_ci`
2. Dans phpMyAdmin, avant l'import, exécutez:
```sql
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
```

---

## Vérification post-import

### 1. Vérifier le nombre de tables

Dans phpMyAdmin, vous devriez voir environ 30+ tables:
- auth_group
- auth_user
- pf_user
- pf_hopital
- pf_specialite
- pf_specialiste
- pf_patient
- pf_pharmacie
- pf_produit
- pf_ordonnance
- pf_dossiermedical
- etc.

### 2. Vérifier les données

Cliquez sur quelques tables et vérifiez qu'elles contiennent des données:

```sql
SELECT COUNT(*) FROM pf_user;
SELECT COUNT(*) FROM pf_hopital;
SELECT COUNT(*) FROM pf_specialiste;
SELECT COUNT(*) FROM pf_patient;
```

### 3. Tester une requête

```sql
SELECT * FROM pf_user LIMIT 5;
```

---

## Mise à jour des credentials dans Django

Après l'import, mettez à jour votre fichier `.env` sur le serveur:

```env
DATABASE_NAME=e_sora
DATABASE_USER=votre_user_cpanel
DATABASE_PASSWORD=votre_mot_de_passe
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

---

## Sauvegarde régulière

Pour créer des sauvegardes régulières, ajoutez un CRON job dans cPanel:

```bash
0 2 * * * mysqldump -u votre_user -p'votre_password' e_sora | gzip > ~/backups/e_sora_$(date +\%Y\%m\%d).sql.gz
```

Cela créera une sauvegarde quotidienne à 2h du matin.

---

## Informations sur la base de données exportée

- **Nom de la base**: e_sora
- **Taille**: ~285 KB (non compressé), ~69 KB (compressé)
- **Encodage**: UTF-8 (utf8mb4)
- **Tables**: ~30+ tables Django + tables personnalisées
- **Date d'export**: 15 février 2026
- **Version MySQL**: Compatible MySQL 5.7+ / MariaDB 10.2+

---

## Structure des tables principales

### Tables d'authentification
- `auth_user` - Utilisateurs Django (legacy)
- `pf_user` - Utilisateurs personnalisés (nouveau modèle)
- `pf_historiqueconnexion` - Historique des connexions
- `pf_sessionutilisateur` - Sessions actives

### Tables métier
- `pf_hopital` - Hôpitaux
- `pf_specialite` - Spécialités médicales
- `pf_specialiste` - Médecins spécialistes
- `pf_patient` - Patients
- `pf_rendezvous` - Rendez-vous
- `pf_consultationpf` - Consultations de planning familial
- `pf_dossiermedical` - Dossiers médicaux
- `pf_ordonnance` - Ordonnances
- `pf_pharmacie` - Pharmacies
- `pf_produit` - Produits pharmaceutiques
- `pf_ventepharmacie` - Ventes
- `pf_fournisseur` - Fournisseurs
- `pf_facturefournisseur` - Factures fournisseurs

---

## Support

Si vous rencontrez des problèmes:

1. Vérifiez les logs d'erreur de phpMyAdmin
2. Vérifiez la version de MySQL/MariaDB (doit être 5.7+ ou 10.2+)
3. Vérifiez les permissions de l'utilisateur MySQL
4. Contactez le support de votre hébergeur si nécessaire

---

**Note importante**: Gardez une copie locale de votre base de données en sécurité. Ne partagez jamais vos fichiers SQL contenant des données sensibles.
