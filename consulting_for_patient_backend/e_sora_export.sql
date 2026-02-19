-- MySQL dump 10.13  Distrib 9.5.0, for macos26.1 (arm64)
--
-- Host: localhost    Database: e_sora
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Contenu de la page d\'accueil',6,'add_landingpagecontent'),(22,'Can change Contenu de la page d\'accueil',6,'change_landingpagecontent'),(23,'Can delete Contenu de la page d\'accueil',6,'delete_landingpagecontent'),(24,'Can view Contenu de la page d\'accueil',6,'view_landingpagecontent'),(25,'Can add Méthode contraceptive',7,'add_methodecontraceptive'),(26,'Can change Méthode contraceptive',7,'change_methodecontraceptive'),(27,'Can delete Méthode contraceptive',7,'delete_methodecontraceptive'),(28,'Can view Méthode contraceptive',7,'view_methodecontraceptive'),(29,'Can add Spécialité',8,'add_specialite'),(30,'Can change Spécialité',8,'change_specialite'),(31,'Can delete Spécialité',8,'delete_specialite'),(32,'Can view Spécialité',8,'view_specialite'),(33,'Can add Utilisateur',9,'add_user'),(34,'Can change Utilisateur',9,'change_user'),(35,'Can delete Utilisateur',9,'delete_user'),(36,'Can view Utilisateur',9,'view_user'),(37,'Can add Hôpital',10,'add_hopital'),(38,'Can change Hôpital',10,'change_hopital'),(39,'Can delete Hôpital',10,'delete_hopital'),(40,'Can view Hôpital',10,'view_hopital'),(41,'Can add Patient',11,'add_patient'),(42,'Can change Patient',11,'change_patient'),(43,'Can delete Patient',11,'delete_patient'),(44,'Can view Patient',11,'view_patient'),(45,'Can add Message de contact',12,'add_contactmessage'),(46,'Can change Message de contact',12,'change_contactmessage'),(47,'Can delete Message de contact',12,'delete_contactmessage'),(48,'Can view Message de contact',12,'view_contactmessage'),(49,'Can add Consultation PF',13,'add_consultationpf'),(50,'Can change Consultation PF',13,'change_consultationpf'),(51,'Can delete Consultation PF',13,'delete_consultationpf'),(52,'Can view Consultation PF',13,'view_consultationpf'),(53,'Can add Pharmacie',14,'add_pharmacie'),(54,'Can change Pharmacie',14,'change_pharmacie'),(55,'Can delete Pharmacie',14,'delete_pharmacie'),(56,'Can view Pharmacie',14,'view_pharmacie'),(57,'Can add Prescription',15,'add_prescription'),(58,'Can change Prescription',15,'change_prescription'),(59,'Can delete Prescription',15,'delete_prescription'),(60,'Can view Prescription',15,'view_prescription'),(61,'Can add Commande Pharmacie',16,'add_commandepharmacie'),(62,'Can change Commande Pharmacie',16,'change_commandepharmacie'),(63,'Can delete Commande Pharmacie',16,'delete_commandepharmacie'),(64,'Can view Commande Pharmacie',16,'view_commandepharmacie'),(65,'Can add Produit',17,'add_produit'),(66,'Can change Produit',17,'change_produit'),(67,'Can delete Produit',17,'delete_produit'),(68,'Can view Produit',17,'view_produit'),(69,'Can add Ligne Commande',18,'add_lignecommande'),(70,'Can change Ligne Commande',18,'change_lignecommande'),(71,'Can delete Ligne Commande',18,'delete_lignecommande'),(72,'Can view Ligne Commande',18,'view_lignecommande'),(73,'Can add Rapport Consultation',19,'add_rapportconsultation'),(74,'Can change Rapport Consultation',19,'change_rapportconsultation'),(75,'Can delete Rapport Consultation',19,'delete_rapportconsultation'),(76,'Can view Rapport Consultation',19,'view_rapportconsultation'),(77,'Can add Rendez-vous',20,'add_rendezvous'),(78,'Can change Rendez-vous',20,'change_rendezvous'),(79,'Can delete Rendez-vous',20,'delete_rendezvous'),(80,'Can view Rendez-vous',20,'view_rendezvous'),(81,'Can add Notification',21,'add_notification'),(82,'Can change Notification',21,'change_notification'),(83,'Can delete Notification',21,'delete_notification'),(84,'Can view Notification',21,'view_notification'),(85,'Can add Service',22,'add_service'),(86,'Can change Service',22,'change_service'),(87,'Can delete Service',22,'delete_service'),(88,'Can view Service',22,'view_service'),(89,'Can add Spécialiste',23,'add_specialiste'),(90,'Can change Spécialiste',23,'change_specialiste'),(91,'Can delete Spécialiste',23,'delete_specialiste'),(92,'Can view Spécialiste',23,'view_specialiste'),(93,'Can add Disponibilité Spécialiste',24,'add_disponibilitespecialiste'),(94,'Can change Disponibilité Spécialiste',24,'change_disponibilitespecialiste'),(95,'Can delete Disponibilité Spécialiste',24,'delete_disponibilitespecialiste'),(96,'Can view Disponibilité Spécialiste',24,'view_disponibilitespecialiste'),(97,'Can add Avis Spécialiste',25,'add_avisspecialiste'),(98,'Can change Avis Spécialiste',25,'change_avisspecialiste'),(99,'Can delete Avis Spécialiste',25,'delete_avisspecialiste'),(100,'Can view Avis Spécialiste',25,'view_avisspecialiste'),(101,'Can add Stock',26,'add_stockitem'),(102,'Can change Stock',26,'change_stockitem'),(103,'Can delete Stock',26,'delete_stockitem'),(104,'Can view Stock',26,'view_stockitem'),(105,'Can add Mouvement de stock',27,'add_mouvementstock'),(106,'Can change Mouvement de stock',27,'change_mouvementstock'),(107,'Can delete Mouvement de stock',27,'delete_mouvementstock'),(108,'Can view Mouvement de stock',27,'view_mouvementstock'),(109,'Can add Stock Produit',28,'add_stockproduit'),(110,'Can change Stock Produit',28,'change_stockproduit'),(111,'Can delete Stock Produit',28,'delete_stockproduit'),(112,'Can view Stock Produit',28,'view_stockproduit'),(113,'Can add Valeur',29,'add_value'),(114,'Can change Valeur',29,'change_value'),(115,'Can delete Valeur',29,'delete_value'),(116,'Can view Valeur',29,'view_value'),(117,'Can add Session utilisateur',30,'add_sessionutilisateur'),(118,'Can change Session utilisateur',30,'change_sessionutilisateur'),(119,'Can delete Session utilisateur',30,'delete_sessionutilisateur'),(120,'Can view Session utilisateur',30,'view_sessionutilisateur'),(121,'Can add Historique de connexion',31,'add_historiqueconnexion'),(122,'Can change Historique de connexion',31,'change_historiqueconnexion'),(123,'Can delete Historique de connexion',31,'delete_historiqueconnexion'),(124,'Can view Historique de connexion',31,'view_historiqueconnexion'),(125,'Can add Vente Pharmacie',32,'add_ventepharmacie'),(126,'Can change Vente Pharmacie',32,'change_ventepharmacie'),(127,'Can delete Vente Pharmacie',32,'delete_ventepharmacie'),(128,'Can view Vente Pharmacie',32,'view_ventepharmacie'),(129,'Can add Ligne Vente',33,'add_lignevente'),(130,'Can change Ligne Vente',33,'change_lignevente'),(131,'Can delete Ligne Vente',33,'delete_lignevente'),(132,'Can view Ligne Vente',33,'view_lignevente'),(133,'Can add Employé Pharmacie',34,'add_employepharmacie'),(134,'Can change Employé Pharmacie',34,'change_employepharmacie'),(135,'Can delete Employé Pharmacie',34,'delete_employepharmacie'),(136,'Can view Employé Pharmacie',34,'view_employepharmacie'),(137,'Can add Registre',35,'add_registre'),(138,'Can change Registre',35,'change_registre'),(139,'Can delete Registre',35,'delete_registre'),(140,'Can view Registre',35,'view_registre'),(141,'Can add Ordonnance',36,'add_ordonnance'),(142,'Can change Ordonnance',36,'change_ordonnance'),(143,'Can delete Ordonnance',36,'delete_ordonnance'),(144,'Can view Ordonnance',36,'view_ordonnance'),(145,'Can add Ligne d\'ordonnance',37,'add_ligneordonnance'),(146,'Can change Ligne d\'ordonnance',37,'change_ligneordonnance'),(147,'Can delete Ligne d\'ordonnance',37,'delete_ligneordonnance'),(148,'Can view Ligne d\'ordonnance',37,'view_ligneordonnance'),(149,'Can add Dossier médical',38,'add_dossiermedical'),(150,'Can change Dossier médical',38,'change_dossiermedical'),(151,'Can delete Dossier médical',38,'delete_dossiermedical'),(152,'Can view Dossier médical',38,'view_dossiermedical'),(153,'Can add Fichier de dossier médical',39,'add_fichierdossiermedical'),(154,'Can change Fichier de dossier médical',39,'change_fichierdossiermedical'),(155,'Can delete Fichier de dossier médical',39,'delete_fichierdossiermedical'),(156,'Can view Fichier de dossier médical',39,'view_fichierdossiermedical'),(157,'Can add Fournisseur',40,'add_fournisseur'),(158,'Can change Fournisseur',40,'change_fournisseur'),(159,'Can delete Fournisseur',40,'delete_fournisseur'),(160,'Can view Fournisseur',40,'view_fournisseur'),(161,'Can add Facture Fournisseur',41,'add_facturefournisseur'),(162,'Can change Facture Fournisseur',41,'change_facturefournisseur'),(163,'Can delete Facture Fournisseur',41,'delete_facturefournisseur'),(164,'Can view Facture Fournisseur',41,'view_facturefournisseur'),(165,'Can add Ligne de Facture Fournisseur',42,'add_lignefacturefournisseur'),(166,'Can change Ligne de Facture Fournisseur',42,'change_lignefacturefournisseur'),(167,'Can delete Ligne de Facture Fournisseur',42,'delete_lignefacturefournisseur'),(168,'Can view Ligne de Facture Fournisseur',42,'view_lignefacturefournisseur');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `avis_specialistes`
--

DROP TABLE IF EXISTS `avis_specialistes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `avis_specialistes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `note` int NOT NULL,
  `commentaire` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `ponctualite` int DEFAULT NULL,
  `ecoute` int DEFAULT NULL,
  `explication` int DEFAULT NULL,
  `recommande` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  `rendez_vous_id` bigint NOT NULL,
  `specialiste_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rendez_vous_id` (`rendez_vous_id`),
  UNIQUE KEY `avis_specialistes_specialiste_id_patient_i_9a15e381_uniq` (`specialiste_id`,`patient_id`,`rendez_vous_id`),
  KEY `avis_specialistes_patient_id_a5ae5d78_fk_patients_id` (`patient_id`),
  CONSTRAINT `avis_specialistes_patient_id_a5ae5d78_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  CONSTRAINT `avis_specialistes_rendez_vous_id_65f95d67_fk_rendez_vous_id` FOREIGN KEY (`rendez_vous_id`) REFERENCES `rendez_vous` (`id`),
  CONSTRAINT `avis_specialistes_specialiste_id_fab33785_fk_specialistes_id` FOREIGN KEY (`specialiste_id`) REFERENCES `specialistes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `avis_specialistes`
--

LOCK TABLES `avis_specialistes` WRITE;
/*!40000 ALTER TABLE `avis_specialistes` DISABLE KEYS */;
/*!40000 ALTER TABLE `avis_specialistes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commandes_pharmacies`
--

DROP TABLE IF EXISTS `commandes_pharmacies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `commandes_pharmacies` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_commande` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `statut` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `montant_total` decimal(10,2) NOT NULL,
  `prescription_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes_patient` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes_pharmacie` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_commande` datetime(6) NOT NULL,
  `date_confirmation` datetime(6) DEFAULT NULL,
  `date_preparation` datetime(6) DEFAULT NULL,
  `date_prete` datetime(6) DEFAULT NULL,
  `date_recuperation` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `patient_id` bigint NOT NULL,
  `pharmacie_id` bigint NOT NULL,
  `prescription_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_commande` (`numero_commande`),
  KEY `commandes_p_numero__09a399_idx` (`numero_commande`),
  KEY `commandes_p_patient_186957_idx` (`patient_id`,`statut`),
  KEY `commandes_p_pharmac_98e40b_idx` (`pharmacie_id`,`statut`),
  KEY `commandes_p_date_co_a21b10_idx` (`date_commande`),
  KEY `commandes_pharmacies_prescription_id_a8309188_fk_prescript` (`prescription_id`),
  CONSTRAINT `commandes_pharmacies_patient_id_d24c425f_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  CONSTRAINT `commandes_pharmacies_pharmacie_id_67e497eb_fk_pharmacies_id` FOREIGN KEY (`pharmacie_id`) REFERENCES `pharmacies` (`id`),
  CONSTRAINT `commandes_pharmacies_prescription_id_a8309188_fk_prescript` FOREIGN KEY (`prescription_id`) REFERENCES `prescriptions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commandes_pharmacies`
--

LOCK TABLES `commandes_pharmacies` WRITE;
/*!40000 ALTER TABLE `commandes_pharmacies` DISABLE KEYS */;
INSERT INTO `commandes_pharmacies` VALUES (61,'CMD33805255','preparee',6600.00,'','Mince quart ouvrir ton bouche vêtement soit. Course gauche écouter importance douze autre.','','2025-12-27 04:08:59.700242',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.700254','2025-12-27 04:08:59.705655',142,12,NULL),(62,'CMD78542898','confirmee',2250.00,'','','','2025-12-27 04:08:59.706932',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.706942','2025-12-27 04:08:59.708567',105,11,NULL),(63,'CMD26404174','confirmee',3200.00,'','','[06/01/2026 02:02] Votre commande a été confirmée ! Nous commençons la préparation immédiatement.','2025-12-27 04:08:59.709663','2026-01-06 02:02:29.970882',NULL,NULL,NULL,'2025-12-27 04:08:59.709674','2026-01-06 02:02:29.971064',147,11,NULL),(64,'CMD31910209','confirmee',5750.00,'','','','2025-12-27 04:08:59.716318',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.716328','2025-12-27 04:08:59.718751',123,14,NULL),(65,'CMD81211000','recuperee',4200.00,'','Ton on ruine comme peau. Ainsi parmi lueur reprendre créer énergie. Importer propre sourire.','','2025-12-27 04:08:59.719815',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.719825','2026-01-06 01:25:14.048660',108,11,NULL),(66,'CMD54001358','confirmee',4900.00,'','Beauté conseil joli. Avant visage champ.','','2025-12-27 04:08:59.722537',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.722546','2025-12-27 04:08:59.723918',144,13,NULL),(67,'CMD92272987','confirmee',5200.00,'','Entre recherche pas risquer bientôt. Rire demi lien passé après.','','2025-12-27 04:08:59.724942',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.724951','2025-12-27 04:08:59.731490',116,15,NULL),(68,'CMD56925122','recuperee',2200.00,'','','','2025-12-27 04:08:59.732650',NULL,NULL,NULL,'2026-01-06 01:32:49.919403','2025-12-27 04:08:59.732661','2026-01-06 01:32:49.919658',133,11,NULL),(69,'CMD47454468','confirmee',4500.00,'','Trop pays mort odeur. Soudain puisque jeunesse.','','2025-12-27 04:08:59.735566',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.735602','2025-12-27 04:08:59.737283',128,14,NULL),(70,'CMD28817980','confirmee',15300.00,'','','','2025-12-27 04:08:59.737962',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.737975','2025-12-27 04:08:59.740233',110,14,NULL),(71,'CMD03230719','recuperee',13900.00,'','Devoir complètement posséder énorme parfaitement politique. Même profiter confondre.','','2025-12-27 04:08:59.741408',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.741420','2026-01-06 00:50:52.281563',140,11,NULL),(72,'CMD27868273','recuperee',8200.00,'','Étranger sommet user respirer croire ligne sur. Baisser mourir hésiter retrouver avoir.','','2025-12-27 04:08:59.744941',NULL,NULL,NULL,'2026-01-05 01:00:54.819281','2025-12-27 04:08:59.744953','2026-01-07 01:00:54.842368',112,11,NULL),(73,'CMD45402256','recuperee',3200.00,'','Décider d\'autres profondément mais. Vêtement tout depuis naturellement jeu contenter.','','2025-12-27 04:08:59.748055',NULL,NULL,NULL,'2026-01-06 01:00:54.819281','2025-12-27 04:08:59.748065','2026-01-07 01:00:54.840497',116,11,NULL),(74,'CMD22585410','confirmee',10200.00,'','Maintenant douceur heure. Seigneur puisque étaler. Payer atteindre joie pitié tandis que fenêtre.','','2025-12-27 04:08:59.750930',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.750941','2025-12-27 04:08:59.752866',111,15,NULL),(75,'CMD97969557','confirmee',9000.00,'','Membre entre femme difficile. Retourner billet étudier repas. Devenir où camarade le.','','2025-12-27 04:08:59.753828',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.753838','2025-12-27 04:08:59.755698',109,14,NULL),(76,'CMD84774146','preparee',4750.00,'','Nerveux as longtemps grain oiseau charge sept forêt. Rencontrer quitter ministre vérité noir.','','2025-12-27 04:08:59.756317',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.756326','2025-12-27 04:08:59.758156',135,15,NULL),(77,'CMD46481745','en_attente',8300.00,'','Peur intéresser haut épaule. Long détruire entrée glace surveiller beau.','','2025-12-27 04:08:59.758779',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.758789','2025-12-27 04:08:59.762427',130,12,NULL),(78,'CMD15998170','en_attente',15100.00,'','','','2025-12-27 04:08:59.765102',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.765111','2025-12-27 04:08:59.771139',147,14,NULL),(79,'CMD32307338','preparee',5500.00,'','Penser durer couler ruine. Dame manquer faim arrêter. Reculer chasse retirer soldat verser voilà.','','2025-12-27 04:08:59.772251',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.772261','2025-12-27 04:08:59.773760',101,12,NULL),(80,'CMD02746181','preparee',11250.00,'','Feu caractère mode lever. Énorme travers donc absence beau an.','','2025-12-27 04:08:59.775041',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.775133','2025-12-27 04:08:59.778198',117,14,NULL),(81,'CMD36724331','en_attente',7350.00,'','Saisir pourtant accent cours projet voix propos. Visite avis fixer traverser acte mourir étendre.','','2025-12-27 04:08:59.779110',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.779120','2025-12-27 04:08:59.782388',141,15,NULL),(82,'CMD47798120','recuperee',6900.00,'','Appel déposer prochain corde grave quartier.','','2025-12-27 04:08:59.784040',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.784052','2025-12-27 04:08:59.787740',122,12,NULL),(83,'CMD24059388','recuperee',6600.00,'','','','2025-12-27 04:08:59.788489',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.788500','2025-12-27 04:08:59.793602',146,12,NULL),(84,'CMD58710057','confirmee',3000.00,'','Carte femme du parfois envelopper arme coin.','','2025-12-27 04:08:59.794390',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.794402','2025-12-27 04:08:59.796121',129,15,NULL),(85,'CMD88447856','preparee',5700.00,'','Petit nuit frère poussière. Courir quelque quinze. Tapis bois an lui bouche.','','2025-12-27 04:08:59.796848',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.796858','2025-12-27 04:08:59.799412',101,15,NULL),(86,'CMD57935034','confirmee',5950.00,'','Ancien recherche fille saint queue sourire.','','2025-12-27 04:08:59.800216',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.800227','2025-12-27 04:08:59.804327',149,13,NULL),(87,'CMD68451963','confirmee',18500.00,'','','','2025-12-27 04:08:59.805045',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.805054','2025-12-27 04:08:59.810941',121,15,NULL),(88,'CMD39071358','recuperee',7500.00,'','Autrefois article fois angoisse rayon principe grâce prison.','','2025-12-27 04:08:59.811810',NULL,NULL,NULL,'2026-01-07 01:00:54.819281','2025-12-27 04:08:59.811822','2026-01-07 01:00:54.824597',123,11,NULL),(89,'CMD10458671','preparee',5500.00,'','Miser certainement assister métier. Saint demande durant apporter droite rire.','','2025-12-27 04:08:59.814253',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.814263','2025-12-27 04:08:59.816385',105,12,NULL),(90,'CMD15942934','preparee',4700.00,'','Rapide placer peuple bas dangereux froid arrêter. Discussion tard expression herbe leur appartenir.','','2025-12-27 04:08:59.817792',NULL,NULL,NULL,NULL,'2025-12-27 04:08:59.817802','2025-12-27 04:08:59.819669',145,14,NULL);
/*!40000 ALTER TABLE `commandes_pharmacies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultations_pf`
--

DROP TABLE IF EXISTS `consultations_pf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultations_pf` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `anamnese` longtext COLLATE utf8mb4_unicode_ci,
  `examen` longtext COLLATE utf8mb4_unicode_ci,
  `methode_posee` tinyint(1) NOT NULL,
  `effets_secondaires` longtext COLLATE utf8mb4_unicode_ci,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `observation` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `hopital_id` bigint DEFAULT NULL,
  `methode_prescite_id` bigint DEFAULT NULL,
  `methode_proposee_id` bigint DEFAULT NULL,
  `patient_id` bigint NOT NULL,
  `rendez_vous_id` bigint DEFAULT NULL,
  `specialiste_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `consultations_pf_rendez_vous_id_f6d3a3e7_fk_rendez_vous_id` (`rendez_vous_id`),
  KEY `consultatio_date_84c806_idx` (`date`),
  KEY `consultatio_patient_0b408e_idx` (`patient_id`,`date`),
  KEY `consultatio_special_d53c55_idx` (`specialiste_id`,`date`),
  KEY `consultatio_hopital_4a5002_idx` (`hopital_id`),
  KEY `consultations_pf_methode_prescite_id_8014b804_fk_methodes_` (`methode_prescite_id`),
  KEY `consultations_pf_methode_proposee_id_02add518_fk_methodes_` (`methode_proposee_id`),
  CONSTRAINT `consultations_pf_hopital_id_a8f611ec_fk_hopitaux_id` FOREIGN KEY (`hopital_id`) REFERENCES `hopitaux` (`id`),
  CONSTRAINT `consultations_pf_methode_prescite_id_8014b804_fk_methodes_` FOREIGN KEY (`methode_prescite_id`) REFERENCES `methodes_contraceptives` (`id`),
  CONSTRAINT `consultations_pf_methode_proposee_id_02add518_fk_methodes_` FOREIGN KEY (`methode_proposee_id`) REFERENCES `methodes_contraceptives` (`id`),
  CONSTRAINT `consultations_pf_patient_id_f2db0df8_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  CONSTRAINT `consultations_pf_rendez_vous_id_f6d3a3e7_fk_rendez_vous_id` FOREIGN KEY (`rendez_vous_id`) REFERENCES `rendez_vous` (`id`),
  CONSTRAINT `consultations_pf_specialiste_id_eed7cd56_fk_specialistes_id` FOREIGN KEY (`specialiste_id`) REFERENCES `specialistes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultations_pf`
--

LOCK TABLES `consultations_pf` WRITE;
/*!40000 ALTER TABLE `consultations_pf` DISABLE KEYS */;
INSERT INTO `consultations_pf` VALUES (44,'2025-10-28 09:00:06.656450','Être avant violent satisfaire dresser rire sommet hier.\nPrès rendre désirer nombre as empêcher. Danser détruire face avouer toi.\nRue expression noir politique volonté. Perdre comprendre désespoir gens. Recommencer si hier au bas il.\nJuger loi blond devenir signe. Après conclure chat avancer.','Durant suivant pluie ici même. Proposer chaise sauver franchir nom ami.\nViolent appel arrêter finir assurer conscience placer.\nRose demain attitude général service vin quelque.',1,'Légers maux de tête','Vide rêver histoire valeur. Machine gros heure permettre traîner nature froid. Perdre pur plaisir envelopper.','Tenir mal content retomber cou pourtant particulier deviner. Rare valoir naissance.','2025-12-27 04:08:59.658330','2025-12-27 04:08:59.658335',7,34,35,130,202,36),(45,'2025-12-05 17:43:02.658689','Terme complet haut fête.\nCreuser faim accepter. Arracher jeune de raconter rayon haut étage.\nApprendre gagner commander position vêtir un achever lien. Personnage discussion jouer départ oeil peu franc. Chambre salut côté rouge découvrir cruel essayer.','Charger nez jour rêver exemple dormir. Précieux écraser animal espèce. Garçon autour pencher chair curiosité autrefois profiter. Maître côté fin silencieux mal vivant refuser dire.',0,'Légers maux de tête','Particulier enfance terrain recevoir. Fixe sourire discuter or révéler portier ramasser. Un fleur prendre mer tapis bruit.','Remplir ce prince assurer. Certainement demande de goût.','2025-12-27 04:08:59.659350','2025-12-27 04:08:59.659355',8,30,33,120,203,31),(46,'2025-09-27 03:01:38.128447','Chasser remplir danser drôle imposer société. Ville ordre fonder sauvage important.\nFrançois honneur cacher ferme fer police.\nVeille réalité trembler amener armer inutile frapper. Plante juge cour souvent an former acte. Étonner folie lever lisser partie sujet obéir.','Hésiter caresser source violence refuser. Monter joie nourrir épais accuser. An peur haut visite discuter.\nPénétrer champ souhaiter important âme.',0,'','Vin classe perdu siège poitrine taire expérience droit. Fête pas je grain cercle. Calmer menacer point arriver.','Départ plaisir douceur absolu billet pièce. Toute retirer cheveu oui drôle tracer très.','2025-12-27 04:08:59.660270','2025-12-27 04:08:59.660275',7,32,33,125,213,30),(47,'2025-10-08 09:24:28.727973','Vieux tout saluer sueur.\nCalmer offrir dent chambre mien. Ciel mine aujourd\'hui pencher bureau sommeil.\nChoisir lutte cercle tête pas chaîne. Avenir effet dégager fauteuil voiture.\nSouvenir six sourire te pièce dernier.','Armer madame compter fatigue pont tout dernier si. Dehors éprouver arrêter lien sept décrire.',1,'Légers maux de tête','Barbe voici public doigt quel. Moi fenêtre âgé. Tellement peu moi.\nRetirer mode retrouver moitié pluie oeil. Rire exposer paysage dangereux garder.','Soutenir révéler sous but passion. Marche nouveau au fenêtre chat pitié ferme.','2025-12-27 04:08:59.661271','2025-12-27 04:08:59.661275',7,NULL,NULL,116,214,26),(48,'2025-10-18 04:07:31.788985','Point autorité reculer étude argent peuple connaissance depuis. Faible unique rideau réveiller.\nPapa midi bonheur pain. Battre dernier détail guerre empire toile. Un atteindre triste même tôt effet envelopper.\nPrintemps supporter miser signer honneur mois comme.','Étendue verser existence près admettre cuisine. Fête en désigner demain aujourd\'hui mot action.',0,'','Exécuter école près ministre mille rideau départ. Lumière rendre nuage adresser société. Soit madame passer groupe.','Parole douze nommer matière douceur. Grâce saluer as autre oser.','2025-12-27 04:08:59.662351','2025-12-27 04:08:59.662355',7,NULL,NULL,117,216,36),(49,'2025-11-08 21:20:43.333653','Certainement suivre intérieur loi. Couleur siège compagnie maintenir sentiment lune exemple. Chat passé image long conduire terrain. Frapper pièce peine condition mince.','Ça tombe terminer hier. Beaucoup comment peine comment. Petit oreille école matière nez grain.',0,'Nausées','Compte fois île condition papa écarter continuer. Menacer colline lutter ajouter.','Supporter soleil combat mentir relation dieu amour.','2025-12-27 04:08:59.663145','2025-12-27 04:08:59.663149',8,42,NULL,123,217,31),(50,'2025-10-14 01:07:03.593160','Affirmer vous page type forme ancien d\'autres apparence. Vieux saint religion.\nDéchirer cause dont lune traiter passion. Effort décider éclater envie de. Poser dangereux papa fidèle chercher. Rentrer histoire prendre.','Sec abandonner échapper consentir remplacer entraîner. Conclure accomplir court rêve. Vol sur enfin tour. École traîner habiter parfaitement.',0,'','Chemin également émotion violent. Tendre amuser barbe ignorer nord envie. Passé appartement blond cause lequel de.','Joindre je disposer autrement. En dame étranger casser saison mode. Été vide bras derrière causer.','2025-12-27 04:08:59.663972','2025-12-27 04:08:59.663976',9,NULL,30,111,221,35),(51,'2025-10-29 04:20:58.808327','Bon midi tôt en. Garde vivre ainsi marquer seul système.\nMembre plus succès malheur odeur gens. Promettre rouge plein franchir danger discuter.\nRéveiller robe colon écrire. Personne somme retrouver rien. Assez personne conclure entendre président retourner contenter jamais.','Glisser as visible leur réduire. Camarade masse mais frère oublier haut tapis.\nFond ennemi divers mari plaisir. Traiter un veiller signer question durant âme reconnaître.',1,'Aucun','Pitié sens soudain rideau tout vêtement. Quarante mêler divers or choix quant à fin. Peine patron chanter chaud que.','Chant jamais soi occasion éviter causer. Selon instinct grave demander.','2025-12-27 04:08:59.664881','2025-12-27 04:08:59.664886',9,31,35,117,225,27),(52,'2025-10-18 12:11:45.642131','Longtemps parole pendre autrefois inspirer. Recueillir changement goût possible depuis expérience.\nEnvelopper blanc inquiéter présenter silence réveiller manier. Envelopper derrière juste fin brusquement.','Beau un désirer poids. Saisir derrière grandir pierre.\nSocial etc lutter tant succès son parfaitement souffrir.',0,'','Roche avant poursuivre acheter. Marchand résultat réveiller cour étudier enlever. Toi accomplir aussitôt.','Fauteuil but désert vague route doigt mur champ. Important lequel fatigue politique aujourd\'hui ça.','2025-12-27 04:08:59.665620','2025-12-27 04:08:59.665624',9,NULL,29,101,226,29),(53,'2025-11-05 02:11:15.593192','Depuis peur ventre avec. Colline précipiter conduire allumer nouveau.\nFou intérêt marcher témoin plein marquer.\nCoûter vaste courant matière escalier quoi question.\nRéalité loi promettre puis sens établir puissant. Emporter bruit traîner essayer victime.','Douceur hier objet frère. Poche quel ou environ scène trou. Dieu ici trait ministre.\nDemeurer justice engager poésie presser. Donner marcher nu douter secret. Abattre traîner monde obliger mari.',0,'Nausées','Clair doute moitié garder éloigner geste cheveu. Pain parler épaule frère réponse discuter.\nQue menacer d\'autres bras bataille cou police.','Nature autrefois action rouge sourire marché douleur. Sec rayon goût posséder.','2025-12-27 04:08:59.666465','2025-12-27 04:08:59.666470',8,34,41,144,230,28),(54,'2025-11-08 06:39:25.237149','Étendre attirer pluie bruit absolu gauche souffler preuve. Prière rappeler voyager étendue société chez contenir. Poussière lune somme grâce chaleur musique beauté. Admettre faible cacher chance offrir.\nSueur éprouver peau obéir. Vivre vous inconnu question. Complètement lier fixer vide fin.','Saluer fidèle vide parfaitement. Abri sec dessiner résister chien comment âge absolu. Jamais effet chien secours.\nOser regard liberté certes sol vif.',1,'Légers maux de tête','Finir auteur compte taille par essayer.','Flot presser contraire français. Créer prince connaissance départ jambe entier.','2025-12-27 04:08:59.667272','2025-12-27 04:08:59.667277',7,31,29,147,233,26),(55,'2025-10-20 12:21:31.416245','Souhaiter appartenir certainement beauté épais respect bande. Pauvre mourir voler.\nDevoir abandonner possible avenir tandis que.\nJour juste sec. Cher ennemi beau peau tuer. Dégager choix vingt inconnu vieux parmi.','Montagne ce rompre entre faux user mériter nombreux. Mon prétendre pleurer. Voici quitter raconter préférer éclat réfléchir. Neuf printemps parfaitement midi bien adresser interrompre.',1,'Légers maux de tête','Produire fixer vers dormir attitude. Habiter cerveau discours jeune confondre couvrir. Occuper puis aucun enfant entraîner pensée toile livre.','Comment où nommer parler exemple grâce troubler.','2025-12-27 04:08:59.668169','2025-12-27 04:08:59.668174',9,NULL,41,132,234,34),(56,'2025-12-15 01:24:45.135560','Vingt dehors gros. Sauvage ailleurs mari obtenir.\nDéfendre finir certainement habitant ligne envoyer serrer. Projet figure servir journée marchand. Sujet violence proposer visible phrase madame.','Lettre patron dernier famille y apercevoir unique. Début recueillir dent dire bureau. Faute seigneur vieil cinquante protéger prononcer tour.',1,'Légers maux de tête','De idée depuis sûr grand certain. Désir conduire mensonge occuper. Pur volonté passer réussir âge but.','Essayer attitude souffrir. Billet marchand présence convenir position appuyer peau.','2025-12-27 04:08:59.668974','2025-12-27 04:08:59.668978',7,42,36,124,235,26),(57,'2025-12-11 13:41:10.785094','Flamme quand branche quel secrétaire côte quitter professeur. Subir paquet servir frère comprendre. Fond triste yeux bras tôt secret on.\nRetenir briser soleil mener ni signe veille. Droite particulier repousser immense étudier.\nInstant continuer respecter donner tel dehors or système.','Peser assez connaître hasard écrire d\'autres gagner. Essayer chute coin assurer.\nExprimer perdre portier fil vieil tellement ciel aider. Bande surtout paquet presque. Maître amuser observer ensuite.',1,'Aucun','Roi lentement mon. Attacher prix malgré malheur docteur arrière violent. Davantage être printemps fonction arriver.','Bande humain exemple. Il crier pays police.','2025-12-27 04:08:59.670242','2025-12-27 04:08:59.670247',8,32,NULL,125,237,31),(58,'2025-12-08 18:47:28.909365','Malheur en moitié. Petit vraiment droite vouloir demander habitant. Intérieur autrefois subir autrefois claire perdre.\nSocial réel conversation ce dur coûter précéder.\nÉternel extraordinaire printemps éclairer souffrance calme. Qualité dernier caractère si vent falloir.','Fort maladie attaquer énergie. Avis habitant dix.\nPrêter père cas attacher large etc appeler. Parent valeur honneur banc.',0,'Nausées','Ferme chiffre séparer juste meilleur. Moment humide étoile cacher pas personne certes.','Personne ressembler libre exister subir. Lisser rare supporter cruel seconde.','2025-12-27 04:08:59.671214','2025-12-27 04:08:59.671218',7,32,35,109,239,36),(59,'2025-11-28 14:13:30.522506','Pouvoir soulever apprendre tâche intéresser. Glisser grain fils.\nDistinguer changement large enfoncer fin soirée.\nPièce impression quarante exiger ce prétendre aider tantôt. Air anglais résistance plaisir mon autorité miser social.','Exécuter rideau notre même intéresser digne.\nConnaissance exposer montagne dieu. Intérêt loi pauvre angoisse relation personne. Aventure côté haute art.',0,'Nausées','Unique continuer remplir miser. Voisin demander disparaître réveiller. Retourner voix affaire pas objet travailler.','Si plan coeur. Figure acte répandre naître. Naturellement leur donc vêtement sien.','2025-12-27 04:08:59.672051','2025-12-27 04:08:59.672056',9,32,NULL,149,241,34),(60,'2025-12-03 12:20:40.749122','Discuter savoir vent saisir battre remettre. Embrasser permettre honte spectacle gauche parler pain. Observer accord lourd cacher sombre conseil envie.\nRéfléchir côte importer suffire cruel. Compagnie passé déclarer prier debout. Obéir français force somme chanter différent vie.','Note connaître conclure. Sentir part résoudre morceau naturellement acte. Quoi sommeil violent.',0,'Nausées','Gouvernement épaule battre. Gagner loin ciel malade.','Suivant court vivant effet repas fils. Moitié vaincre vêtir. Médecin rire accepter route.','2025-12-27 04:08:59.672790','2025-12-27 04:08:59.672794',9,30,31,128,243,25),(61,'2025-12-24 01:17:38.645244','Abattre gagner pendre île. Tandis Que même tapis huit dix droit extraordinaire veille.\nUn appel noir condition poste brusquement barbe. Résistance retour droite d\'autres ça lendemain. Victime souffrance sept.','Endroit herbe peu étoile.\nLequel supposer supporter troisième fonder. Compagnie oser bien soir exister port salut.',1,'Légers maux de tête','Attacher imposer musique feuille étranger courir salle. Diriger expliquer remonter tromper habitant garder.','Vaincre front cou question place revoir terme. Titre chaise éclairer moindre passé.','2025-12-27 04:08:59.673852','2025-12-27 04:08:59.673856',8,NULL,NULL,110,249,31),(62,'2025-12-21 04:01:21.983195','Prévenir projet brûler d\'autres user. Colline ventre dos long flot visage sur par. Parent son espèce folie parfaitement oncle dresser.\nSilencieux demain leur. Sou demeurer journal noir. Tandis Que veiller demeurer aider.\nCeci sentir poursuivre essayer.','Lettre composer deux chacun art. Battre tuer circonstance remarquer fait cou.\nGrand me vague ce inconnu sortir.',1,'','Tout travail que titre soirée lutter joindre. Pont midi comment sans triste faim. Pensée amuser soit entrer.','Spectacle froid fort préférer double. Sorte poète secret.','2025-12-27 04:08:59.675007','2025-12-27 04:08:59.675011',8,31,NULL,122,254,32),(63,'2025-12-13 03:02:00.813741','Blond étendue unique. Visite tel étouffer particulier devenir derrière.\nPolitique sourire chaise neuf roche. Signe jeune père pauvre descendre essuyer. Salut agir caresser pur vouloir terminer tromper.\nRessembler épais depuis. Me importance remettre raison aussitôt temps.','Rejoindre peine parent campagne prétendre. Songer coup douceur année guerre véritable rapporter.',0,'Légers maux de tête','Ce professeur phrase rêve mener. Tracer arme supposer fils saluer éclairer. Voler quarante vaste.\nSonger place beaucoup auprès rapport suivre.','Couleur voiture davantage corps renoncer. Pouvoir léger lendemain frais souvent jeune poussière.','2025-12-27 04:08:59.675968','2025-12-27 04:08:59.675972',7,36,40,119,257,30),(64,'2025-10-03 18:28:48.900359','Ignorer lisser compagnie appeler habitant par rapport. Contenter habiter échapper prier.\nVillage camarade découvrir absolument secret famille sentiment grandir. Poitrine argent drôle.','Champ choix scène préférer. Vin prêter ensemble poser. Savoir parce que effort théâtre réveiller.',1,'','Enfoncer pousser malade trente accorder monsieur. Tout casser victime foi femme ennemi petit briller. Mais étrange liberté mort.','Livre lueur or pénétrer pièce. Retourner crise joie perdre.','2025-12-27 04:08:59.676862','2025-12-27 04:08:59.676866',7,NULL,34,114,258,33),(65,'2025-10-15 14:08:28.434283','Cheveu creuser rêve bouche surtout saint présence. Dame réalité souffrance étudier armée particulier du. Branche course dur bras.\nAutrement dos changer prévenir saint oui. En vin commander oreille. Son réveiller ramasser gloire raconter.','Accrocher hier décider fatigue demi.\nRamasser devenir chasse exiger seuil. Presser ah nous quitter vie se hier. Face dresser siège long fait.',0,'Légers maux de tête','Etc descendre français désir. Bord chute résultat. Glisser réflexion mériter plus.','Beaucoup part soulever fils rouge. Étudier grave penser.','2025-12-27 04:08:59.677770','2025-12-27 04:08:59.677774',8,NULL,41,108,259,32),(66,'2025-12-11 11:15:51.408063','Réveiller vendre événement disposer lorsque. Détruire gros chacun ajouter objet pas remonter.\nVictime absence sec étendue. Croix sentiment pouvoir dernier simple mener. Abandonner peur impossible garde supposer former vingt.','Doute mesure attention gros risquer dessiner plaindre. Malheur occasion calme non impression presque en.',0,'','Souffrance conclure séparer victime garde président. Frapper un quelque rare cesse verre étage.','Grand histoire facile interroger prochain. Confondre arrivée afin de pain solitude.','2025-12-27 04:08:59.678701','2025-12-27 04:08:59.678705',8,38,NULL,108,266,28),(67,'2025-10-25 10:58:58.881243','Fidèle reconnaître oeil visite fidèle éternel. Rien continuer résister ainsi dimanche cuisine violent. Haïr me leur joie fixe enlever gauche.\nRamasser rappeler agent noire secours.\nUn enlever membre goutte général changer. Immense magnifique grâce impossible chasse.','Quant À toit droit remplir. Prêt foi profondément avant.\nÊtre plus distance type extraordinaire étudier note éternel. Commencement honte palais réunir long double vie. Groupe gloire aventure.',1,'Légers maux de tête','Observer position grave joindre. Campagne indiquer expérience croix entrée gloire garde. Souhaiter défaut douze feuille besoin.','Main votre ministre. Puis menacer projet exister conscience prétendre.','2025-12-27 04:08:59.679914','2025-12-27 04:08:59.679918',8,NULL,NULL,135,269,28),(68,'2025-12-03 23:14:37.944378','User dresser voyager nommer terreur sol te. Sang finir sou. Commencer plaine détruire différent terrain intérêt.\nVoilà doute même femme chaque. Dresser envie réalité demain acte reculer l\'une force. Tout finir ni quant à commencer mourir maladie. Prier brûler coin caresser entre pencher fer.','Prétendre même bouche jeu mensonge. Port contre soulever profond nuit.',0,'Légers maux de tête','Double attendre blanc mensonge jeunesse. Verre mourir glisser conduire paysage autant enfermer.','Droit asseoir profondément habitude chaque odeur. Terrain fin amuser matin visage y disposer voilà.','2025-12-27 04:08:59.680787','2025-12-27 04:08:59.680791',7,32,39,140,274,30),(69,'2025-12-13 00:13:02.698096','Étouffer nuage officier chemise naturel. Commencer crise dessus nécessaire vue chacun lier.\nTandis Que bras second genre saisir étudier obéir. Passage assister placer réel perte dimanche cerveau. Tendre approcher verre inspirer muet dominer.','Gouvernement poids intérieur suivre pitié depuis.\nLoin alors pur arbre témoin. Effort tout obliger atteindre désigner toujours menacer. Que égal papa voie vêtir.',0,'Légers maux de tête','Masse lorsque chaîne paysage glisser. Signe côte spectacle.\nConfondre couleur nord. Fil soumettre sec appeler importer.','Jeunesse un lisser jamais âge frère rapidement.','2025-12-27 04:08:59.681700','2025-12-27 04:08:59.681704',7,NULL,NULL,111,276,30),(70,'2025-11-05 21:17:34.814824','Marche vieux retirer compte pitié puis. Payer champ ami. Supposer souvent grâce spectacle rapporter fenêtre. Cercle véritable premier reprendre courir mettre parmi.','Froid endormir soi condamner moitié. Malgré social essayer aimer capable qualité membre.\nBlanc cri nuage maladie sonner. Parent impression père chaise désormais rire fils.',0,'','Soirée habitude feu beau pleurer résistance. Ensemble naturel étudier genre moitié maître.','Éclat chemin parfois ancien voler terme. Rompre intéresser heureux forcer inquiétude.','2025-12-27 04:08:59.682528','2025-12-27 04:08:59.682532',9,39,38,107,280,25),(71,'2025-09-28 02:52:04.018506','Poursuivre village haine étoile hauteur. Voici terreur rouler ordre éclairer. Quatre argent dimanche déjà possible acte.\nCertes hors parce que bien divers tendre.\nPourtant courant tache exister enfermer. Nuage terminer travers souvenir dimanche maintenir.','Sauter pouvoir pensée état. Perdre réveiller manier article immense exiger certain tout. Souffler tirer maison écraser malgré poste.',1,'','Troubler émotion supérieur attendre rêve céder ministre. Certain ville même ce exécuter. Chemise crise jusque flot prix glisser toujours.','Engager prendre rare davantage déposer. Essuyer crainte hôtel autre parent produire million.','2025-12-27 04:08:59.683492','2025-12-27 04:08:59.683496',9,40,NULL,126,281,34),(72,'2025-12-01 12:02:31.532090','Partager autrefois capable inquiéter remercier remonter. Lieu genou demande spectacle chanter.\nEnnemi odeur bout tard reconnaître autorité tôt. Peu effacer dos pays mien crier. Six passé impression système avancer plan je.','Seul aventure fusil voisin. Tout fil rapide.\nMuet silencieux ouvrir arrivée main loup presque.',1,'Nausées','Disposer prévenir parti ensemble apprendre justice vague. Oui année noir accuser durer. Recueillir public chant fenêtre. Ouvert départ alors.','Ensemble maître rentrer ennemi. Ci demeurer souvenir vers imaginer.','2025-12-27 04:08:59.684288','2025-12-27 04:08:59.684292',9,NULL,NULL,143,283,34),(73,'2025-10-08 21:29:20.321415','Malgré voisin importer petit parent chat là. Doucement vague plaisir autre. Épaule terrain public changer dire prison.\nÉgalement mentir silencieux groupe. Soutenir accomplir mensonge mot beau.','Loup trois plein vérité rêve durer.\nDevant exister je. Étudier descendre respecter peu mesure écraser.\nSavoir il serrer lorsque. Prétendre ce pour.',0,'Nausées','Herbe oser sonner lendemain million porter. Sonner main nul commun sujet début forêt parmi. Devant tôt ancien salle devoir tâche exemple.','Quart asseoir âme naturellement. Certes lorsque éprouver repousser.','2025-12-27 04:08:59.685256','2025-12-27 04:08:59.685260',7,32,39,124,284,36),(74,'2025-11-16 03:19:56.916067','Notre repousser etc considérer. Or taire avoir consulter profondément vide. Ah désigner absence bruit essuyer trait debout.\nAller moment matin calme moitié durant un en. Traiter espace point lier personne ah. Donner billet tombe portier.','Signe observer beau âgé te. Rayon rapport grand nul enlever vraiment. Camarade situation six après couleur.',1,'Nausées','Bleu monsieur assurer connaître personne hésiter passé semblable. Finir bien terme ancien drôle bout.\nGenou se gloire grain. Fixer rouge charge.','Cause serrer compte port faveur. Compagnon exprimer présent présenter dernier cesser sommet.','2025-12-27 04:08:59.686922','2025-12-27 04:08:59.686927',7,NULL,NULL,110,297,30),(75,'2025-11-25 16:14:14.604095','Port vision trésor court. Monsieur sorte former bientôt. Pays y prêter suivre comment paysage.\nCertes agent retenir oh.\nTout deviner est profond admettre recommencer. Poids accompagner franchir accepter complet endroit résoudre. Blond chien votre instant étoile prix.','Claire hauteur visage dresser ailleurs esprit âge projet.\nTon port soirée. Tromper étaler question instinct.\nMois dernier geste puis trois. Former droit haut nation. Ainsi obliger devenir chez.',1,'Nausées','Auprès fou entrée pourquoi front curieux. Jardin présenter remettre titre égal couvrir rouge. Parce Que saint but tempête type enfance.','Obtenir tôt loup mon pièce double. Matière dire proposer demande route valeur pauvre découvrir.','2025-12-27 04:08:59.688810','2025-12-27 04:08:59.688814',7,30,35,142,300,26);
/*!40000 ALTER TABLE `consultations_pf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_messages`
--

DROP TABLE IF EXISTS `contact_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_messages` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sujet` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `lu` tinyint(1) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `patient_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `contact_messages_patient_id_dabeea10_fk_patients_id` (`patient_id`),
  CONSTRAINT `contact_messages_patient_id_dabeea10_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_messages`
--

LOCK TABLES `contact_messages` WRITE;
/*!40000 ALTER TABLE `contact_messages` DISABLE KEYS */;
INSERT INTO `contact_messages` VALUES (41,'Eugène Barthelemy-Mace','cecile48@example.com','Parfaitement action tourner lutter tempête.','Rester silencieux mort donner soirée plaire rond. Croire papa accent gagner traîner prévenir train.\nTourner plaine droit pierre eaux impression falloir confier. Essuyer premier tourner midi fille raison métier.\nPreuve nerveux usage près marcher autre.\nCacher jeunesse douze couleur soir banc oiseau.\nApparaître déposer membre fort inquiéter. Soi derrière posséder ancien refuser miser propos. Fidèle grave remplacer fin cas toute.',1,'2025-12-27 04:08:59.866270',146),(42,'Noémi Guichard','hubertluc@example.net','Frapper poussière égal espèce dur scène aventure.','Tandis Que détacher devenir depuis décrire promettre bataille. Violent former espérer asseoir vouloir recherche colon. Lèvre avenir arbre haut vif société suffire.\nRapport françois enfoncer remarquer quoi soleil reposer anglais. Livre retirer sang autorité.\nCas autour préparer. Travail décider arrêter valoir choix drame quant à. Huit voie âme aider paysage pareil deux. Meilleur réveiller mois servir.\nAsseoir mien composer étranger membre. Besoin durant ouvrage accrocher.',0,'2025-12-27 04:08:59.867045',130),(43,'Jeanne Delaunay','picardjeannine@example.net','Large dangereux peine tellement chambre.','Passage moi cerveau saluer reconnaître chute. Grand parfois colon tellement silence calme tout. Vision honte préparer joie.\nPersonnage éclat tirer enfance peu. Fort arme quand attention verser. Dehors tour porte déposer user soleil matière.\nTout fois emmener toi. Pleurer journée étroit tard désert. Briller calmer maître énorme centre.\nPauvre lentement parole mien.',1,'2025-12-27 04:08:59.867688',117),(44,'Corinne Briand','valleesabine@example.com','Art saisir doute produire seuil.','Créer nous étendue soi plein révéler. Déjà respect gouvernement propos voile réel demander.\nInstant place indiquer dormir présence sourire bois. Coup matin paix finir lit.\nDépasser hauteur président question couper marchand essayer auprès. Marché importer seuil gros.\nBien cercle fonction. Cinq roman impossible fuir croiser.\nArrêter part user. Réunir afin de guère durer saint delà. Pouvoir billet point cou fort. Certes âme pénétrer peau but lutte.',0,'2025-12-27 04:08:59.868835',104),(45,'Paulette Delannoy','maggie81@example.org','Mettre début déchirer lentement seuil événement faire.','Ton demain vin or terre son. Quelque après vide nouveau.\nHumide lors printemps d\'autres également justice bientôt. Oublier foi trouver complètement mettre demi.\nSuivant mort six armer renoncer escalier nation. Arracher grand bien. Propos même bonheur complet.\nSauver vieux foi ignorer système brûler. Décider genre commencement ensuite rapport sang. Désespoir épais tard.\nSubir fait trop dominer désert. Craindre déclarer appartenir asseoir lune accent le.',1,'2025-12-27 04:08:59.869598',NULL),(46,'Gabrielle Martins Le Lemaire','georgesmichaud@example.com','Habitant douceur delà voir mort étranger bien.','Tache tenter amuser étudier exécuter trois volonté. Digne hors exprimer trois ferme souffrance prière.\nRecueillir payer juge impossible habiller. Oreille souhaiter argent salle aussitôt prier. Du seuil fleur matin y.\nNation marché justice second servir autour. Taille déchirer maintenir rendre bande.\nBas créer scène chasse. Semaine céder complet proposer long arriver fruit.',1,'2025-12-27 04:08:59.870786',NULL),(47,'Emmanuelle Perrin','patrickguillot@example.com','Secours étranger sentiment engager sorte fortune autant cou.','Ramener agent condamner arracher.\nSalut fenêtre étonner. Naturel nous apparence large sein souhaiter grandir moyen. Courage cinq règle achever descendre mari demande pierre. Trou contenter loup pénétrer répéter droit tôt.\nConstruire goût objet. Lune ordre particulier odeur printemps fatigue. Presque possible rentrer.\nNaissance baisser gris ennemi travail entraîner. Leur goutte pointe blanc. Voir faux différent boire drôle bureau demeurer.',0,'2025-12-27 04:08:59.871467',NULL),(48,'Françoise de la Bourdon','besnardmargaud@example.net','Trésor attention geste époque noir recevoir.','Aussitôt parvenir chercher vendre accuser construire plaine. Approcher caractère lentement cercle douze l\'un delà.\nGrave vivant vol parent hauteur. Son quatre besoin son autrefois briller engager. On conseil cri interrompre défendre glisser devant.\nRelever comme président asseoir. Eau avancer mensonge mensonge. Importance pas doux nuage.\nMoitié chaud retirer jardin danser ruine côte. Danger rejoindre morceau condition comment tenir retenir ennemi.',0,'2025-12-27 04:08:59.872020',NULL),(49,'Timothée du Duval','nathalie31@example.net','Noir si oreille dame quinze bon centre.','Rapport très dormir connaître aussitôt. Couvrir toit absence rejoindre examiner parler manger. Bout visage matin visible source emporter prochain. Guère semaine eh réfléchir prévenir remarquer.\nAsseoir rapide fleur transformer pierre source entre. Lendemain société endroit appel.\nRang loi arrière école général. Morceau patron si sol jardin suivant.\nAmour inspirer soudain travers manger taire silence. Page marché doucement autre.',0,'2025-12-27 04:08:59.872755',NULL),(50,'Corinne Olivier','chauveauvincent@example.org','Avec rire nom parvenir bras leur voile.','Objet tôt bataille agir briser.\nAmour chasser hésiter conclure paquet.\nHomme oser nul mari ouvrir blanc plonger. Recherche mur arbre présenter.\nÊtre bureau rejeter servir livre cri. Prévenir baisser quart.\nAbsolu soulever enfoncer. Humain neuf entrer chaud rêver envoyer désert. Lèvre planche palais passé baisser.\nRoute dégager miser mille pont eau douceur. Habitude avance compagnie vous exposer rassurer. Attirer descendre chasse sourire animal.',0,'2025-12-27 04:08:59.873298',106),(51,'Jacques Louis','louisemaillot@example.com','Pitié trait clef honneur sang terrain.','Existence observer an battre remettre. Ignorer surtout général lisser signe durant moyen. Sourd pouvoir million autrement police.\nMourir descendre interrompre tout. Faim métier préparer habiller ramener humide attirer debout.\nFenêtre faveur mois entretenir tôt. Traverser répandre nul. Fin plaine en gens un cinquante.\nPropre point maintenir vous. Douleur comme militaire cacher parfois disparaître nature noire. Dimanche offrir combien appeler.\nAucun mensonge riche sauver parmi entraîner oreille.',0,'2025-12-27 04:08:59.874096',107),(52,'Thomas Leroy Le Morin','moulinsylvie@example.com','Preuve puisque as naître nature dehors glisser fort.','Français pièce fauteuil renverser semblable entrée chiffre. Repousser répondre général atteindre face. Rue compagnie affirmer veille employer.\nAllumer cent allumer. Découvrir un dire raconter amener haut aimer. Désespoir fumée inconnu pour mauvais. Ancien ressembler avis oiseau vol seuil parce que.\nCours chambre tomber plaindre beaucoup cher tracer. Froid avancer long groupe acheter coup mince. Raconter silencieux françois attention coeur.',0,'2025-12-27 04:08:59.874617',NULL),(53,'Alexandria Hardy','laurent01@example.com','Vaste confier nation cou centre pas étrange.','Village maladie maintenant point article. Curiosité marchand chaise. Sien quelque solitude debout papa robe charger.\nPar quart coucher avancer moi. Posséder visage vers plonger partager. Marcher début frapper pourquoi construire oublier.\nJardin retour un rappeler bras muet. Jardin aide arrêter. Sans claire suite robe vouloir mériter.\nBranche particulier reprendre de révéler parole votre. Perdu tandis que signifier tâche donc toi avec raconter.',1,'2025-12-27 04:08:59.875284',NULL),(54,'Sébastien de la Bouchet','margotlelievre@example.com','Nouveau naître avis public claire presque surveiller mettre.','Odeur paraître projet passer idée front. Croix côté phrase garde cela sonner. Nombreux matière autre vous grain.\nSimple violence vieux oeil premier désigner. Émotion voyage ancien pourquoi rêver prendre poitrine. Sourire nuit repousser gloire réveiller.\nLettre un dent debout père dessus se. Ailleurs semblable déchirer passage ruine tomber cacher. Honte tendre ainsi relation frapper empire fois.\nÉtonner celui douter durant lettre auteur autre. Arbre vent oh étudier voile découvrir genou bruit.',1,'2025-12-27 04:08:59.878236',NULL),(55,'François Bousquet','bertrand89@example.org','Triste fait faux campagne de français personne.','Mode rentrer cacher jusque. Plutôt front avoir guère usage doucement occuper. Soleil père corps désigner.\nEnsuite beau soirée présenter violence saison. Saison mur lune inventer trace. Secret genou connaissance rideau plein.\nNon arrêter liberté cours cacher peau. Part ce rire gauche intérêt. Colline temps fauteuil dégager gauche or scène.\nConduire époque vivre compte auquel magnifique ça. Quarante passer vers.',0,'2025-12-27 04:08:59.879909',137),(56,'Julie Dupré','fredericgimenez@example.org','Hier ou musique réalité supérieur relever.','Bruit car cent saluer françois celui. Ennemi car aucun sentier.\nSystème pas ton pauvre. Croiser importer répandre position.\nCabinet société préférer atteindre parcourir. Étoile mal instinct marier. Sec convenir réel temps.\nAccent lorsque étranger ressembler pas là. Accent somme couper voler foi double sang animer. Perdu social direction neuf.',1,'2025-12-27 04:08:59.880805',NULL),(57,'Denis Fouquet','augustindaniel@example.org','Théâtre métier ami coin.','Pierre endroit prier quarante décrire accorder. Moitié scène plonger capable comme système.\nMois aspect oreille sauvage.\nPoche nécessaire joue aile cheveu. Fortune risquer ventre montrer certain discours quarante. Secret parole très révolution deviner beau.\nMériter loin disparaître ton briller accompagner.\nCasser ton rejoindre noir ville éclat.\nEnsemble chaud plonger fenêtre respirer. Appeler docteur trente immense peu éteindre. Agent dominer pays objet honte pendant.',0,'2025-12-27 04:08:59.881536',135),(58,'Robert Lebreton','jerome26@example.com','Arrêter rang établir répondre éclater.','Sourd ferme briller doute précéder parce que campagne. Jouer table ouvert cesser.\nDehors guerre acheter franchir planche. Vaincre comment bas bas arracher lieu choix. Voiture pitié nous rôle forêt muet veiller.\nSuccès morceau parti davantage fidèle président rayon. Ah sonner quant à côte paupière asseoir creuser.\nCommun force servir entrée retour partir chanter.\nArmer conversation passer portier dernier. Examiner machine campagne robe demeurer. Exister réel été respect succès lever.',1,'2025-12-27 04:08:59.882082',NULL),(59,'Denise Morvan du Prévost','alice54@example.com','Surtout salle debout réussir expérience fine.','Être désir joie bête remonter heure. Air situation règle.\nMesure mot mine douleur. Espèce marche plaire doux chaleur dire douceur renverser.\nEspoir payer mal oeuvre lentement. Voiture large tôt étage porte passé premier. Parent leur idée visite.\nPrononcer campagne parcourir problème vendre. Sûr présenter envelopper lutter et. Assister paquet mariage épaule science.',1,'2025-12-27 04:08:59.882592',NULL),(60,'Sabine Evrard','benoitmenard@example.org','Jaune pareil effet adresser accuser arme propre.','Exiger couper honte cabinet prêter plaisir révéler. Je inquiétude sens avenir face danser escalier.\nTour absolument quoi autant oiseau bord que. Fenêtre médecin pierre obtenir couler oeil peine. Qualité vaste sein caractère heureux.\nHabitant cinq fait descendre. Inutile montrer lèvre roman année. Visible fort ensemble journal certes race falloir.\nFermer étude fumer soirée remonter pouvoir crier. Déclarer quel problème tromper. Signifier joie goût joindre.',0,'2025-12-27 04:08:59.883237',NULL);
/*!40000 ALTER TABLE `contact_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disponibilites_specialistes`
--

DROP TABLE IF EXISTS `disponibilites_specialistes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disponibilites_specialistes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `jour_semaine` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `heure_debut` time(6) NOT NULL,
  `heure_fin` time(6) NOT NULL,
  `date_debut_exception` date DEFAULT NULL,
  `date_fin_exception` date DEFAULT NULL,
  `motif_exception` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `specialiste_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `disponibilites_specialis_specialiste_id_jour_sema_a5f3695c_uniq` (`specialiste_id`,`jour_semaine`,`heure_debut`),
  CONSTRAINT `disponibilites_speci_specialiste_id_ece25685_fk_specialis` FOREIGN KEY (`specialiste_id`) REFERENCES `specialistes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=230 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disponibilites_specialistes`
--

LOCK TABLES `disponibilites_specialistes` WRITE;
/*!40000 ALTER TABLE `disponibilites_specialistes` DISABLE KEYS */;
INSERT INTO `disponibilites_specialistes` VALUES (159,'samedi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.426623',25),(160,'jeudi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.427536',25),(161,'mardi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.429489',25),(162,'mercredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.431219',25),(163,'mercredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.432006',25),(164,'samedi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.433201',26),(165,'mercredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.434065',26),(166,'lundi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.435738',26),(167,'lundi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.436588',26),(168,'jeudi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.437044',26),(169,'jeudi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.437890',26),(170,'lundi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.438489',27),(171,'vendredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.439006',27),(172,'vendredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.439647',27),(173,'mardi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.440652',27),(174,'mardi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.443970',27),(175,'jeudi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.444761',27),(176,'lundi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.445143',28),(177,'lundi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.445485',28),(178,'samedi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.445821',28),(179,'samedi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.446248',28),(180,'vendredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.446565',28),(181,'vendredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.446855',28),(182,'samedi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.447277',29),(183,'samedi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.448125',29),(184,'vendredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.448871',29),(185,'lundi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.449616',29),(186,'lundi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.450128',29),(187,'mardi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.450504',29),(188,'mardi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.450951',29),(189,'jeudi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.451990',29),(190,'jeudi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.452393',29),(191,'jeudi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.453192',30),(192,'jeudi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.453853',30),(193,'lundi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.454642',30),(194,'mardi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.455405',30),(195,'mardi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.456768',30),(196,'samedi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.457672',30),(197,'mercredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.458132',30),(198,'mercredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.458554',30),(199,'vendredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.459683',30),(200,'vendredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.460097',31),(201,'vendredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.460924',31),(202,'lundi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.462008',31),(203,'mercredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.463188',31),(204,'mercredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.463789',31),(205,'samedi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.464809',32),(206,'lundi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.485992',32),(207,'jeudi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.486624',32),(208,'lundi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.487242',33),(209,'jeudi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.488423',33),(210,'jeudi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.489480',34),(211,'vendredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.491825',34),(212,'samedi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.492528',34),(213,'mercredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.493681',35),(214,'vendredi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.494906',35),(215,'mardi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.495535',35),(216,'jeudi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.496217',35),(217,'jeudi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.496709',35),(218,'samedi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.497063',35),(219,'mercredi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.498188',36),(220,'mardi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.499368',36),(221,'samedi','08:00:00.000000','12:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.500033',36),(222,'samedi','14:00:00.000000','18:00:00.000000',NULL,NULL,'',1,'2025-12-27 04:08:59.500628',36),(223,'lundi','08:00:00.000000','17:00:00.000000',NULL,NULL,'',1,'2026-02-01 05:48:19.968519',36),(224,'lundi','08:00:00.000000','17:00:00.000000','2026-02-09','2026-02-09','',1,'2026-02-03 03:09:47.538389',25),(226,'mercredi','10:10:00.000000','11:11:00.000000','2026-02-04','2026-02-04','',1,'2026-02-03 03:27:56.149266',25),(229,'lundi','10:00:00.000000','17:00:00.000000',NULL,NULL,'',1,'2026-02-03 03:33:22.209705',25);
/*!40000 ALTER TABLE `disponibilites_specialistes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(25,'pf','avisspecialiste'),(16,'pf','commandepharmacie'),(13,'pf','consultationpf'),(12,'pf','contactmessage'),(24,'pf','disponibilitespecialiste'),(38,'pf','dossiermedical'),(34,'pf','employepharmacie'),(41,'pf','facturefournisseur'),(39,'pf','fichierdossiermedical'),(40,'pf','fournisseur'),(31,'pf','historiqueconnexion'),(10,'pf','hopital'),(6,'pf','landingpagecontent'),(18,'pf','lignecommande'),(42,'pf','lignefacturefournisseur'),(37,'pf','ligneordonnance'),(33,'pf','lignevente'),(7,'pf','methodecontraceptive'),(27,'pf','mouvementstock'),(21,'pf','notification'),(36,'pf','ordonnance'),(11,'pf','patient'),(14,'pf','pharmacie'),(15,'pf','prescription'),(17,'pf','produit'),(19,'pf','rapportconsultation'),(35,'pf','registre'),(20,'pf','rendezvous'),(22,'pf','service'),(30,'pf','sessionutilisateur'),(23,'pf','specialiste'),(8,'pf','specialite'),(26,'pf','stockitem'),(28,'pf','stockproduit'),(9,'pf','user'),(29,'pf','value'),(32,'pf','ventepharmacie'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-26 00:29:04.222053'),(2,'contenttypes','0002_remove_content_type_name','2025-12-26 00:29:04.251029'),(3,'auth','0001_initial','2025-12-26 00:29:04.327883'),(4,'auth','0002_alter_permission_name_max_length','2025-12-26 00:29:04.344050'),(5,'auth','0003_alter_user_email_max_length','2025-12-26 00:29:04.346603'),(6,'auth','0004_alter_user_username_opts','2025-12-26 00:29:04.349516'),(7,'auth','0005_alter_user_last_login_null','2025-12-26 00:29:04.351901'),(8,'auth','0006_require_contenttypes_0002','2025-12-26 00:29:04.352347'),(9,'auth','0007_alter_validators_add_error_messages','2025-12-26 00:29:04.355061'),(10,'auth','0008_alter_user_username_max_length','2025-12-26 00:29:04.358002'),(11,'auth','0009_alter_user_last_name_max_length','2025-12-26 00:29:04.360143'),(12,'auth','0010_alter_group_name_max_length','2025-12-26 00:29:04.366877'),(13,'auth','0011_update_proxy_permissions','2025-12-26 00:29:04.370112'),(14,'auth','0012_alter_user_first_name_max_length','2025-12-26 00:29:04.373280'),(15,'pf','0001_initial','2025-12-26 00:29:05.911042'),(16,'admin','0001_initial','2025-12-26 00:29:05.956060'),(17,'admin','0002_logentry_remove_auto_add','2025-12-26 00:29:05.965807'),(18,'admin','0003_logentry_add_action_flag_choices','2025-12-26 00:29:05.974380'),(19,'sessions','0001_initial','2025-12-26 00:29:05.980329'),(20,'pf','0002_historiqueconnexion_sessionutilisateur','2026-01-05 23:56:52.287785'),(21,'pf','0003_ventepharmacie_lignevente_and_more','2026-01-07 00:32:32.579848'),(22,'pf','0004_alter_user_role_employepharmacie','2026-01-08 01:45:11.183278'),(23,'pf','0005_patient_ethnie_patient_lieu_naissance_and_more','2026-01-21 19:13:20.698896'),(24,'pf','0006_ordonnance_ligneordonnance_and_more','2026-01-22 21:46:59.523080'),(25,'pf','0007_ordonnance_qr_code_ordonnance_qr_code_url','2026-01-22 22:19:44.588734'),(26,'pf','0008_dossiermedical','2026-01-26 21:21:46.335826'),(27,'pf','0009_remove_consultationpf_methode_prescite_and_more','2026-02-12 02:10:41.916456'),(28,'pf','0999_add_factures_fournisseurs','2026-02-13 17:50:01.460088'),(29,'pf','1000_add_annulation_vente','2026-02-13 19:54:01.196880');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dossiers_medicaux`
--

DROP TABLE IF EXISTS `dossiers_medicaux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dossiers_medicaux` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_dossier` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patient_nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patient_prenom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patient_age` int NOT NULL,
  `patient_sexe` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `motif_consultation` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `histoire_maladie` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `antecedents` longtext COLLATE utf8mb4_unicode_ci,
  `antecedents_familiaux` longtext COLLATE utf8mb4_unicode_ci,
  `gyneco_obstetricaux` longtext COLLATE utf8mb4_unicode_ci,
  `chirurgicaux` longtext COLLATE utf8mb4_unicode_ci,
  `examen_general` longtext COLLATE utf8mb4_unicode_ci,
  `examen_physique` longtext COLLATE utf8mb4_unicode_ci,
  `hypothese_diagnostic` longtext COLLATE utf8mb4_unicode_ci,
  `diagnostic` longtext COLLATE utf8mb4_unicode_ci,
  `bilan_biologie` longtext COLLATE utf8mb4_unicode_ci,
  `bilan_imagerie` longtext COLLATE utf8mb4_unicode_ci,
  `date_consultation` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `hopital_id` bigint NOT NULL,
  `registre_id` bigint NOT NULL,
  `specialiste_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_dossier` (`numero_dossier`),
  KEY `dossiers_medicaux_hopital_id_03258527_fk_hopitaux_id` (`hopital_id`),
  KEY `dossiers_me_numero__a87310_idx` (`numero_dossier`),
  KEY `dossiers_me_registr_729522_idx` (`registre_id`),
  KEY `dossiers_me_special_c5f2d9_idx` (`specialiste_id`,`date_consultation`),
  CONSTRAINT `dossiers_medicaux_hopital_id_03258527_fk_hopitaux_id` FOREIGN KEY (`hopital_id`) REFERENCES `hopitaux` (`id`),
  CONSTRAINT `dossiers_medicaux_registre_id_b756e13d_fk_registres_id` FOREIGN KEY (`registre_id`) REFERENCES `registres` (`id`),
  CONSTRAINT `dossiers_medicaux_specialiste_id_9ea93f07_fk_specialistes_id` FOREIGN KEY (`specialiste_id`) REFERENCES `specialistes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dossiers_medicaux`
--

LOCK TABLES `dossiers_medicaux` WRITE;
/*!40000 ALTER TABLE `dossiers_medicaux` DISABLE KEYS */;
INSERT INTO `dossiers_medicaux` VALUES (1,'DOS202601265808','Dembele','Arouna',30,'M','palau','bdjd','dhgd','ddd','thd','gghd','dkkdk','','djjd','wggdb','dflpfd','dvvd','2026-01-26 21:28:28.670335','2026-01-26 21:28:28.670401','2026-01-26 21:28:28.670418',9,5,25),(2,'DOS202601277155','Dembele','Arouna',30,'M','mot de tête','il ya deux jours','cote maternelle','les mots de tête sont récurent','','','','','','','','','2026-01-27 20:17:46.228582','2026-01-27 20:17:46.229318','2026-01-27 20:17:46.229332',9,5,25),(3,'DOS202601273264','Doumbia','Ousmane',30,'M','des mots de tête récurent , avec des vomissement','Il ya deux jour , je suis mal senti après j\'ai commence a vomir et avoir des mots de tête','','','','','','','','','','','2026-01-27 21:33:20.495769','2026-01-27 21:33:20.495816','2026-01-27 21:33:20.495826',9,6,25),(4,'DOS202602017487','Kouma','Mamadou',20,'M','Paludisme','j\'avais des maux de tête ,et après j\'ai commence a vomir','','','','','','','','','','','2026-02-01 05:36:01.216390','2026-02-01 05:36:01.216419','2026-02-12 02:38:38.098925',7,7,36),(11,'DOS202602128375','Kouma','Mamadou',20,'M','rrtt','ffgt','','','','','','','','','','','2026-02-12 02:29:16.545636','2026-02-12 02:29:16.545714','2026-02-12 19:38:12.646353',7,7,36);
/*!40000 ALTER TABLE `dossiers_medicaux` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employes_pharmacies`
--

DROP TABLE IF EXISTS `employes_pharmacies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employes_pharmacies` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `poste` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_embauche` date NOT NULL,
  `salaire` decimal(10,2) DEFAULT NULL,
  `peut_vendre` tinyint(1) NOT NULL,
  `peut_gerer_stock` tinyint(1) NOT NULL,
  `peut_voir_commandes` tinyint(1) NOT NULL,
  `peut_traiter_commandes` tinyint(1) NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `pharmacie_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `peut_annuler_vente` tinyint(1) NOT NULL,
  `peut_enregistrer_facture` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `employes_pharmacies_user_id_pharmacie_id_4ea0c575_uniq` (`user_id`,`pharmacie_id`),
  KEY `employes_ph_pharmac_7bacf8_idx` (`pharmacie_id`),
  KEY `employes_ph_user_id_23119e_idx` (`user_id`),
  KEY `employes_ph_actif_a5904c_idx` (`actif`),
  CONSTRAINT `employes_pharmacies_pharmacie_id_097e98cc_fk_pharmacies_id` FOREIGN KEY (`pharmacie_id`) REFERENCES `pharmacies` (`id`),
  CONSTRAINT `employes_pharmacies_user_id_dba25265_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employes_pharmacies`
--

LOCK TABLES `employes_pharmacies` WRITE;
/*!40000 ALTER TABLE `employes_pharmacies` DISABLE KEYS */;
INSERT INTO `employes_pharmacies` VALUES (1,'Vendeur','2026-01-08',NULL,1,1,1,1,1,'Employé test','2026-01-08 01:50:06.863107','2026-02-13 20:04:01.856961',11,229,0,0),(4,'Vendeur','2026-01-08',200000.00,1,0,1,1,1,'','2026-01-08 02:58:10.105016','2026-02-13 23:18:48.951231',11,232,1,0),(5,'Employé','2026-01-08',NULL,1,1,1,0,1,'','2026-01-08 03:09:50.914259','2026-01-08 03:09:50.914276',12,233,0,0),(6,'Employé','2026-01-11',1000.00,1,1,1,1,1,'','2026-01-11 22:13:27.200002','2026-02-14 00:47:58.612885',11,234,1,1),(7,'Préparateur','2026-02-13',NULL,1,1,1,1,1,'','2026-02-13 23:21:08.681912','2026-02-13 23:21:08.681920',11,241,1,1),(8,'Magasinier','2026-02-13',NULL,1,0,1,1,1,'','2026-02-13 23:22:15.335031','2026-02-13 23:22:15.335043',11,242,1,1);
/*!40000 ALTER TABLE `employes_pharmacies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `factures_fournisseurs`
--

DROP TABLE IF EXISTS `factures_fournisseurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factures_fournisseurs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_facture` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_facture` date NOT NULL,
  `date_enregistrement` datetime(6) NOT NULL,
  `date_echeance` date NOT NULL,
  `montant_ht` decimal(12,2) NOT NULL,
  `montant_tva` decimal(12,2) NOT NULL,
  `montant_remise` decimal(12,2) NOT NULL,
  `montant_total` decimal(12,2) NOT NULL,
  `mode_paiement` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `montant_paye` decimal(12,2) NOT NULL,
  `statut` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `stock_incremente` tinyint(1) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `fichier_facture` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `enregistre_par_id` bigint DEFAULT NULL,
  `fournisseur_id` bigint NOT NULL,
  `pharmacie_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_facture` (`numero_facture`),
  KEY `facture_pharmacie_statut_idx` (`pharmacie_id`,`statut`),
  KEY `facture_fournisseur_idx` (`fournisseur_id`),
  KEY `facture_numero_idx` (`numero_facture`),
  KEY `facture_date_idx` (`date_facture`),
  KEY `facture_statut_idx` (`statut`),
  KEY `factures_fournisseurs_enregistre_par_id_65a8e59e_fk_users_id` (`enregistre_par_id`),
  CONSTRAINT `factures_fournisseurs_enregistre_par_id_65a8e59e_fk_users_id` FOREIGN KEY (`enregistre_par_id`) REFERENCES `users` (`id`),
  CONSTRAINT `factures_fournisseurs_fournisseur_id_375e387c_fk_fournisseurs_id` FOREIGN KEY (`fournisseur_id`) REFERENCES `fournisseurs` (`id`),
  CONSTRAINT `factures_fournisseurs_pharmacie_id_36dd39d4_fk_pharmacies_id` FOREIGN KEY (`pharmacie_id`) REFERENCES `pharmacies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `factures_fournisseurs`
--

LOCK TABLES `factures_fournisseurs` WRITE;
/*!40000 ALTER TABLE `factures_fournisseurs` DISABLE KEYS */;
INSERT INTO `factures_fournisseurs` VALUES (1,'FACT-2024-001','2026-02-13','2026-02-13 19:31:42.908356','2026-02-20',100000.00,18000.00,0.00,118000.00,'especes',1000000.00,'validee',1,'','','2026-02-13 19:31:42.908465','2026-02-13 19:45:08.276464',169,1,11);
/*!40000 ALTER TABLE `factures_fournisseurs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fichiers_dossiers_medicaux`
--

DROP TABLE IF EXISTS `fichiers_dossiers_medicaux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fichiers_dossiers_medicaux` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `dossier_medical_id` bigint NOT NULL,
  `type_fichier` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fichier` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom_fichier` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `taille_fichier` int DEFAULT NULL,
  `type_mime` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fichiers_do_dossier_df9ebd_idx` (`dossier_medical_id`,`type_fichier`),
  KEY `fichiers_do_created_d94269_idx` (`created_at`),
  CONSTRAINT `fichiers_dossiers_m_dossier_medical_id_fk` FOREIGN KEY (`dossier_medical_id`) REFERENCES `dossiers_medicaux` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fichiers_dossiers_medicaux`
--

LOCK TABLES `fichiers_dossiers_medicaux` WRITE;
/*!40000 ALTER TABLE `fichiers_dossiers_medicaux` DISABLE KEYS */;
INSERT INTO `fichiers_dossiers_medicaux` VALUES (1,11,'chirurgicaux','dossiers_medicaux/2026/02/12/Lettre_de_motivation_mamadoukouma.docx','Lettre_de_motivation_mamadoukouma.docx',NULL,4380,'application/vnd.openxmlformats-officedocument.wordprocessingml.document','2026-02-12 02:29:16.589744','2026-02-12 02:29:16.589762'),(2,11,'gyneco_obstetricaux','dossiers_medicaux/2026/02/12/Lettre_de_motivation.docx','Lettre_de_motivation.docx',NULL,37274,'application/vnd.openxmlformats-officedocument.wordprocessingml.document','2026-02-12 19:38:12.730859','2026-02-12 19:38:12.730881');
/*!40000 ALTER TABLE `fichiers_dossiers_medicaux` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fournisseurs`
--

DROP TABLE IF EXISTS `fournisseurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fournisseurs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `adresse` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `ville` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pays` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_registre_commerce` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_identification_fiscale` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delai_paiement_jours` int NOT NULL,
  `remise_habituelle` decimal(5,2) NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fournisseur_nom_idx` (`nom`),
  KEY `fournisseur_actif_idx` (`actif`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fournisseurs`
--

LOCK TABLES `fournisseurs` WRITE;
/*!40000 ALTER TABLE `fournisseurs` DISABLE KEYS */;
INSERT INTO `fournisseurs` VALUES (1,'SODIPHARM','medina rue 31 angle 18','Dakar','Sénégal','33 832 59 98','sodipharm@gmail.com','SN-DKR-2020-B-12345123456789','',30,0.00,1,'','2026-02-13 19:30:13.981112','2026-02-13 19:30:13.981149');
/*!40000 ALTER TABLE `fournisseurs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historique_connexions`
--

DROP TABLE IF EXISTS `historique_connexions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historique_connexions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `statut` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` char(39) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_agent` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `device_info` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_tentative` datetime(6) NOT NULL,
  `details` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `historique__user_id_cea1b7_idx` (`user_id`,`date_tentative`),
  KEY `historique__statut_b129c3_idx` (`statut`),
  KEY `historique__ip_addr_81c485_idx` (`ip_address`),
  CONSTRAINT `historique_connexions_user_id_5c3117e6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historique_connexions`
--

LOCK TABLES `historique_connexions` WRITE;
/*!40000 ALTER TABLE `historique_connexions` DISABLE KEYS */;
INSERT INTO `historique_connexions` VALUES (1,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-06 00:04:51.137754','Connexion pharmacien réussie',169),(2,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-06 01:12:45.442601','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',169),(3,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-06 01:12:57.948056','Connexion pharmacien réussie',169),(4,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-06 01:51:33.502348','Connexion pharmacien réussie',169),(5,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-06 02:01:50.423577','Connexion pharmacien réussie',169),(6,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-06 02:40:01.806472','Connexion pharmacien réussie',169),(7,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-06 02:42:30.064867','Connexion pharmacien réussie',169),(8,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-06 13:36:24.293049','Connexion pharmacien réussie',169),(9,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-06 13:45:23.723417','Connexion pharmacien réussie',169),(10,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-07 00:02:49.734674','Connexion pharmacien réussie',169),(11,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-07 01:16:40.930275','Connexion pharmacien réussie',169),(12,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-07 01:17:03.027525','Connexion pharmacien réussie',169),(13,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-07 01:17:30.071940','Connexion pharmacien réussie',169),(14,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-07 01:18:17.488101','Connexion pharmacien réussie',169),(15,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-07 01:19:10.906662','Connexion pharmacien réussie',169),(16,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-07 01:20:00.582034','Connexion pharmacien réussie',169),(17,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-07 23:06:36.334172','Connexion pharmacien réussie',169),(18,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 01:50:06.169696','Connexion pharmacien réussie',169),(19,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 01:50:59.250419','Connexion pharmacien réussie',169),(20,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 01:51:26.761392','Connexion pharmacien réussie',169),(21,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 02:02:11.983622','Connexion pharmacien réussie',169),(22,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 02:02:31.949441','Connexion pharmacien réussie',169),(23,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 02:02:50.151235','Connexion pharmacien réussie',169),(24,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 02:03:03.103624','Connexion pharmacien réussie',169),(25,'echec','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 02:04:18.394504','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Cette application est réservée aux pharmaciens uniquement.\', code=\'not_pharmacist\')]}',229),(26,'echec','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 02:04:37.538578','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Cette application est réservée aux pharmaciens uniquement.\', code=\'not_pharmacist\')]}',229),(27,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 02:21:28.875634','Connexion pharmacien réussie',169),(28,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 02:24:51.983789','Connexion pharmacien réussie',169),(29,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 02:29:23.911615','Connexion pharmacien réussie',169),(30,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 02:30:17.674994','Connexion pharmacien réussie',169),(31,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 02:30:37.242317','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',229),(32,'echec','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 02:46:13.363609','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',229),(33,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 02:55:29.165966','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',229),(34,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 02:56:37.906877','Connexion pharmacien réussie',169),(35,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 02:58:54.988097','Connexion pharmacien réussie',169),(36,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:00:40.926978','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',170),(37,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:00:58.852403','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',170),(38,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:01:15.084875','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',170),(39,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:02:11.063019','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',170),(40,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:02:13.191267','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',170),(41,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:02:14.784218','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',170),(42,'succes','127.0.0.1','curl/8.7.1','Inconnu sur Inconnu','','2026-01-08 03:04:05.272945','Connexion pharmacien réussie',170),(43,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:04:32.749521','Connexion pharmacien réussie',170),(44,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:27:55.657592','Connexion pharmacien réussie',169),(45,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 03:34:41.857469','Connexion pharmacien réussie',170),(46,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 12:50:26.820951','Connexion pharmacien réussie',169),(47,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-08 18:12:32.122299','Connexion pharmacien réussie',169),(48,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-09 17:04:43.221542','Connexion pharmacien réussie',169),(49,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-09 18:17:00.115734','Connexion pharmacien réussie',169),(50,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-09 18:59:45.732885','Connexion pharmacien réussie',169),(51,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-11 22:04:25.840993','Connexion pharmacien réussie',169),(52,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-11 22:14:45.471026','Connexion pharmacien réussie',169),(53,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-19 01:00:17.728795','Connexion pharmacien réussie',169),(54,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15','Safari sur macOS','','2026-01-26 18:06:04.212105','Connexion pharmacien réussie',169),(55,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-01-28 18:38:49.531626','Connexion pharmacien réussie',169),(56,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-08 07:35:28.224100','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',157),(57,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-08 07:35:56.389108','Connexion hôpital réussie',157),(58,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-08 07:38:30.566148','Connexion hôpital réussie',157),(59,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-08 07:39:19.878309','Connexion hôpital réussie',154),(60,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-10 13:51:50.279135','Connexion hôpital réussie',154),(61,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-10 13:57:09.776979','Connexion hôpital réussie',168),(62,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-11 21:43:26.109709','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(63,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-11 21:43:57.640597','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',229),(64,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-11 21:43:59.183113','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',229),(65,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-11 21:44:09.554785','Connexion pharmacien réussie',170),(66,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 00:38:33.021942','Connexion pharmacien réussie',233),(67,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 00:42:43.166886','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(68,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 00:42:46.092172','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(69,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 00:44:13.837008','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',171),(70,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 00:44:23.400264','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',171),(71,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:25:31.790866','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',229),(72,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:26:00.490402','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(73,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:27:32.891497','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(74,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:28:36.180977','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(75,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:28:50.179007','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(76,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:38:23.177012','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(77,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:38:25.519852','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(78,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:48:35.602882','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(79,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:49:03.533510','Connexion pharmacien réussie',169),(80,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:55:49.411942','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(81,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 01:55:58.293807','Connexion pharmacien réussie',169),(82,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 21:01:26.484677','Connexion pharmacien réussie',169),(83,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 21:01:42.332570','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',229),(84,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 21:01:45.024674','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',229),(85,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-12 21:02:00.278206','Connexion pharmacien réussie',170),(86,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 13:54:24.423141','Connexion pharmacien réussie',169),(87,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 19:55:32.198051','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',234),(88,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 19:55:55.402769','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Cette application est réservée aux pharmaciens et employés de pharmacie uniquement.\', code=\'not_pharmacy_user\')]}',157),(89,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 19:56:04.389522','Connexion pharmacien réussie',169),(90,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 19:57:20.497957','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',169),(91,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 19:57:31.115548','Connexion pharmacien réussie',169),(92,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 19:57:40.561337','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Ce compte utilisateur est désactivé. Contactez votre administrateur.\', code=\'invalid\')]}',234),(93,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 19:59:48.512051','Connexion pharmacien réussie',169),(94,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:01:05.071364','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\"Aucune pharmacie n\'est associée à ce compte. Contactez l\'administrateur système.\", code=\'no_pharmacy\')]}',234),(95,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:01:20.169343','Connexion pharmacien réussie',169),(96,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:01:41.697403','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\"Aucune pharmacie n\'est associée à ce compte. Contactez l\'administrateur système.\", code=\'no_pharmacy\')]}',234),(97,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:05:04.969550','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\"Aucune pharmacie n\'est associée à ce compte. Contactez l\'administrateur système.\", code=\'no_pharmacy\')]}',234),(98,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:05:06.195310','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\"Aucune pharmacie n\'est associée à ce compte. Contactez l\'administrateur système.\", code=\'no_pharmacy\')]}',234),(99,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:06:00.928656','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\"Aucune pharmacie n\'est associée à ce compte. Contactez l\'administrateur système.\", code=\'no_pharmacy\')]}',234),(100,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:06:32.659211','Connexion pharmacien réussie',169),(101,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:07:38.899394','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',234),(102,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:07:46.625349','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\"Aucune pharmacie n\'est associée à ce compte. Contactez l\'administrateur système.\", code=\'no_pharmacy\')]}',234),(103,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:07:55.112296','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\'Mot de passe incorrect.\', code=\'invalid\')]}',234),(104,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:08:01.965103','Connexion pharmacien réussie',169),(105,'echec','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:08:53.557674','Échec de connexion: {\'non_field_errors\': [ErrorDetail(string=\"Aucune pharmacie n\'est associée à ce compte. Contactez l\'administrateur système.\", code=\'no_pharmacy\')]}',234),(106,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:14:58.322059','Connexion pharmacien réussie',169),(107,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:15:21.276403','Connexion pharmacien réussie',234),(108,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:15:39.872848','Connexion pharmacien réussie',169),(109,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 20:16:25.510761','Connexion pharmacien réussie',234),(110,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 23:18:04.425347','Connexion pharmacien réussie',169),(111,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 23:19:10.382592','Connexion pharmacien réussie',169),(112,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 23:19:28.540578','Connexion pharmacien réussie',232),(113,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 23:20:10.693049','Connexion pharmacien réussie',169),(114,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-13 23:22:39.872222','Connexion pharmacien réussie',242),(115,'succes','127.0.0.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15','Safari sur macOS','','2026-02-14 00:41:35.703287','Connexion pharmacien réussie',169);
/*!40000 ALTER TABLE `historique_connexions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hopitaux`
--

DROP TABLE IF EXISTS `hopitaux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hopitaux` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code_hopital` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `adresse` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `ville` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pays` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `couleur_theme` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `horaires_ouverture` json NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `date_inscription` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `admin_hopital_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_hopital` (`code_hopital`),
  KEY `hopitaux_code_ho_751aa6_idx` (`code_hopital`),
  KEY `hopitaux_ville_d893cc_idx` (`ville`),
  KEY `hopitaux_actif_80d873_idx` (`actif`),
  KEY `hopitaux_admin_hopital_id_831174a3_fk_users_id` (`admin_hopital_id`),
  CONSTRAINT `hopitaux_admin_hopital_id_831174a3_fk_users_id` FOREIGN KEY (`admin_hopital_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hopitaux`
--

LOCK TABLES `hopitaux` WRITE;
/*!40000 ALTER TABLE `hopitaux` DISABLE KEYS */;
INSERT INTO `hopitaux` VALUES (7,'Hôpital Abass Ndao','HAN001','Route de l\'aéroport, Dakar','Dakar','Sénégal','+221338234567','contact@abassndao.sn',14.684152,-17.451327,'','#0066CC','','{}',1,'2025-12-27 04:08:59.370783','2025-12-27 04:08:59.370817','2026-01-28 13:47:15.514002',154),(8,'Hôpital Aristide Le Dantec','HALD002','Avenue Pasteur, Dakar','Dakar','Sénégal','+221338891234','contact@ledantec.sn',14.692800,-17.446700,'','#0066CC','','{}',1,'2025-12-27 04:08:59.375556','2025-12-27 04:08:59.375574','2025-12-27 04:08:59.375578',155),(9,'Hôpital Dalal Jamm','HDJ003','Guédiawaye, Dakar','Guédiawaye','Sénégal','+221338567890','contact@dalaljamm.sn',14.766700,-17.416700,'','#0066CC','','{}',1,'2025-12-27 04:08:59.378832','2025-12-27 04:08:59.378866','2026-02-08 07:35:44.159682',156),(14,'centre de lafiabougou','CLA0234','Lafiabougou bougoudani','Bamako','Mali','+223 75 09 79 85','admin.lafia@lafia.com',NULL,NULL,'','#0066CC','','{}',1,'2026-02-05 08:06:58.150101','2026-02-05 08:06:58.150130','2026-02-05 08:06:58.308551',238);
/*!40000 ALTER TABLE `hopitaux` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `landing_page_content`
--

DROP TABLE IF EXISTS `landing_page_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `landing_page_content` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `logo_text` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hero_title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hero_description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `hero_button_primary` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hero_button_secondary` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `about_title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `about_description_1` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `about_description_2` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `about_stat_1_value` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `about_stat_1_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `about_stat_2_value` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `about_stat_2_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `services_title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `services_subtitle` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `values_title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `values_subtitle` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `footer_about_text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `footer_address` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `footer_phone` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `footer_email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `footer_facebook` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `footer_twitter` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `footer_instagram` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `footer_linkedin` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landing_page_content`
--

LOCK TABLES `landing_page_content` WRITE;
/*!40000 ALTER TABLE `landing_page_content` DISABLE KEYS */;
INSERT INTO `landing_page_content` VALUES (1,'E-sora','Votre Santé, Notre Priorité','Centre d\'excellence en santé reproductive et planification familiale au Sénégal.','Prendre Rendez-vous','En savoir plus','À propos d\'E-Sora','L\'application E-sora est une application de référence en matière de santé reproductive et de planification familiale au Sénégal.','Nous offrons des soins de qualité avec une équipe de professionnels expérimentés et des équipements modernes.','12+','Années d\'expérience','50+','Professionnels de santé','Nos Services','Une gamme complète de services de santé reproductive','Nos Valeurs','Ce qui nous guide dans notre mission','Votre partenaire de confiance pour la santé reproductive et le bien-être.','Route de l\'aéroport, Dakar, Sénégal','+221 33 823 45 67','contact@e-sora.sn',NULL,NULL,NULL,NULL,'2025-12-27 04:13:13.173753','2025-12-28 00:51:04.343036');
/*!40000 ALTER TABLE `landing_page_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lignes_commandes`
--

DROP TABLE IF EXISTS `lignes_commandes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lignes_commandes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantite` int NOT NULL,
  `prix_unitaire` decimal(10,2) NOT NULL,
  `prix_total` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `commande_id` bigint NOT NULL,
  `produit_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lignes_commandes_commande_id_produit_id_d69dcf31_uniq` (`commande_id`,`produit_id`),
  KEY `lignes_commandes_produit_id_aea3785c_fk_produits_id` (`produit_id`),
  CONSTRAINT `lignes_commandes_commande_id_5809a881_fk_commandes_pharmacies_id` FOREIGN KEY (`commande_id`) REFERENCES `commandes_pharmacies` (`id`),
  CONSTRAINT `lignes_commandes_produit_id_aea3785c_fk_produits_id` FOREIGN KEY (`produit_id`) REFERENCES `produits` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=221 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lignes_commandes`
--

LOCK TABLES `lignes_commandes` WRITE;
/*!40000 ALTER TABLE `lignes_commandes` DISABLE KEYS */;
INSERT INTO `lignes_commandes` VALUES (138,1,3000.00,3000.00,'2025-12-27 04:08:59.700972',61,27),(139,3,1200.00,3600.00,'2025-12-27 04:08:59.701432',61,23),(140,3,750.00,2250.00,'2025-12-27 04:08:59.707696',62,22),(141,1,1200.00,1200.00,'2025-12-27 04:08:59.713706',63,30),(142,1,500.00,500.00,'2025-12-27 04:08:59.714214',63,21),(143,1,1500.00,1500.00,'2025-12-27 04:08:59.714748',63,25),(144,1,1500.00,1500.00,'2025-12-27 04:08:59.716798',64,25),(145,3,750.00,2250.00,'2025-12-27 04:08:59.717134',64,22),(146,1,2000.00,2000.00,'2025-12-27 04:08:59.717428',64,26),(147,1,1500.00,1500.00,'2025-12-27 04:08:59.720333',65,25),(148,1,500.00,500.00,'2025-12-27 04:08:59.720688',65,21),(149,1,2200.00,2200.00,'2025-12-27 04:08:59.721037',65,28),(150,2,1200.00,2400.00,'2025-12-27 04:08:59.722955',66,30),(151,1,2500.00,2500.00,'2025-12-27 04:08:59.723294',66,24),(152,2,1500.00,3000.00,'2025-12-27 04:08:59.725619',67,25),(153,1,2200.00,2200.00,'2025-12-27 04:08:59.728005',67,28),(154,1,2200.00,2200.00,'2025-12-27 04:08:59.733223',68,28),(155,3,1500.00,4500.00,'2025-12-27 04:08:59.736369',69,25),(156,3,1500.00,4500.00,'2025-12-27 04:08:59.738418',70,25),(157,1,800.00,800.00,'2025-12-27 04:08:59.738751',70,29),(158,2,3000.00,6000.00,'2025-12-27 04:08:59.739112',70,27),(159,2,2000.00,4000.00,'2025-12-27 04:08:59.739443',70,26),(160,1,1500.00,1500.00,'2025-12-27 04:08:59.741943',71,25),(161,2,1200.00,2400.00,'2025-12-27 04:08:59.742282',71,23),(162,2,3000.00,6000.00,'2025-12-27 04:08:59.742608',71,27),(163,2,2000.00,4000.00,'2025-12-27 04:08:59.742953',71,26),(164,1,2000.00,2000.00,'2025-12-27 04:08:59.745352',72,26),(165,2,2500.00,5000.00,'2025-12-27 04:08:59.745667',72,24),(166,1,1200.00,1200.00,'2025-12-27 04:08:59.746286',72,23),(167,1,800.00,800.00,'2025-12-27 04:08:59.748600',73,29),(168,2,1200.00,2400.00,'2025-12-27 04:08:59.749092',73,23),(169,1,1200.00,1200.00,'2025-12-27 04:08:59.751663',74,23),(170,3,3000.00,9000.00,'2025-12-27 04:08:59.752114',74,27),(171,2,1200.00,2400.00,'2025-12-27 04:08:59.754306',75,23),(172,3,2200.00,6600.00,'2025-12-27 04:08:59.754745',75,28),(173,1,1500.00,1500.00,'2025-12-27 04:08:59.756775',76,25),(174,3,750.00,2250.00,'2025-12-27 04:08:59.757131',76,22),(175,2,500.00,1000.00,'2025-12-27 04:08:59.757489',76,21),(176,1,2500.00,2500.00,'2025-12-27 04:08:59.759690',77,24),(177,1,2000.00,2000.00,'2025-12-27 04:08:59.760109',77,26),(178,2,800.00,1600.00,'2025-12-27 04:08:59.760494',77,29),(179,1,2200.00,2200.00,'2025-12-27 04:08:59.760975',77,28),(180,3,1500.00,4500.00,'2025-12-27 04:08:59.765698',78,25),(181,3,1200.00,3600.00,'2025-12-27 04:08:59.766190',78,23),(182,2,2000.00,4000.00,'2025-12-27 04:08:59.766710',78,26),(183,1,3000.00,3000.00,'2025-12-27 04:08:59.767116',78,27),(184,2,1500.00,3000.00,'2025-12-27 04:08:59.772695',79,25),(185,1,2500.00,2500.00,'2025-12-27 04:08:59.772994',79,24),(186,3,800.00,2400.00,'2025-12-27 04:08:59.775985',80,29),(187,3,1500.00,4500.00,'2025-12-27 04:08:59.776325',80,25),(188,1,750.00,750.00,'2025-12-27 04:08:59.776899',80,22),(189,3,1200.00,3600.00,'2025-12-27 04:08:59.777324',80,23),(190,1,750.00,750.00,'2025-12-27 04:08:59.779817',81,22),(191,2,800.00,1600.00,'2025-12-27 04:08:59.780158',81,29),(192,2,2000.00,4000.00,'2025-12-27 04:08:59.780512',81,26),(193,2,500.00,1000.00,'2025-12-27 04:08:59.781061',81,21),(194,1,2000.00,2000.00,'2025-12-27 04:08:59.785084',82,26),(195,3,500.00,1500.00,'2025-12-27 04:08:59.785706',82,21),(196,1,2200.00,2200.00,'2025-12-27 04:08:59.786100',82,28),(197,1,1200.00,1200.00,'2025-12-27 04:08:59.786438',82,30),(198,1,1200.00,1200.00,'2025-12-27 04:08:59.789479',83,23),(199,2,500.00,1000.00,'2025-12-27 04:08:59.790401',83,21),(200,3,1200.00,3600.00,'2025-12-27 04:08:59.791871',83,30),(201,1,800.00,800.00,'2025-12-27 04:08:59.792532',83,29),(202,3,500.00,1500.00,'2025-12-27 04:08:59.795003',84,21),(203,2,750.00,1500.00,'2025-12-27 04:08:59.795369',84,22),(204,1,1200.00,1200.00,'2025-12-27 04:08:59.797231',85,30),(205,1,3000.00,3000.00,'2025-12-27 04:08:59.797723',85,27),(206,1,1500.00,1500.00,'2025-12-27 04:08:59.798585',85,25),(207,3,750.00,2250.00,'2025-12-27 04:08:59.801235',86,22),(208,1,2200.00,2200.00,'2025-12-27 04:08:59.802428',86,28),(209,3,500.00,1500.00,'2025-12-27 04:08:59.803354',86,21),(210,3,2000.00,6000.00,'2025-12-27 04:08:59.805628',87,26),(211,2,3000.00,6000.00,'2025-12-27 04:08:59.807454',87,27),(212,2,2500.00,5000.00,'2025-12-27 04:08:59.808797',87,24),(213,3,500.00,1500.00,'2025-12-27 04:08:59.809784',87,21),(214,3,2500.00,7500.00,'2025-12-27 04:08:59.812407',88,24),(215,1,1500.00,1500.00,'2025-12-27 04:08:59.814769',89,25),(216,2,750.00,1500.00,'2025-12-27 04:08:59.815368',89,22),(217,1,2500.00,2500.00,'2025-12-27 04:08:59.815686',89,24),(218,1,500.00,500.00,'2025-12-27 04:08:59.818262',90,21),(219,2,1500.00,3000.00,'2025-12-27 04:08:59.818575',90,25),(220,1,1200.00,1200.00,'2025-12-27 04:08:59.818877',90,30);
/*!40000 ALTER TABLE `lignes_commandes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lignes_factures_fournisseurs`
--

DROP TABLE IF EXISTS `lignes_factures_fournisseurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lignes_factures_fournisseurs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom_produit` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantite` int NOT NULL,
  `prix_unitaire_ht` decimal(10,2) NOT NULL,
  `taux_tva` decimal(5,2) NOT NULL,
  `remise_ligne` decimal(10,2) NOT NULL,
  `montant_ht` decimal(12,2) NOT NULL,
  `montant_tva` decimal(12,2) NOT NULL,
  `montant_ttc` decimal(12,2) NOT NULL,
  `numero_lot` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_peremption` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `facture_id` bigint NOT NULL,
  `produit_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ligne_facture_idx` (`facture_id`),
  KEY `ligne_produit_idx` (`produit_id`),
  CONSTRAINT `lignes_factures_four_facture_id_05920908_fk_factures_` FOREIGN KEY (`facture_id`) REFERENCES `factures_fournisseurs` (`id`),
  CONSTRAINT `lignes_factures_fournisseurs_produit_id_cd3189ce_fk_produits_id` FOREIGN KEY (`produit_id`) REFERENCES `produits` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lignes_factures_fournisseurs`
--

LOCK TABLES `lignes_factures_fournisseurs` WRITE;
/*!40000 ALTER TABLE `lignes_factures_fournisseurs` DISABLE KEYS */;
INSERT INTO `lignes_factures_fournisseurs` VALUES (1,'Amoxicilline 500mg',1000,100.00,18.00,0.00,100000.00,18000.00,118000.00,'LOT-2024-001','2026-05-23','2026-02-13 19:31:42.915834','2026-02-13 19:31:42.915847',1,23);
/*!40000 ALTER TABLE `lignes_factures_fournisseurs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lignes_ordonnances`
--

DROP TABLE IF EXISTS `lignes_ordonnances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lignes_ordonnances` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom_medicament` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dosage` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantite` decimal(8,2) NOT NULL,
  `unite` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `frequence` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `frequence_detail` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `moment_prise` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duree_traitement` int NOT NULL,
  `instructions` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantite_totale` decimal(10,2) DEFAULT NULL,
  `ordre` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `produit_id` bigint DEFAULT NULL,
  `ordonnance_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lignes_ordo_ordonna_ae303a_idx` (`ordonnance_id`,`ordre`),
  KEY `lignes_ordonnances_produit_id_e4c44a4a_fk_produits_id` (`produit_id`),
  CONSTRAINT `lignes_ordonnances_ordonnance_id_da4a2ca8_fk_ordonnances_id` FOREIGN KEY (`ordonnance_id`) REFERENCES `ordonnances` (`id`),
  CONSTRAINT `lignes_ordonnances_produit_id_e4c44a4a_fk_produits_id` FOREIGN KEY (`produit_id`) REFERENCES `produits` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lignes_ordonnances`
--

LOCK TABLES `lignes_ordonnances` WRITE;
/*!40000 ALTER TABLE `lignes_ordonnances` DISABLE KEYS */;
INSERT INTO `lignes_ordonnances` VALUES (1,'Paracétamol','500mg',1.00,'comprime','3_fois_jour','','apres_repas',7,'Après les repas',21.00,0,'2026-01-22 22:30:19.296394',NULL,2),(2,'Ibuprofène','200mg',1.00,'comprime','2_fois_jour','','apres_repas',5,'Avec de la nourriture',10.00,0,'2026-01-22 22:30:19.330612',NULL,2),(3,'Aspirine','100mg',1.00,'comprime','1_fois_jour','','apres_repas',10,'Avec beaucoup d eau',10.00,1,'2026-01-22 22:37:20.043106',NULL,3),(4,'paracetamol','1000',2.00,'comprime','3_fois_jour','','apres_repas',13,'',78.00,1,'2026-01-24 20:21:41.744426',NULL,4),(5,'ibuprofène ','700',2.00,'comprime','3_fois_jour','','apres_repas',11,'',66.00,1,'2026-01-27 21:36:43.155614',NULL,5),(6,'paracetamol','1000',1.00,'comprime','4_fois_jour','','apres_repas',6,'',24.00,2,'2026-01-27 21:36:43.174879',NULL,5),(7,'paracetamol','1000',2.00,'comprime','4_fois_jour','','apres_repas',10,'',80.00,1,'2026-02-01 05:37:33.401255',NULL,6),(8,'anti douleur','1000',3.00,'comprime','3_fois_jour','','apres_repas',3,'',27.00,1,'2026-02-02 22:45:04.444963',NULL,7),(9,'paracetamol','1000',1.00,'comprime','1_fois_jour','','apres_repas',1,'',1.00,1,'2026-02-03 18:11:26.370742',NULL,8),(10,'Préservatifs Durex','500',1.00,'autre','1_fois_jour','','apres_repas',1,'',1.00,1,'2026-02-05 20:23:10.835238',NULL,9);
/*!40000 ALTER TABLE `lignes_ordonnances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lignes_ventes`
--

DROP TABLE IF EXISTS `lignes_ventes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lignes_ventes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantite` int NOT NULL,
  `prix_unitaire` decimal(10,2) NOT NULL,
  `prix_total` decimal(10,2) NOT NULL,
  `remise_pourcentage` decimal(5,2) NOT NULL,
  `remise_montant` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `produit_id` bigint NOT NULL,
  `stock_produit_id` bigint NOT NULL,
  `vente_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lignes_ventes_vente_id_produit_id_c97e4873_uniq` (`vente_id`,`produit_id`),
  KEY `lignes_ventes_produit_id_af5da834_fk_produits_id` (`produit_id`),
  KEY `lignes_ventes_stock_produit_id_33408288_fk_stocks_produits_id` (`stock_produit_id`),
  CONSTRAINT `lignes_ventes_produit_id_af5da834_fk_produits_id` FOREIGN KEY (`produit_id`) REFERENCES `produits` (`id`),
  CONSTRAINT `lignes_ventes_stock_produit_id_33408288_fk_stocks_produits_id` FOREIGN KEY (`stock_produit_id`) REFERENCES `stocks_produits` (`id`),
  CONSTRAINT `lignes_ventes_vente_id_58de3017_fk_ventes_pharmacies_id` FOREIGN KEY (`vente_id`) REFERENCES `ventes_pharmacies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lignes_ventes`
--

LOCK TABLES `lignes_ventes` WRITE;
/*!40000 ALTER TABLE `lignes_ventes` DISABLE KEYS */;
INSERT INTO `lignes_ventes` VALUES (3,1,992.25,992.25,0.00,0.00,'2026-01-07 00:42:43.705086',22,66,3),(4,2,992.25,1885.28,5.00,99.23,'2026-01-07 00:58:49.795621',22,66,4),(5,1,1407.31,1407.31,0.00,0.00,'2026-01-07 01:07:48.498840',23,70,5),(6,1,1407.31,1407.31,0.00,0.00,'2026-01-07 22:22:54.108132',23,70,6),(7,1,992.25,992.25,0.00,0.00,'2026-01-07 22:22:54.115298',22,66,6),(8,2,750.00,1500.00,0.00,0.00,'2026-01-08 02:02:50.724292',22,66,8),(9,1,750.00,750.00,0.00,0.00,'2026-01-08 02:05:45.428873',22,66,9),(10,2,1407.31,2814.62,0.00,0.00,'2026-01-11 22:07:59.907903',23,70,10),(11,3,1407.31,4221.93,0.00,0.00,'2026-01-26 18:12:19.216311',23,70,11),(12,1,998.59,998.59,0.00,0.00,'2026-02-12 00:14:48.451405',29,98,12);
/*!40000 ALTER TABLE `lignes_ventes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `methodes_contraceptives`
--

DROP TABLE IF EXISTS `methodes_contraceptives`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `methodes_contraceptives` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `categorie` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `methodes_contraceptives`
--

LOCK TABLES `methodes_contraceptives` WRITE;
/*!40000 ALTER TABLE `methodes_contraceptives` DISABLE KEYS */;
INSERT INTO `methodes_contraceptives` VALUES (29,'Pilule combinée','hormonale','Contraceptif oral combiné œstrogène-progestatif','2025-12-27 04:08:59.541058','2025-12-27 04:08:59.541064'),(30,'Pilule progestative','hormonale','Contraceptif oral à base de progestatif seul','2025-12-27 04:08:59.541422','2025-12-27 04:08:59.541427'),(31,'Implant contraceptif','hormonale','Implant sous-cutané libérant des hormones','2025-12-27 04:08:59.541872','2025-12-27 04:08:59.541876'),(32,'Injection contraceptive','hormonale','Injection trimestrielle de progestatif','2025-12-27 04:08:59.542554','2025-12-27 04:08:59.542563'),(33,'DIU hormonal','iud','Dispositif intra-utérin libérant des hormones','2025-12-27 04:08:59.543025','2025-12-27 04:08:59.543031'),(34,'DIU au cuivre','iud','Dispositif intra-utérin en cuivre','2025-12-27 04:08:59.543503','2025-12-27 04:08:59.543509'),(35,'Préservatif masculin','barriere','Protection mécanique masculine','2025-12-27 04:08:59.544009','2025-12-27 04:08:59.544014'),(36,'Préservatif féminin','barriere','Protection mécanique féminine','2025-12-27 04:08:59.544340','2025-12-27 04:08:59.544344'),(37,'Diaphragme','barriere','Coupelle contraceptive','2025-12-27 04:08:59.544663','2025-12-27 04:08:59.544667'),(38,'Spermicides','barriere','Produits chimiques contraceptifs','2025-12-27 04:08:59.545126','2025-12-27 04:08:59.545130'),(39,'Stérilisation féminine','permanent','Ligature des trompes','2025-12-27 04:08:59.545606','2025-12-27 04:08:59.545610'),(40,'Stérilisation masculine','permanent','Vasectomie','2025-12-27 04:08:59.546059','2025-12-27 04:08:59.546064'),(41,'Méthode des températures','naturelle','Observation de la température basale','2025-12-27 04:08:59.547033','2025-12-27 04:08:59.547039'),(42,'Méthode Billings','naturelle','Observation de la glaire cervicale','2025-12-27 04:08:59.547488','2025-12-27 04:08:59.547493');
/*!40000 ALTER TABLE `methodes_contraceptives` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mouvements_stock`
--

DROP TABLE IF EXISTS `mouvements_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mouvements_stock` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_mouvement` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantite` int NOT NULL,
  `motif` longtext COLLATE utf8mb4_unicode_ci,
  `date_mouvement` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `stock_item_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mouvements__date_mo_5995a9_idx` (`date_mouvement`),
  KEY `mouvements__type_mo_85e8dd_idx` (`type_mouvement`),
  KEY `mouvements_stock_user_id_22f56fab_fk_users_id` (`user_id`),
  KEY `mouvements_stock_stock_item_id_593ee056_fk_stocks_id` (`stock_item_id`),
  CONSTRAINT `mouvements_stock_stock_item_id_593ee056_fk_stocks_id` FOREIGN KEY (`stock_item_id`) REFERENCES `stocks` (`id`),
  CONSTRAINT `mouvements_stock_user_id_22f56fab_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mouvements_stock`
--

LOCK TABLES `mouvements_stock` WRITE;
/*!40000 ALTER TABLE `mouvements_stock` DISABLE KEYS */;
INSERT INTO `mouvements_stock` VALUES (101,'entree',43,'Correction inventaire','2025-12-27 04:08:59.884422',170,87),(102,'entree',42,'Casse','2025-12-27 04:08:59.884839',169,88),(103,'entree',24,'Correction inventaire','2025-12-27 04:08:59.886553',172,89),(104,'sortie',48,'Réapprovisionnement','2025-12-27 04:08:59.887205',171,66),(105,'perte',37,'Casse','2025-12-27 04:08:59.887633',172,70),(106,'sortie',9,'Produit périmé','2025-12-27 04:08:59.887950',170,86),(107,'perte',40,'Réapprovisionnement','2025-12-27 04:08:59.888247',172,67),(108,'perte',30,'Réapprovisionnement','2025-12-27 04:08:59.888638',173,68),(109,'inventaire',33,'Casse','2025-12-27 04:08:59.889067',169,86),(110,'entree',6,'Produit périmé','2025-12-27 04:08:59.889491',170,78),(111,'sortie',30,'Réapprovisionnement','2025-12-27 04:08:59.890205',173,68),(112,'sortie',41,'Produit périmé','2025-12-27 04:08:59.890969',153,65),(113,'sortie',1,'Réapprovisionnement','2025-12-27 04:08:59.891998',173,66),(114,'entree',8,'Produit périmé','2025-12-27 04:08:59.892355',153,73),(115,'sortie',47,'Produit périmé','2025-12-27 04:08:59.892683',170,80),(116,'entree',40,'Produit périmé','2025-12-27 04:08:59.893064',169,85),(117,'entree',30,'Casse','2025-12-27 04:08:59.893662',153,67),(118,'perte',8,'Vente','2025-12-27 04:08:59.894568',172,65),(119,'perte',37,'Réapprovisionnement','2025-12-27 04:08:59.894969',169,62),(120,'perte',36,'Réapprovisionnement','2025-12-27 04:08:59.895313',153,76),(121,'inventaire',18,'Vente','2025-12-27 04:08:59.895581',169,75),(122,'sortie',13,'Réapprovisionnement','2025-12-27 04:08:59.896063',170,63),(123,'perte',33,'Réapprovisionnement','2025-12-27 04:08:59.896652',172,62),(124,'sortie',35,'Casse','2025-12-27 04:08:59.897058',171,67),(125,'sortie',21,'Réapprovisionnement','2025-12-27 04:08:59.897374',173,70),(126,'sortie',35,'Correction inventaire','2025-12-27 04:08:59.897805',170,87),(127,'entree',40,'Produit périmé','2025-12-27 04:08:59.898184',153,61),(128,'sortie',37,'Réapprovisionnement','2025-12-27 04:08:59.898599',171,66),(129,'inventaire',26,'Produit périmé','2025-12-27 04:08:59.899164',153,70),(130,'sortie',30,'Correction inventaire','2025-12-27 04:08:59.899858',169,78),(131,'entree',17,'Correction inventaire','2025-12-27 04:08:59.900509',169,86),(132,'entree',15,'Correction inventaire','2025-12-27 04:08:59.900846',173,84),(133,'perte',1,'Vente','2025-12-27 04:08:59.901207',153,83),(134,'inventaire',8,'Réapprovisionnement','2025-12-27 04:08:59.901813',169,88),(135,'entree',40,'Correction inventaire','2025-12-27 04:08:59.902977',153,82),(136,'sortie',42,'Vente','2025-12-27 04:08:59.903601',173,86),(137,'inventaire',18,'Réapprovisionnement','2025-12-27 04:08:59.904008',173,88),(138,'entree',39,'Réapprovisionnement','2025-12-27 04:08:59.904399',173,89),(139,'inventaire',16,'Correction inventaire','2025-12-27 04:08:59.904943',173,76),(140,'sortie',46,'Produit périmé','2025-12-27 04:08:59.905389',171,63),(141,'inventaire',16,'Vente','2025-12-27 04:08:59.905719',173,64),(142,'inventaire',17,'Produit périmé','2025-12-27 04:08:59.906017',173,70),(143,'sortie',44,'Produit périmé','2025-12-27 04:08:59.906277',171,84),(144,'entree',48,'Réapprovisionnement','2025-12-27 04:08:59.906542',173,64),(145,'sortie',1,'Réapprovisionnement','2025-12-27 04:08:59.906869',171,63),(146,'perte',24,'Correction inventaire','2025-12-27 04:08:59.907181',171,86),(147,'inventaire',45,'Casse','2025-12-27 04:08:59.907453',169,63),(148,'entree',42,'Réapprovisionnement','2025-12-27 04:08:59.907727',170,87),(149,'perte',34,'Casse','2025-12-27 04:08:59.908549',172,90),(150,'entree',21,'Vente','2025-12-27 04:08:59.909373',170,80);
/*!40000 ALTER TABLE `mouvements_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_notification` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `titre` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `data` json NOT NULL,
  `lu` tinyint(1) NOT NULL,
  `date_lecture` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `commande_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `rendez_vous_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `notificatio_user_id_c971fe_idx` (`user_id`,`lu`),
  KEY `notificatio_created_e4c995_idx` (`created_at`),
  KEY `notifications_commande_id_ab0d2bae_fk_commandes_pharmacies_id` (`commande_id`),
  KEY `notifications_rendez_vous_id_936a6639_fk_rendez_vous_id` (`rendez_vous_id`),
  CONSTRAINT `notifications_commande_id_ab0d2bae_fk_commandes_pharmacies_id` FOREIGN KEY (`commande_id`) REFERENCES `commandes_pharmacies` (`id`),
  CONSTRAINT `notifications_rendez_vous_id_936a6639_fk_rendez_vous_id` FOREIGN KEY (`rendez_vous_id`) REFERENCES `rendez_vous` (`id`),
  CONSTRAINT `notifications_user_id_468e288d_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=325 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (101,'commande_prete','Travailler revoir valeur huit disposer.','Voie éclater mémoire particulier vague enfant. Certainement médecin champ habitude désespoir lit.\nRencontre fixer rester ouvrir vaincre. Depuis garder falloir. Intérieur semaine entretenir fort.','{}',1,NULL,'2025-12-27 04:08:59.821034',NULL,164,NULL),(102,'commande_prete','Veiller si.','Liberté âgé demain ennemi ouvrir envoyer avouer inutile. Six devant an. Briser debout mois rire passer.','{}',0,NULL,'2025-12-27 04:08:59.821767',NULL,185,NULL),(103,'rendez_vous_confirme','Tracer tout pain affaire.','Asseoir demain immense carte jusque précipiter. Colline inviter regard vingt spectacle poussière long.','{}',1,NULL,'2025-12-27 04:08:59.822935',NULL,164,NULL),(104,'commande_prete','Gens loup réalité règle fin.','Époque promener lien obéir forêt veiller donc. Feu garçon sol français accorder centre parole. Abri saint jardin marquer quartier détacher paraître.','{}',1,NULL,'2025-12-27 04:08:59.825918',NULL,185,NULL),(105,'rendez_vous_rappel','Place poitrine sable de.','Nommer heure bleu histoire pousser immense. Trois chiffre comme maître affirmer.\nPremier mais profondément air île centre apprendre. Volonté monsieur accrocher enfant fait premier machine.','{}',1,NULL,'2025-12-27 04:08:59.826548',NULL,179,NULL),(106,'commande_confirmee','Devoir effort voir sept inviter.','Falloir deviner soldat. Chaque parce que eaux pénétrer dangereux accrocher établir. Corde volonté assurer course voir gros. Bas confondre remercier mer oui.','{}',1,NULL,'2025-12-27 04:08:59.827321',NULL,195,NULL),(107,'consultation_rapport','Pluie coucher ramasser tirer.','Coucher disposer deviner montrer témoin. Notre exiger exécuter pain puis cause prison blanc. Voie marche plan suite réussir nouveau. Voiture ce soleil soirée.','{}',0,NULL,'2025-12-27 04:08:59.828039',NULL,223,NULL),(108,'rendez_vous_rappel','Fumée lit.','Puissance main seigneur preuve avec. Écraser toucher fort robe histoire endroit. Baisser musique vous feu.','{}',0,NULL,'2025-12-27 04:08:59.828621',NULL,215,NULL),(109,'commande_confirmee','Officier obéir pouvoir loin flamme.','D\'Abord devant rêver absolu quel santé traverser. Garçon livrer fixe six. Refuser note page mauvais être livrer race.','{}',1,NULL,'2025-12-27 04:08:59.829096',NULL,192,NULL),(110,'rendez_vous_rappel','Défaut paquet tel double.','Pour officier veiller image autrement. Énergie suivre élément accuser paix. Homme rapide saint côte même partir.','{}',1,NULL,'2025-12-27 04:08:59.829514',NULL,219,NULL),(111,'consultation_rapport','Montagne bois déposer.','As suivre vivant drôle. Réunir résoudre précieux son reste train. Convenir ensuite faim confondre passé envelopper parce que.\nEst deux personne nu montrer couler.','{}',1,NULL,'2025-12-27 04:08:59.830030',NULL,191,NULL),(112,'commande_prete','Page forêt tendre énergie plaine.','Sauter compagnie casser honneur briller revenir détacher. Âme rompre permettre heureux ouvrage rouler. Cour prévenir monter.','{}',1,NULL,'2025-12-27 04:08:59.830445',NULL,167,NULL),(113,'commande_confirmee','Espérer faible.','Colline enfermer figure sauver goût rencontre âgé. Humide vendre question naturellement bas médecin me refuser.','{}',0,NULL,'2025-12-27 04:08:59.830860',NULL,195,NULL),(114,'commande_confirmee','Plaire prévoir contenter conversation.','Rêver avant avouer charge. Retomber chaleur briller tout sol compte.\nEau accorder as extraordinaire empêcher exécuter. Avouer bras désirer rouge apparence.','{}',0,NULL,'2025-12-27 04:08:59.831327',NULL,196,NULL),(115,'rendez_vous_rappel','Calme neuf recueillir.','Distance parfois direction étudier autour prison eau. Présence calme pour descendre éteindre fer.','{}',0,NULL,'2025-12-27 04:08:59.831727',NULL,205,NULL),(116,'commande_prete','Secret croix retirer quelqu\'un.','Semaine former hésiter tracer soldat annoncer leur. Plus aussi impossible journal tourner. Sien détacher d\'autres couche.','{}',0,NULL,'2025-12-27 04:08:59.832117',NULL,223,NULL),(117,'commande_confirmee','Prétendre an.','Exister nation remplir drame siècle vingt cou. Accuser condamner grave nombre secours quatre durant discuter. Temps vous lendemain droite d\'autres trou.','{}',1,NULL,'2025-12-27 04:08:59.832498',NULL,191,NULL),(118,'commande_confirmee','Accorder nu cinq.','Son travailler vide même. Fait demeurer enfance religion meilleur rassurer.\nEnlever saint depuis saison respect jouer interrompre. Satisfaire sept mettre succès arracher plan.\nBureau rare plusieurs.','{}',1,NULL,'2025-12-27 04:08:59.832989',NULL,213,NULL),(119,'rendez_vous_confirme','Mériter beau après boire rond.','Agiter ensuite larme soleil. Enfin veiller fait rare scène champ. Sable événement écouter sujet attitude chez véritable.','{}',1,NULL,'2025-12-27 04:08:59.833525',NULL,185,NULL),(120,'commande_prete','Banc complet dehors.','Nu réel verre. Cependant déclarer portier poste toit avec plus politique. Combat front flamme fort après journée.','{}',0,NULL,'2025-12-27 04:08:59.833925',NULL,202,NULL),(121,'consultation_rapport','Mur lourd haut prévenir.','Ailleurs résister rapidement lettre armée. Séparer de espèce.\nTel pourtant ceci abattre convenir fond abandonner. Embrasser quinze tromper monde étude lier.','{}',0,NULL,'2025-12-27 04:08:59.834448',NULL,215,NULL),(122,'rendez_vous_nouveau','Glisser montrer difficile.','Danser boire moins entre. Âgé approcher herbe depuis situation rêve. Abri gens loi argent plus soirée remplacer céder.','{}',1,NULL,'2025-12-27 04:08:59.836251',NULL,163,NULL),(123,'consultation_rapport','Danser salut droite inspirer.','Ressembler remercier rang signifier. Désormais animer dans éteindre pas long action charge. Plonger avoir soi.\nCraindre suivre juge colline. Éteindre pain haine. Appeler tenter profond ressembler.','{}',0,NULL,'2025-12-27 04:08:59.837337',NULL,220,NULL),(124,'rendez_vous_nouveau','Succès permettre rouler.','Mal résoudre dehors. Fond révolution appartement coup certain.\nMoindre saint geste avant confier ajouter.\nSigner quelque doux âme lequel tel.','{}',1,NULL,'2025-12-27 04:08:59.839074',NULL,195,NULL),(125,'commande_confirmee','Fermer encore preuve habiter.','Palais recommencer beau présent exister fidèle souffrance. Livre vite fils sueur. Rouler saint franchir bataille auprès dent expérience.','{}',1,NULL,'2025-12-27 04:08:59.840193',NULL,204,NULL),(126,'rendez_vous_confirme','Quand changer transformer signifier.','Science midi contenter. Avance chaîne rester passer. Installer même supporter nuit.\nAnglais course besoin. Aider réduire réduire proposer. Désirer fidèle déchirer pitié.','{}',0,NULL,'2025-12-27 04:08:59.841593',NULL,164,NULL),(127,'rendez_vous_confirme','Malade chercher.','Transformer agir discussion. Large cher avant après. Campagne ci vie voiture personnage.\nVers garçon naissance instinct pièce. Clair possible fauteuil pendant obtenir.','{}',0,NULL,'2025-12-27 04:08:59.842526',NULL,181,NULL),(128,'rendez_vous_nouveau','Tourner remarquer demander.','Étroit gauche militaire confondre professeur seuil. Impossible fonder mort sentier. Vol jaune habitant face.','{}',0,NULL,'2025-12-27 04:08:59.843230',NULL,164,NULL),(129,'rendez_vous_rappel','Honneur leur beau colon.','Aussitôt souhaiter bout abandonner. Étendre discuter tromper.\nSavoir prêt allumer rire courage françois encore me. Garder retirer dernier porter. Large règle pouvoir heure or.','{}',1,NULL,'2025-12-27 04:08:59.844027',NULL,199,NULL),(130,'rendez_vous_nouveau','Même auteur.','Empire présence inconnu depuis membre. Combien faible défendre mener. Dieu diriger reprendre plan paysan. Aussi voile vague trembler défaut ramasser.','{}',1,NULL,'2025-12-27 04:08:59.844851',NULL,164,NULL),(131,'consultation_rapport','Autant rue.','Animer trois complet chemin liberté fait. Fuir nature inspirer revenir. Chasser mur gens principe.','{}',1,NULL,'2025-12-27 04:08:59.845404',NULL,190,NULL),(132,'commande_confirmee','Secrétaire prévoir.','Plaisir blanc six un mentir facile fier également. Venir cuisine sentiment. Renverser terreur terrible voyage eh manier salle. Feu faim avec absolu céder vague ici joli.','{}',1,NULL,'2025-12-27 04:08:59.846625',NULL,179,NULL),(133,'rendez_vous_nouveau','Soudain parler chanter emporter malgré.','Raconter machine épaule foule faire. Son conscience printemps cinq.','{}',1,NULL,'2025-12-27 04:08:59.847193',NULL,218,NULL),(134,'consultation_rapport','Placer fermer terre demi.','Vivre cercle falloir. Effort cri honneur mine compter comment heure. Haïr vert puis certes employer secret. Officier saison aspect couler choix.','{}',0,NULL,'2025-12-27 04:08:59.847723',NULL,163,NULL),(135,'commande_prete','Détruire fond étaler étage portier.','Intérieur terminer clair principe profiter. Te danger emmener en distinguer auteur pour.\nRassurer casser descendre banc. As montrer aucun clef fille. Projet rompre marche possible pensée.','{}',1,NULL,'2025-12-27 04:08:59.848213',NULL,211,NULL),(136,'consultation_rapport','Même oublier transformer.','Rond coin fort changement pointe absence porter. Bas mémoire cher vêtement entretenir arme ouvert.\nAvoir tranquille voile répondre ouvrage. Prix espérer projet compagnon.','{}',1,NULL,'2025-12-27 04:08:59.849423',NULL,212,NULL),(137,'consultation_rapport','Mer enfant front calme.','L\'Un sein musique dieu accepter rester créer connaissance. Animal mort papa lit bataille nombre penser. Désert encore entre du fortune fil créer colline.','{}',1,NULL,'2025-12-27 04:08:59.850180',NULL,189,NULL),(138,'rendez_vous_rappel','Élever immobile pointe longtemps sorte.','Garçon achever ignorer même arracher embrasser. Foule bureau quelque éteindre recommencer réveiller. Pas montrer risquer saison rouge élever étouffer déclarer.','{}',0,NULL,'2025-12-27 04:08:59.850793',NULL,193,NULL),(139,'commande_prete','Achever aide monde trente.','Soir commencer contenter commander mien françois. Nommer verre vieux bon être achever. Aventure affirmer anglais croire ensuite rire.','{}',0,NULL,'2025-12-27 04:08:59.851377',NULL,214,NULL),(140,'rendez_vous_confirme','Cesser pourquoi midi danger.','Distinguer et donner puis jambe problème. Chien battre pont un près frapper. Argent personne accent remplir.','{}',1,NULL,'2025-12-27 04:08:59.851885',NULL,163,NULL),(141,'commande_prete','Droite y passer affaire.','Bord prêt attaquer rare fine cabinet champ front. Étrange bête pied exprimer larme aussi.','{}',1,NULL,'2025-12-27 04:08:59.853084',NULL,219,NULL),(142,'rendez_vous_confirme','Poitrine le autre ombre séparer.','Présence servir folie offrir danger. Extraordinaire aussitôt goût raconter clair train savoir.\nBras miser or prince. Riche danser son mémoire inconnu. Tenir monter fort temps.','{}',1,NULL,'2025-12-27 04:08:59.854585',NULL,217,NULL),(143,'rendez_vous_rappel','Fil partager envie mémoire parler.','Officier tu mener pourquoi mériter être. Dès fatigue rapide baisser qualité drôle fou.\nChaîne pièce colline salle près prévenir haut. Voler remplacer un résoudre emporter regard.','{}',0,NULL,'2025-12-27 04:08:59.855553',NULL,226,NULL),(144,'commande_confirmee','Empêcher flamme.','Même dire voilà porte froid chute armée. Eau verre presser unique hôtel former. Lever garder avant remettre importance voisin.\nLier famille sauver faible moins écarter creuser.','{}',1,NULL,'2025-12-27 04:08:59.856150',NULL,181,NULL),(145,'rendez_vous_rappel','Satisfaire refuser cher.','Réfléchir peau certes troubler ministre répondre tu ni. Âme simplement figure double veille fuir.','{}',1,NULL,'2025-12-27 04:08:59.856821',NULL,158,NULL),(146,'consultation_rapport','Billet centre un.','Sortir parole titre pain expérience. Tracer sommeil rôle aider lorsque amuser leur.','{}',1,NULL,'2025-12-27 04:08:59.857763',NULL,182,NULL),(147,'commande_prete','Là ajouter.','Depuis semaine essuyer obtenir tapis. Calme peau abattre être. Aller passer vérité précipiter drôle français résoudre.\nEmpêcher accompagner mensonge unique assurer.','{}',1,NULL,'2025-12-27 04:08:59.858476',NULL,168,NULL),(148,'consultation_rapport','Empire arrière.','Vert regretter question déclarer extraordinaire. Centre lisser voiture tantôt.\nExpliquer calme doucement écrire.','{}',0,NULL,'2025-12-27 04:08:59.858960',NULL,166,NULL),(149,'rendez_vous_nouveau','Public article habiller droite.','Désir eaux tout marier air aucun crainte commander. Raison autorité exiger devoir qui pierre assister. Revoir devant retour paraître.','{}',0,NULL,'2025-12-27 04:08:59.859369',NULL,227,NULL),(150,'commande_confirmee','Nord davantage chute après.','Secret témoin terme blanc.\nConscience hôtel diriger ici conscience. Trembler certain froid quelqu\'un et.','{}',1,NULL,'2025-12-27 04:08:59.859984',NULL,161,NULL),(151,'commande_confirmee','Commande confirmée','Votre commande a été confirmée ! Nous commençons la préparation immédiatement.','{\"pharmacie_nom\": \"Pharmacie Centrale\", \"nouveau_statut\": \"confirmee\", \"statut_precedent\": \"en_attente\", \"message_pharmacien\": \"Votre commande a été confirmée ! Nous commençons la préparation immédiatement.\"}',0,NULL,'2026-01-06 02:02:29.978953',63,225,NULL),(232,'autre','Registre créé','Nouveau patient créé automatiquement: Test Patient','{\"registre_id\": 1, \"patient_cree\": true}',0,NULL,'2026-01-21 20:03:46.252885',NULL,157,NULL),(233,'autre','Registre créé','Patient existant lié au registre: Test Patient','{\"registre_id\": 2, \"patient_cree\": false}',1,'2026-01-22 21:52:23.147013','2026-01-21 20:04:10.451002',NULL,157,NULL),(234,'autre','Registre créé','Patient existant lié au registre: Diallo Aminata','{\"registre_id\": 3, \"patient_cree\": false}',1,'2026-01-22 21:52:14.859255','2026-01-21 20:05:14.428952',NULL,157,NULL),(235,'autre','Ordonnance créée','Ordonnance ORD202601229515 créée pour Test Patient','{\"ordonnance_id\": 3}',0,NULL,'2026-01-22 22:37:20.122326',NULL,157,NULL),(236,'autre','Registre créé','Nouveau patient créé automatiquement: Kouma Mamadou','{\"registre_id\": 4, \"patient_cree\": true}',0,NULL,'2026-01-24 19:34:52.086500',NULL,157,NULL),(237,'autre','Registre créé','Nouveau patient créé automatiquement: Dembele Arouna','{\"registre_id\": 5, \"patient_cree\": true}',0,NULL,'2026-01-24 20:17:25.077893',NULL,157,NULL),(238,'autre','Ordonnance créée','Ordonnance ORD202601242829 créée pour Dembele Arouna','{\"ordonnance_id\": 4}',1,'2026-01-27 01:18:53.238845','2026-01-24 20:21:41.751924',NULL,157,NULL),(239,'autre','Registre créé','Nouveau patient créé automatiquement: Doumbia Ousmane','{\"registre_id\": 6, \"patient_cree\": true}',0,NULL,'2026-01-27 21:30:47.312565',NULL,157,NULL),(240,'autre','Ordonnance créée','Ordonnance ORD202601272797 créée pour Doumbia Ousmane','{\"ordonnance_id\": 5}',0,NULL,'2026-01-27 21:36:43.178545',NULL,157,NULL),(241,'autre','Registre créé','Nouveau patient créé automatiquement: Kouma Mamadou','{\"registre_id\": 7, \"patient_cree\": true}',0,NULL,'2026-02-01 05:33:59.540221',NULL,168,NULL),(242,'autre','Ordonnance créée','Ordonnance ORD202602015316 créée pour Kouma Mamadou','{\"ordonnance_id\": 6}',0,NULL,'2026-02-01 05:37:33.404937',NULL,168,NULL),(243,'autre','Ordonnance créée','Ordonnance ORD202602021972 créée pour Doumbia Ousmane','{\"ordonnance_id\": 7}',0,NULL,'2026-02-02 22:45:04.458619',NULL,157,NULL),(244,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.728849',NULL,169,NULL),(245,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.736063',NULL,169,NULL),(246,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-14 00:49:04.735654','2026-02-03 04:22:54.737699',NULL,169,NULL),(247,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',1,'2026-02-14 00:49:02.098710','2026-02-03 04:22:54.740125',NULL,169,NULL),(248,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.745882',NULL,170,NULL),(249,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.748041',NULL,170,NULL),(250,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.749323','2026-02-03 04:22:54.749409',NULL,170,NULL),(251,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.750351',NULL,170,NULL),(252,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.755046',NULL,171,NULL),(253,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.756567',NULL,171,NULL),(254,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.757520','2026-02-03 04:22:54.757587',NULL,171,NULL),(255,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.758651',NULL,171,NULL),(256,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.759848',NULL,172,NULL),(257,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.766354',NULL,172,NULL),(258,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.770388','2026-02-03 04:22:54.770467',NULL,172,NULL),(259,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.784403',NULL,172,NULL),(260,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.787707',NULL,173,NULL),(261,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.789237',NULL,173,NULL),(262,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.789965','2026-02-03 04:22:54.790027',NULL,173,NULL),(263,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.793854',NULL,173,NULL),(264,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.794748',NULL,229,NULL),(265,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.795730',NULL,229,NULL),(266,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.798252','2026-02-03 04:22:54.798311',NULL,229,NULL),(267,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.800392',NULL,229,NULL),(268,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.801324',NULL,230,NULL),(269,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.803563',NULL,230,NULL),(270,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.804560','2026-02-03 04:22:54.804622',NULL,230,NULL),(271,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.805740',NULL,230,NULL),(272,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.806499',NULL,231,NULL),(273,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.811267',NULL,231,NULL),(274,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.812359','2026-02-03 04:22:54.812417',NULL,231,NULL),(275,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.813762',NULL,231,NULL),(276,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.814680',NULL,232,NULL),(277,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.818760',NULL,232,NULL),(278,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.822625','2026-02-03 04:22:54.822769',NULL,232,NULL),(279,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.824240',NULL,232,NULL),(280,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.827238',NULL,233,NULL),(281,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.828605',NULL,233,NULL),(282,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.830031','2026-02-03 04:22:54.830098',NULL,233,NULL),(283,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.869551',NULL,233,NULL),(284,'commande_confirmee','[TEST] Nouvelle commande confirmée','Une commande a été confirmée et nécessite votre attention. Veuillez préparer les produits demandés.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:22:54.898188',NULL,234,NULL),(285,'stock_alerte','[TEST] Alerte stock faible','Le stock de Paracétamol 500mg est en dessous du seuil d\'alerte (5 unités restantes). Veuillez réapprovisionner rapidement.','{\"test\": true, \"produit\": \"Paracétamol 500mg\", \"stock_restant\": 5}',0,NULL,'2026-02-03 04:22:54.900329',NULL,234,NULL),(286,'commande_prete','[TEST] Commande prête pour récupération','La commande CMD123456 est prête et peut être récupérée par le patient.','{\"test\": true, \"commande_numero\": \"CMD123456\"}',1,'2026-02-03 02:22:54.901306','2026-02-03 04:22:54.901423',NULL,234,NULL),(287,'autre','[TEST] Mise à jour système','Le système a été mis à jour avec de nouvelles fonctionnalités. Consultez la documentation pour plus d\'informations.','{\"test\": true, \"version\": \"2.1.0\"}',0,NULL,'2026-02-03 04:22:54.902508',NULL,234,NULL),(303,'rendez_vous_confirme','[TEST] Rendez-vous confirmé','Votre rendez-vous avec Dr. Martin le 15 février à 14h30 a été confirmé.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:46:42.569903',NULL,179,NULL),(304,'rendez_vous_rappel','[TEST] Rappel de rendez-vous','Votre rendez-vous avec Dr. Sow est prévu demain à 10h00.','{\"test\": true, \"priority\": \"medium\"}',0,NULL,'2026-02-03 04:46:42.585031',NULL,179,NULL),(305,'commande_prete','[TEST] Commande prête','Votre commande #CMD-2024-001 est prête à être récupérée à la Pharmacie du Centre.','{\"test\": true, \"commande_numero\": \"CMD-2024-001\"}',0,NULL,'2026-02-03 04:46:42.586474',NULL,179,NULL),(306,'consultation_rapport','[TEST] Rapport de consultation disponible','Le rapport de votre consultation du 28 janvier est maintenant disponible.','{\"test\": true}',1,'2026-02-03 02:46:42.588788','2026-02-03 04:46:42.588909',NULL,179,NULL),(307,'autre','[TEST] Mise à jour de l\'application','Une nouvelle version de l\'application e-Sora est disponible avec des améliorations.','{\"test\": true, \"version\": \"2.1.0\"}',1,'2026-02-02 04:46:42.589612','2026-02-03 04:46:42.589749',NULL,179,NULL),(313,'rendez_vous_confirme','[TEST] Rendez-vous confirmé','Votre rendez-vous avec Dr. Martin le 15 février à 14h30 a été confirmé.','{\"test\": true, \"priority\": \"high\"}',0,NULL,'2026-02-03 04:46:42.607959',NULL,181,NULL),(314,'rendez_vous_rappel','[TEST] Rappel de rendez-vous','Votre rendez-vous avec Dr. Sow est prévu demain à 10h00.','{\"test\": true, \"priority\": \"medium\"}',0,NULL,'2026-02-03 04:46:42.611265',NULL,181,NULL),(315,'commande_prete','[TEST] Commande prête','Votre commande #CMD-2024-001 est prête à être récupérée à la Pharmacie du Centre.','{\"test\": true, \"commande_numero\": \"CMD-2024-001\"}',0,NULL,'2026-02-03 04:46:42.612399',NULL,181,NULL),(316,'consultation_rapport','[TEST] Rapport de consultation disponible','Le rapport de votre consultation du 28 janvier est maintenant disponible.','{\"test\": true}',1,'2026-02-03 02:46:42.612924','2026-02-03 04:46:42.612997',NULL,181,NULL),(317,'autre','[TEST] Mise à jour de l\'application','Une nouvelle version de l\'application e-Sora est disponible avec des améliorations.','{\"test\": true, \"version\": \"2.1.0\"}',1,'2026-02-02 04:46:42.618797','2026-02-03 04:46:42.618911',NULL,181,NULL),(318,'rendez_vous_confirme','[TEST] Rendez-vous confirmé avec Dr. Martin','Votre rendez-vous avec Dr. Martin le 15 février à 14h30 a été confirmé. Merci de vous présenter 15 minutes avant l\'heure.','{\"test\": true, \"doctor\": \"Dr. Martin\", \"priority\": \"high\"}',0,NULL,'2026-02-03 04:53:14.218556',NULL,180,NULL),(319,'rendez_vous_rappel','[TEST] Rappel: Rendez-vous demain','N\'oubliez pas votre rendez-vous avec Dr. Sow demain à 10h00 au service de cardiologie.','{\"test\": true, \"doctor\": \"Dr. Sow\", \"priority\": \"medium\"}',1,'2026-02-03 04:59:56.176576','2026-02-03 04:53:14.231515',NULL,180,NULL),(320,'commande_prete','[TEST] Votre commande est prête','Votre commande #CMD-2024-001 est prête à être récupérée à la Pharmacie du Centre. Horaires: 8h-18h.','{\"test\": true, \"pharmacie\": \"Pharmacie du Centre\", \"commande_numero\": \"CMD-2024-001\"}',0,NULL,'2026-02-03 04:53:14.237437',NULL,180,NULL),(321,'consultation_rapport','[TEST] Rapport de consultation disponible','Le rapport de votre consultation du 28 janvier avec Dr. Diallo est maintenant disponible dans votre dossier médical.','{\"test\": true, \"doctor\": \"Dr. Diallo\", \"date_consultation\": \"2024-01-28\"}',1,'2026-02-03 02:53:14.217824','2026-02-03 04:53:14.240316',NULL,180,NULL),(322,'autre','[TEST] Mise à jour importante','Une nouvelle version de l\'application e-Sora est disponible avec des améliorations de sécurité et de nouvelles fonctionnalités.','{\"test\": true, \"type\": \"security_update\", \"version\": \"2.1.0\"}',1,'2026-02-02 04:53:14.218288','2026-02-03 04:53:14.242444',NULL,180,NULL),(323,'autre','Ordonnance créée','Ordonnance ORD202602039521 créée pour Doumbia Ousmane','{\"ordonnance_id\": 8}',0,NULL,'2026-02-03 18:11:26.377588',NULL,157,NULL),(324,'autre','Ordonnance créée','Ordonnance ORD202602052557 créée pour Doumbia Ousmane','{\"ordonnance_id\": 9}',0,NULL,'2026-02-05 20:23:10.847375',NULL,157,NULL);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordonnances`
--

DROP TABLE IF EXISTS `ordonnances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordonnances` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_ordonnance` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patient_nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patient_prenom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `patient_age` int NOT NULL,
  `patient_sexe` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `diagnostic` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `observations` longtext COLLATE utf8mb4_unicode_ci,
  `recommandations` longtext COLLATE utf8mb4_unicode_ci,
  `statut` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_prescription` datetime(6) NOT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_delivrance` datetime(6) DEFAULT NULL,
  `duree_validite_jours` int NOT NULL,
  `date_expiration` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `hopital_id` bigint NOT NULL,
  `pharmacie_delivrance_id` bigint DEFAULT NULL,
  `registre_id` bigint NOT NULL,
  `specialiste_id` bigint NOT NULL,
  `qr_code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `qr_code_url` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_ordonnance` (`numero_ordonnance`),
  KEY `ordonnances_numero__38138c_idx` (`numero_ordonnance`),
  KEY `ordonnances_registr_cfed96_idx` (`registre_id`),
  KEY `ordonnances_special_6030c3_idx` (`specialiste_id`,`date_prescription`),
  KEY `ordonnances_statut_cea8e9_idx` (`statut`),
  KEY `ordonnances_date_ex_19762e_idx` (`date_expiration`),
  KEY `ordonnances_hopital_id_15b640ca_fk_hopitaux_id` (`hopital_id`),
  KEY `ordonnances_pharmacie_delivrance_id_806adf46_fk_pharmacies_id` (`pharmacie_delivrance_id`),
  CONSTRAINT `ordonnances_hopital_id_15b640ca_fk_hopitaux_id` FOREIGN KEY (`hopital_id`) REFERENCES `hopitaux` (`id`),
  CONSTRAINT `ordonnances_pharmacie_delivrance_id_806adf46_fk_pharmacies_id` FOREIGN KEY (`pharmacie_delivrance_id`) REFERENCES `pharmacies` (`id`),
  CONSTRAINT `ordonnances_registre_id_e1c12774_fk_registres_id` FOREIGN KEY (`registre_id`) REFERENCES `registres` (`id`),
  CONSTRAINT `ordonnances_specialiste_id_7c1aff74_fk_specialistes_id` FOREIGN KEY (`specialiste_id`) REFERENCES `specialistes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordonnances`
--

LOCK TABLES `ordonnances` WRITE;
/*!40000 ALTER TABLE `ordonnances` DISABLE KEYS */;
INSERT INTO `ordonnances` VALUES (1,'ORD202601228979','Test','Patient',30,'M','Test diagnostic','Test observations',NULL,'validee','2026-01-22 22:29:59.418334','2026-01-22 22:34:12.852114',NULL,30,'2026-02-21','2026-01-22 22:29:59.418725','2026-01-22 22:34:12.855833',9,NULL,3,25,'ordonnances/qr_codes/qr_ordonnance_ORD202601228979.png','http://localhost:8000/api/ordonnances/1/pdf/'),(2,'ORD202601226840','Test','Patient',30,'M','Test diagnostic','Test observations',NULL,'validee','2026-01-22 22:30:19.288158','2026-01-22 22:30:30.125946',NULL,30,'2026-02-21','2026-01-22 22:30:19.288515','2026-01-22 22:30:30.134735',9,NULL,3,25,'ordonnances/qr_codes/qr_ordonnance_ORD202601226840_drXDbae.png','http://localhost:8000/api/ordonnances/2/pdf/'),(3,'ORD202601229515','Test','Patient',30,'M','Test diagnostic via API','Test observations via API',NULL,'validee','2026-01-22 22:37:20.017591','2026-01-22 22:37:47.517947',NULL,30,'2026-02-21','2026-01-22 22:37:20.018391','2026-01-22 22:37:47.521778',9,NULL,3,25,'ordonnances/qr_codes/qr_ordonnance_ORD202601229515_nyjTkGr.png','http://localhost:8000/api/ordonnances/3/pdf/'),(4,'ORD202601242829','Dembele','Arouna',30,'M','paludisme',NULL,NULL,'validee','2026-01-24 20:21:41.727918','2026-01-24 20:22:02.921107',NULL,30,'2026-02-23','2026-01-24 20:21:41.728048','2026-01-24 20:22:02.924146',9,NULL,5,25,'',NULL),(5,'ORD202601272797','Doumbia','Ousmane',30,'M','lol',NULL,NULL,'validee','2026-01-27 21:36:43.148692','2026-01-27 21:37:08.591175',NULL,30,'2026-02-26','2026-01-27 21:36:43.148830','2026-01-27 21:37:08.592391',9,NULL,6,25,'',NULL),(6,'ORD202602015316','Kouma','Mamadou',20,'M','Paludismes',NULL,NULL,'validee','2026-02-01 05:37:33.391116','2026-02-01 05:38:03.136713',NULL,30,'2026-03-03','2026-02-01 05:37:33.391513','2026-02-01 05:38:03.140049',7,NULL,7,36,'',NULL),(7,'ORD202602021972','Doumbia','Ousmane',30,'M','Infection',NULL,NULL,'validee','2026-02-02 22:45:04.405350','2026-02-02 22:45:38.293150',NULL,30,'2026-03-04','2026-02-02 22:45:04.406799','2026-02-02 22:45:38.305597',9,NULL,6,25,'ordonnances/qr_codes/qr_ordonnance_ORD202602021972.png','http://localhost:8000/api/ordonnances/7/pdf/'),(8,'ORD202602039521','Doumbia','Ousmane',30,'M','lol',NULL,NULL,'validee','2026-02-03 18:11:26.344859','2026-02-03 18:12:35.582822',NULL,30,'2026-03-05','2026-02-03 18:11:26.345145','2026-02-03 18:12:35.598116',9,NULL,6,25,'ordonnances/qr_codes/qr_ordonnance_ORD202602039521.png','http://localhost:8001/api/ordonnances/8/pdf/'),(9,'ORD202602052557','Doumbia','Ousmane',30,'M','loo',NULL,NULL,'brouillon','2026-02-05 20:23:10.776084',NULL,NULL,30,NULL,'2026-02-05 20:23:10.777091','2026-02-05 20:23:10.777113',9,NULL,6,25,'',NULL);
/*!40000 ALTER TABLE `ordonnances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prenom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dob` date NOT NULL,
  `sexe` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `adresse` longtext COLLATE utf8mb4_unicode_ci,
  `antecedents` longtext COLLATE utf8mb4_unicode_ci,
  `allergies` longtext COLLATE utf8mb4_unicode_ci,
  `ville_actuelle` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `preferences_notification` json NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `ethnie` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lieu_naissance` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_cne` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_cni` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profession` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `numero_cne` (`numero_cne`),
  UNIQUE KEY `numero_cni` (`numero_cni`),
  KEY `patients_nom_d733a3_idx` (`nom`,`prenom`),
  KEY `patients_telepho_9a01bc_idx` (`telephone`),
  KEY `patients_email_bf0efb_idx` (`email`),
  CONSTRAINT `patients_user_id_11c42fa7_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=159 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (101,'Gosselin Test CORS','Colette','1990-03-24','M','+33987654321','lecomtedaniel@example.net','19, chemin de Delannoy\n56495 Bousquet','Asthme','Aucune allergie connue','Thiès','{}','2025-12-27 04:08:59.501706','2026-02-03 01:29:19.916629',179,NULL,NULL,NULL,NULL,NULL),(102,'Gilles','Henriette','1987-05-21','F','+33999888772','margot68@example.net','687, rue Robert Antoine\n67229 Boulay','','Pénicilline','Dakar','{}','2025-12-27 04:08:59.502342','2026-02-03 02:07:29.204926',180,NULL,NULL,NULL,NULL,NULL),(103,'Carlier','Laurent','1996-10-16','F','+221733056507','mauriceribeiro@example.org','avenue Durand\n97632 Techer-sur-Dufour','Diabète type 2','Aspirine','Thiès','{}','2025-12-27 04:08:59.503445','2025-12-27 04:08:59.503450',181,NULL,NULL,NULL,NULL,NULL),(104,'Carpentier','Julien','1988-02-17','M','+221751632438','wdufour@example.org','932, rue Aubry\n07243 Gauthierdan','Hypertension artérielle','Aucune allergie connue','Thiès','{}','2025-12-27 04:08:59.504091','2025-12-27 04:08:59.504095',182,NULL,NULL,NULL,NULL,NULL),(105,'Lefort','Lucie','2003-04-26','F','+221704204813','andre55@example.com','5, avenue Susanne Ramos\n66350 Lacroix','Diabète type 2','Pénicilline','Kaolack','{}','2025-12-27 04:08:59.504548','2025-12-27 04:08:59.504553',183,NULL,NULL,NULL,NULL,NULL),(106,'Bodin','Julie','1977-04-28','F','+221744764563','andresauvage@example.org','71, chemin de Lopez\n12300 Legendre-la-Forêt','Asthme','Aucune allergie connue','Thiès','{}','2025-12-27 04:08:59.504981','2025-12-27 04:08:59.504986',184,NULL,NULL,NULL,NULL,NULL),(107,'Lebon','Marcel','1996-10-18','F','+221707176472','david93@example.net','770, rue Anaïs Raymond\n43648 Seguin-sur-Mercier','Asthme','Pénicilline','Thiès','{}','2025-12-27 04:08:59.505618','2025-12-27 04:08:59.505622',185,NULL,NULL,NULL,NULL,NULL),(108,'Lévêque','Madeleine','1988-08-17','M','+221795960341','georges24@example.com','23, avenue Dupré\n71400 Ferreira','Diabète type 2','Pénicilline','Kaolack','{}','2025-12-27 04:08:59.506049','2025-12-27 04:08:59.506053',186,NULL,NULL,NULL,NULL,NULL),(109,'Potier','Martin','2008-02-08','F','+221718865550','drocher@example.com','avenue Marthe Courtois\n20928 Berthelot','Asthme','Aspirine','Ziguinchor','{}','2025-12-27 04:08:59.506475','2025-12-27 04:08:59.506480',187,NULL,NULL,NULL,NULL,NULL),(110,'Guillot','Louise','2007-07-17','F','+221731028459','margaud21@example.com','71, avenue Rémy Pires\n70141 GalletVille','Diabète type 2','Pénicilline','Thiès','{}','2025-12-27 04:08:59.507217','2025-12-27 04:08:59.507223',188,NULL,NULL,NULL,NULL,NULL),(111,'Charles','Susanne','2007-09-22','F','+221787672501','marthe63@example.net','chemin Tristan Petit\n73963 Sainte RenéBourg','Asthme','','Thiès','{}','2025-12-27 04:08:59.511043','2025-12-27 04:08:59.511048',189,NULL,NULL,NULL,NULL,NULL),(112,'Étienne','Lucy','1977-11-26','M','+221781188323','bertrand94@example.com','avenue Tristan Goncalves\n81975 Besnard','Diabète type 2','Aucune allergie connue','Kaolack','{}','2025-12-27 04:08:59.511470','2025-12-27 04:08:59.511475',190,NULL,NULL,NULL,NULL,NULL),(113,'Bourdon','Théophile','1986-03-24','M','+221765147454','duhamelsophie@example.net','98, boulevard Bouchet\n93564 Girarddan','Diabète type 2','Pénicilline','Thiès','{}','2025-12-27 04:08:59.512874','2025-12-27 04:08:59.512880',191,NULL,NULL,NULL,NULL,NULL),(114,'Aubert','Marie','2001-12-20','M','+221719259781','luc33@example.org','778, avenue de Langlois\n67772 Rossi','Aucun antécédent particulier','Aspirine','Saint-Louis','{}','2025-12-27 04:08:59.513929','2025-12-27 04:08:59.513933',192,NULL,NULL,NULL,NULL,NULL),(115,'Leblanc','Bertrand','2003-05-14','M','+221761688313','pmartin@example.net','98, rue Jean\n84972 Sainte Jacques-les-Bains','Hypertension artérielle','','Saint-Louis','{}','2025-12-27 04:08:59.514636','2025-12-27 04:08:59.514641',193,NULL,NULL,NULL,NULL,NULL),(116,'Toussaint','Valentine','2004-02-08','M','+221775979991','aimeeguerin@example.net','90, avenue Paul Dias\n93521 Michel','Diabète type 2','','Ziguinchor','{}','2025-12-27 04:08:59.515468','2025-12-27 04:08:59.515474',194,NULL,NULL,NULL,NULL,NULL),(117,'Denis','Alexandre','1993-01-12','M','+221731735066','thereselemonnier@example.net','16, avenue Poirier\n61588 Paris','','Pénicilline','Kaolack','{}','2025-12-27 04:08:59.516287','2025-12-27 04:08:59.516292',195,NULL,NULL,NULL,NULL,NULL),(118,'Roche','Thibault','1999-02-28','F','+221744849283','dominiquemunoz@example.net','avenue Perrier\n36557 Munoz','Hypertension artérielle','Aspirine','Kaolack','{}','2025-12-27 04:08:59.517617','2025-12-27 04:08:59.517622',196,NULL,NULL,NULL,NULL,NULL),(119,'Robert','David','1995-10-08','M','+221731194971','aimeevincent@example.org','751, chemin Alves\n54850 Dijoux','Diabète type 2','','Ziguinchor','{}','2025-12-27 04:08:59.518657','2025-12-27 04:08:59.518662',197,NULL,NULL,NULL,NULL,NULL),(120,'Bouvet','David','1995-02-11','M','+221716810016','charlesdiane@example.net','chemin Picard\n88868 Saint Valentine','Asthme','Pénicilline','Kaolack','{}','2025-12-27 04:08:59.519928','2025-12-27 04:08:59.519932',198,NULL,NULL,NULL,NULL,NULL),(121,'Marchal','Constance','1999-10-09','F','+221738478674','suzanneduhamel@example.net','391, boulevard de Bazin\n53990 Picard-les-Bains','','Fruits de mer','Thiès','{}','2025-12-27 04:08:59.520534','2025-12-27 04:08:59.520539',199,NULL,NULL,NULL,NULL,NULL),(122,'Hubert','Alexandria','1975-11-25','M','+221782926400','adrienne07@example.com','avenue Guillet\n04307 Cordierboeuf','Aucun antécédent particulier','Fruits de mer','Dakar','{}','2025-12-27 04:08:59.521876','2025-12-27 04:08:59.521881',200,NULL,NULL,NULL,NULL,NULL),(123,'Lambert','Georges','1990-04-01','F','+221759230624','martinedijoux@example.net','avenue de Descamps\n72947 Morel-sur-Martineau','Asthme','Aucune allergie connue','Kaolack','{}','2025-12-27 04:08:59.522666','2025-12-27 04:08:59.522670',201,NULL,NULL,NULL,NULL,NULL),(124,'Descamps','Julien','2007-09-29','F','+221786046910','williamchretien@example.org','21, rue de Gérard\n97190 Picard-sur-Mer','Asthme','','Dakar','{}','2025-12-27 04:08:59.523518','2025-12-27 04:08:59.523547',202,NULL,NULL,NULL,NULL,NULL),(125,'Morvan','Louise','1999-03-24','M','+221725153468','frederic21@example.org','42, avenue de Rémy\n66212 Peltier-sur-Mer','Asthme','Aucune allergie connue','Ziguinchor','{}','2025-12-27 04:08:59.524604','2025-12-27 04:08:59.524615',203,NULL,NULL,NULL,NULL,NULL),(126,'Cordier','Margot','1995-04-02','F','+221767037089','danielstephanie@example.net','rue de Alves\n02501 De SousaBourg','Asthme','Fruits de mer','Dakar','{}','2025-12-27 04:08:59.525594','2025-12-27 04:08:59.525603',204,NULL,NULL,NULL,NULL,NULL),(127,'Pierre','Odette','1994-07-17','F','+221745723567','julien85@example.net','622, chemin de Dupré\n79494 Michel-sur-Breton','Hypertension artérielle','Pénicilline','Ziguinchor','{}','2025-12-27 04:08:59.526135','2025-12-27 04:08:59.526140',205,NULL,NULL,NULL,NULL,NULL),(128,'Cordier','Henriette','1989-03-16','M','+221758762842','martinezalfred@example.org','49, rue Bonneau\n23941 Saint Luciedan','Diabète type 2','Pénicilline','Kaolack','{}','2025-12-27 04:08:59.526619','2025-12-27 04:08:59.526624',206,NULL,NULL,NULL,NULL,NULL),(129,'Martel','Xavier','1987-11-20','M','+221788919638','perriercharles@example.org','8, boulevard Vallet\n63204 Maury-sur-Guillet','Hypertension artérielle','Aspirine','Thiès','{}','2025-12-27 04:08:59.527278','2025-12-27 04:08:59.527282',207,NULL,NULL,NULL,NULL,NULL),(130,'Bonneau','Philippe','1978-05-17','M','+221786423138','charrierlucas@example.net','91, chemin Ferreira\n76309 Riou','Aucun antécédent particulier','Aucune allergie connue','Ziguinchor','{}','2025-12-27 04:08:59.527936','2025-12-27 04:08:59.527942',208,NULL,NULL,NULL,NULL,NULL),(131,'Perrin','Robert','1989-01-11','M','+221799564996','paulette55@example.com','20, boulevard de Michel\n78732 Martel','Aucun antécédent particulier','Pénicilline','Thiès','{}','2025-12-27 04:08:59.528412','2025-12-27 04:08:59.528417',209,NULL,NULL,NULL,NULL,NULL),(132,'Traore','Raymond','1984-10-30','F','+221750392335','fouchergabrielle@example.org','95, boulevard Chauvin\n40441 Sainte Sophie','','Fruits de mer','Saint-Louis','{}','2025-12-27 04:08:59.528864','2025-12-27 04:08:59.528868',210,NULL,NULL,NULL,NULL,NULL),(133,'Charrier','Valentine','1994-07-27','M','+221742828865','honore83@example.com','rue de Pires\n20906 Perrotboeuf','Diabète type 2','','Thiès','{}','2025-12-27 04:08:59.529444','2025-12-27 04:08:59.529449',211,NULL,NULL,NULL,NULL,NULL),(134,'Mace','Lorraine','1986-02-11','F','+221722023075','hubertfrancoise@example.net','81, chemin Perret\n02480 Lemaire','Diabète type 2','Aspirine','Dakar','{}','2025-12-27 04:08:59.530049','2025-12-27 04:08:59.530056',212,NULL,NULL,NULL,NULL,NULL),(135,'Roy','Martine','1975-09-16','M','+221727405703','vlejeune@example.org','546, avenue Chevallier\n23317 Payet-la-Forêt','Diabète type 2','Pénicilline','Ziguinchor','{}','2025-12-27 04:08:59.530687','2025-12-27 04:08:59.530693',213,NULL,NULL,NULL,NULL,NULL),(136,'Diallo','Georges','1986-01-26','F','+221746080978','francois97@example.org','chemin de Langlois\n79690 Monnier','Asthme','Fruits de mer','Thiès','{}','2025-12-27 04:08:59.531173','2025-12-27 04:08:59.531177',214,NULL,NULL,NULL,NULL,NULL),(137,'Giraud','Thierry','1990-01-12','F','+221776164672','remydelahaye@example.com','30, avenue Lemaître\n97244 Martinez','','','Saint-Louis','{}','2025-12-27 04:08:59.531983','2025-12-27 04:08:59.531987',215,NULL,NULL,NULL,NULL,NULL),(138,'Lejeune','Patricia','1988-10-31','F','+221710098241','aime24@example.net','854, chemin de Hebert\n56302 Baillyboeuf','Hypertension artérielle','Aspirine','Saint-Louis','{}','2025-12-27 04:08:59.532462','2025-12-27 04:08:59.532466',216,NULL,NULL,NULL,NULL,NULL),(139,'Adam','Dominique','1980-06-28','M','+221758535896','colinclaude@example.com','39, rue de Coste\n04962 Ramosnec','Asthme','Fruits de mer','Dakar','{}','2025-12-27 04:08:59.532872','2025-12-27 04:08:59.532877',217,NULL,NULL,NULL,NULL,NULL),(140,'Lemaître','Véronique','1992-12-24','M','+221787858993','denisejacquet@example.com','75, rue Eugène Imbert\n60273 Courtois','Aucun antécédent particulier','Fruits de mer','Saint-Louis','{}','2025-12-27 04:08:59.533479','2025-12-27 04:08:59.533483',218,NULL,NULL,NULL,NULL,NULL),(141,'Dufour','Denis','1999-03-25','M','+221711379526','dupuypatrick@example.net','58, boulevard de Parent\n21670 Saint Denis','','Aspirine','Dakar','{}','2025-12-27 04:08:59.534030','2025-12-27 04:08:59.534034',219,NULL,NULL,NULL,NULL,NULL),(142,'Simon','Hélène','1983-10-19','F','+221771751972','alexandrietecher@example.com','31, rue Delahaye\n48855 Meyernec','','Pénicilline','Kaolack','{}','2025-12-27 04:08:59.534581','2025-12-27 04:08:59.534586',220,NULL,NULL,NULL,NULL,NULL),(143,'Letellier','Émilie','1986-03-10','F','+221708507221','lcaron@example.net','7, rue Alexandria Valentin\n80444 Verdier-la-Forêt','Asthme','Aucune allergie connue','Saint-Louis','{}','2025-12-27 04:08:59.535216','2025-12-27 04:08:59.535223',221,NULL,NULL,NULL,NULL,NULL),(144,'Cohen','Laurent','1980-07-13','F','+221750491021','josephine36@example.net','48, boulevard Susanne Fabre\n24943 Pelletier-sur-Cousin','Aucun antécédent particulier','Aspirine','Thiès','{}','2025-12-27 04:08:59.536155','2025-12-27 04:08:59.536160',222,NULL,NULL,NULL,NULL,NULL),(145,'Raynaud','Roger','1978-11-29','F','+221784786347','cordiergilles@example.org','5, avenue de Maillard\n85283 Marquesdan','Aucun antécédent particulier','Aspirine','Saint-Louis','{}','2025-12-27 04:08:59.536629','2025-12-27 04:08:59.536634',223,NULL,NULL,NULL,NULL,NULL),(146,'Roche','Guy','1989-05-16','F','+221711414941','josephinelefevre@example.org','74, chemin Christine Boyer\n97359 Voisin','Asthme','Aucune allergie connue','Dakar','{}','2025-12-27 04:08:59.537689','2025-12-27 04:08:59.537694',224,NULL,NULL,NULL,NULL,NULL),(147,'Leroy','Susan','2008-08-11','M','+221749937627','arthur44@example.net','73, chemin François Courtois\n37237 Letelliernec','Diabète type 2','','Ziguinchor','{}','2025-12-27 04:08:59.538355','2025-12-27 04:08:59.538360',225,NULL,NULL,NULL,NULL,NULL),(148,'Étienne','Stéphane','1978-11-25','M','+221766483553','uguillou@example.org','avenue de Ferrand\n55258 Lecomte','Asthme','Fruits de mer','Kaolack','{}','2025-12-27 04:08:59.538964','2025-12-27 04:08:59.538968',226,NULL,NULL,NULL,NULL,NULL),(149,'Lagarde','Julien','1980-02-05','F','+221730003574','ilemoine@example.net','263, boulevard Bourgeois\n37278 Saint Thibault','Hypertension artérielle','Pénicilline','Ziguinchor','{}','2025-12-27 04:08:59.539593','2025-12-27 04:08:59.539598',227,NULL,NULL,NULL,NULL,NULL),(150,'Potier','Thibaut','2005-02-06','M','+221788423099','emilieferreira@example.org','3, boulevard Julie Lombard\n97622 FaureBourg','','Aspirine','Dakar','{}','2025-12-27 04:08:59.540490','2025-12-27 04:08:59.540495',228,NULL,NULL,NULL,NULL,NULL),(151,'Diallo','Aminata','1990-05-15','F','221771234567','aminata.diallo@test.sn','Dakar, Sénégal',NULL,NULL,'Dakar','{}','2026-01-21 20:00:32.676232','2026-01-21 20:00:32.677136',NULL,'Peul',NULL,'CNE987654321','1234567890123','Enseignante'),(152,'Ndiaye','Moussa','1985-08-20','M','221776543210','moussa.ndiaye@test.sn','Thiès, Sénégal',NULL,NULL,'Thiès','{}','2026-01-21 20:02:32.030183','2026-01-21 20:02:32.030412',NULL,'Wolof',NULL,'CNE123456789',NULL,'Médecin'),(153,'Test','Patient','1996-01-21','M','221771234567','test.patient@example.com','Dakar',NULL,NULL,'Dakar','{}','2026-01-21 20:03:46.228560','2026-01-21 20:03:46.228573',NULL,'Wolof',NULL,NULL,'TEST123456789','Ingénieur'),(154,'Kouma','Mamadou','2000-01-24','M','788749980','k.moh9315@gmail.com','Dakar',NULL,NULL,'Dakar','{}','2026-01-24 19:34:52.068326','2026-01-24 19:34:52.068428',NULL,'Sonike',NULL,NULL,'1223389844','Etudiant'),(155,'Dembele','Arouna','1996-01-24','M','73902244','arouna@gmail.com','Bamako',NULL,NULL,'Bamako','{}','2026-01-24 20:17:25.066419','2026-01-24 20:17:25.066450',NULL,'senofo',NULL,NULL,'122334884','Etudiant'),(156,'Doumbia','Ousmane','1996-01-27','M','+223 78 89 40 09','ousmane@gmail.com','Bamako',NULL,NULL,'Bamako','{}','2026-01-27 21:30:47.298274','2026-01-27 21:30:47.298286',NULL,'Nounou',NULL,NULL,'12344245','Financier'),(157,'Kouma','Mamadou','2006-02-01','M','788749980','mamadoukouma@gmail.com','Dakar',NULL,NULL,'Dakar','{}','2026-02-01 05:33:59.527326','2026-02-01 05:33:59.527336',NULL,'Sonike',NULL,NULL,'11233455','Etudiant'),(158,'Test','Patient','1990-01-01','M',NULL,'test@esora.com',NULL,NULL,NULL,'Dakar','{\"reminders\": false}','2026-02-03 23:20:02.729326','2026-02-11 00:06:38.168487',235,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharmacies`
--

DROP TABLE IF EXISTS `pharmacies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharmacies` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `adresse` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `ville` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pays` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `horaires_ouverture` json NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pharmacies_nom_41910f_idx` (`nom`),
  KEY `pharmacies_user_id_d6f13f_idx` (`user_id`),
  KEY `pharmacies_actif_cea67e_idx` (`actif`),
  KEY `pharmacies_ville_b969a0_idx` (`ville`),
  CONSTRAINT `pharmacies_user_id_25af35f2_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharmacies`
--

LOCK TABLES `pharmacies` WRITE;
/*!40000 ALTER TABLE `pharmacies` DISABLE KEYS */;
INSERT INTO `pharmacies` VALUES (11,'Pharmacie Centrale','16, rue de Laroche\n52560 Saint Agathedan','Dakar','Sénégal','+221805573743','contact@pharmaciecentrale.sn',14.692800,-17.446700,'','{\"jeudi\": \"01:00-18:00\", \"lundi\": \"08:00-18:00\", \"mardi\": \"08:00-18:00\", \"samedi\": \"08:00-18:00\", \"dimanche\": \"08:00-18:00\", \"mercredi\": \"08:00-18:00\", \"vendredi\": \"01:00-18:00\"}','',1,'2025-12-27 04:08:59.548496','2026-02-13 20:04:01.857844',169),(12,'Pharmacie du Plateau','46, avenue Frédérique Guillaume\n88585 Robertboeuf','Dakar','Sénégal','+221873233833','contact@pharmacieduplateau.sn',NULL,NULL,'','{}','',1,'2025-12-27 04:08:59.549736','2025-12-27 04:08:59.549742',170),(13,'Pharmacie Médina','24, avenue de Albert\n38550 Rémy-la-Forêt','Dakar','Sénégal','+221857551363','contact@pharmaciemédina.sn',NULL,NULL,'','{}','',1,'2025-12-27 04:08:59.550253','2026-02-10 13:51:05.698644',171),(14,'Pharmacie Thiès Centre','94, chemin Alix Schneider\n91705 Roy','Thiès','Sénégal','+221843245784','contact@pharmaciethièscentre.sn',NULL,NULL,'','{}','',1,'2025-12-27 04:08:59.550710','2025-12-27 04:08:59.550715',172),(15,'Pharmacie Saint-Louis','423, chemin de Fernandes\n80595 Joly','Saint-Louis','Sénégal','+221823022460','contact@pharmaciesaint-louis.sn',NULL,NULL,'','{}','',1,'2025-12-27 04:08:59.551192','2025-12-27 04:08:59.551198',173);
/*!40000 ALTER TABLE `pharmacies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescriptions`
--

DROP TABLE IF EXISTS `prescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescriptions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `dosage` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `remarque` longtext COLLATE utf8mb4_unicode_ci,
  `date_prescription` datetime(6) NOT NULL,
  `consultation_id` bigint NOT NULL,
  `methode_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `prescriptions_consultation_id_7c2428c1_fk_consultations_pf_id` (`consultation_id`),
  KEY `prescriptions_methode_id_139b97ad_fk_methodes_contraceptives_id` (`methode_id`),
  CONSTRAINT `prescriptions_consultation_id_7c2428c1_fk_consultations_pf_id` FOREIGN KEY (`consultation_id`) REFERENCES `consultations_pf` (`id`),
  CONSTRAINT `prescriptions_methode_id_139b97ad_fk_methodes_contraceptives_id` FOREIGN KEY (`methode_id`) REFERENCES `methodes_contraceptives` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescriptions`
--

LOCK TABLES `prescriptions` WRITE;
/*!40000 ALTER TABLE `prescriptions` DISABLE KEYS */;
INSERT INTO `prescriptions` VALUES (14,'1 application par jour','','2025-12-27 04:08:59.689721',45,30),(15,'Selon les instructions','Prendre le matin','2025-12-27 04:08:59.690488',49,42),(16,'2 comprimés par jour','Avec un repas','2025-12-27 04:08:59.690871',53,34),(17,'2 comprimés par jour','Prendre le matin','2025-12-27 04:08:59.691439',56,42),(18,'Selon les instructions','','2025-12-27 04:08:59.692275',58,32),(19,'1 application par jour','Prendre le matin','2025-12-27 04:08:59.692840',63,36),(20,'2 comprimés par jour','Prendre le matin','2025-12-27 04:08:59.693421',70,39),(21,'1 application par jour','Prendre le matin','2025-12-27 04:08:59.694017',71,40),(22,'2 comprimés par jour','Avec un repas','2025-12-27 04:08:59.698960',73,32);
/*!40000 ALTER TABLE `prescriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produits`
--

DROP TABLE IF EXISTS `produits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produits` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code_barre` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `categorie` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `composition` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `posologie` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `contre_indications` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `fabricant` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prix_unitaire` decimal(10,2) NOT NULL,
  `unite` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prescription_requise` tinyint(1) NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `actif` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_barre` (`code_barre`),
  KEY `produits_categor_4bd210_idx` (`categorie`),
  KEY `produits_code_ba_3bad94_idx` (`code_barre`),
  KEY `produits_actif_c298dc_idx` (`actif`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produits`
--

LOCK TABLES `produits` WRITE;
/*!40000 ALTER TABLE `produits` DISABLE KEYS */;
INSERT INTO `produits` VALUES (21,'Paracétamol 500mg',NULL,'medicament','Description du produit Paracétamol 500mg','','','','Buisson',500.00,'unité',0,'',1,'2025-12-27 04:08:59.552749','2025-12-27 04:08:59.552756'),(22,'Ibuprofène 400mg',NULL,'medicament','Description du produit Ibuprofène 400mg','','','','Vallet',750.00,'unité',1,'',1,'2025-12-27 04:08:59.553485','2025-12-27 04:08:59.553490'),(23,'Amoxicilline 500mg',NULL,'medicament','Description du produit Amoxicilline 500mg','','','','François',1200.00,'unité',0,'',1,'2025-12-27 04:08:59.553990','2025-12-27 04:08:59.554006'),(24,'Pilule Jasmine',NULL,'contraceptif','Description du produit Pilule Jasmine','','','','Colin Lambert SARL',2500.00,'unité',0,'',1,'2025-12-27 04:08:59.554674','2025-12-27 04:08:59.554680'),(25,'Préservatifs Durex',NULL,'contraceptif','Description du produit Préservatifs Durex','','','','Normand Bazin et Fils',1500.00,'unité',0,'',1,'2025-12-27 04:08:59.555238','2025-12-27 04:08:59.555243'),(26,'Test de grossesse',NULL,'materiel_medical','Description du produit Test de grossesse','','','','Jacques Renaud SA',2000.00,'unité',1,'',1,'2025-12-27 04:08:59.555811','2025-12-27 04:08:59.555817'),(27,'Vitamine D3',NULL,'supplement','Description du produit Vitamine D3','','','','Dumas',3000.00,'unité',0,'',1,'2025-12-27 04:08:59.556420','2025-12-27 04:08:59.556425'),(28,'Fer + Acide folique',NULL,'supplement','Description du produit Fer + Acide folique','','','','Le Gall',2200.00,'unité',1,'',1,'2025-12-27 04:08:59.556938','2025-12-27 04:08:59.556943'),(29,'Savon antiseptique',NULL,'hygiene','Description du produit Savon antiseptique','','','','Leleu',800.00,'unité',1,'',1,'2025-12-27 04:08:59.557499','2025-12-27 04:08:59.557504'),(30,'Solution hydroalcoolique',NULL,'hygiene','Description du produit Solution hydroalcoolique','','','','Étienne S.A.R.L.',1200.00,'unité',1,'',1,'2025-12-27 04:08:59.558055','2025-12-27 04:08:59.558060');
/*!40000 ALTER TABLE `produits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rapports_consultations`
--

DROP TABLE IF EXISTS `rapports_consultations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rapports_consultations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diagnostic` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `traitement_prescrit` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `recommandations` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `suivi_necessaire` tinyint(1) NOT NULL,
  `date_prochain_rdv` date DEFAULT NULL,
  `documents` json NOT NULL,
  `envoye_patient` tinyint(1) NOT NULL,
  `date_envoi` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `consultation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `consultation_id` (`consultation_id`),
  CONSTRAINT `rapports_consultatio_consultation_id_13bf15ed_fk_consultat` FOREIGN KEY (`consultation_id`) REFERENCES `consultations_pf` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rapports_consultations`
--

LOCK TABLES `rapports_consultations` WRITE;
/*!40000 ALTER TABLE `rapports_consultations` DISABLE KEYS */;
/*!40000 ALTER TABLE `rapports_consultations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registres`
--

DROP TABLE IF EXISTS `registres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registres` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prenom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sexe` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` int NOT NULL,
  `residence` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ethnie` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profession` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_cni` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_cne` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `consultation_nc` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `consultation_ac` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `consultation_refere_asc` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `poids_kg` decimal(5,2) NOT NULL,
  `taille_cm` decimal(5,2) NOT NULL,
  `poids_taille` decimal(5,2) DEFAULT NULL,
  `taille_age` decimal(5,2) DEFAULT NULL,
  `imc` decimal(5,2) DEFAULT NULL,
  `motif_symptomes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `examen_labo_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `diagnostic` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `hopital_id` bigint NOT NULL,
  `patient_id` bigint DEFAULT NULL,
  `specialiste_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registres_specialiste_id_139b248a_fk_specialistes_id` (`specialiste_id`),
  KEY `registres_hopital_d3f1e7_idx` (`hopital_id`,`specialiste_id`),
  KEY `registres_patient_d86c69_idx` (`patient_id`),
  KEY `registres_date_cr_564348_idx` (`date_creation`),
  KEY `registres_numero__3c1104_idx` (`numero_cni`),
  KEY `registres_numero__b9f6d9_idx` (`numero_cne`),
  KEY `registres_actif_8c2634_idx` (`actif`),
  CONSTRAINT `registres_hopital_id_189486b8_fk_hopitaux_id` FOREIGN KEY (`hopital_id`) REFERENCES `hopitaux` (`id`),
  CONSTRAINT `registres_patient_id_1c14e788_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  CONSTRAINT `registres_specialiste_id_139b248a_fk_specialistes_id` FOREIGN KEY (`specialiste_id`) REFERENCES `specialistes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registres`
--

LOCK TABLES `registres` WRITE;
/*!40000 ALTER TABLE `registres` DISABLE KEYS */;
INSERT INTO `registres` VALUES (1,'Test','Patient','M',30,'Dakar','Wolof','Ingénieur','TEST123456789',NULL,'221771234567','test.patient@example.com','oui','non','non',70.50,175.00,40.29,5.83,23.02,'Consultation de routine','negatif','Patient en bonne santé','2026-01-21 20:03:46.190757','2026-01-21 20:03:46.237170',1,9,153,25),(2,'Test','Patient','M',30,'Dakar','Wolof','Ingénieur','TEST123456789',NULL,'221771234567','test.patient@example.com','oui','non','non',70.50,175.00,40.29,5.83,23.02,'Consultation de routine','negatif','Patient en bonne santé','2026-01-21 20:04:10.414142','2026-01-21 20:04:10.443187',1,9,153,25),(3,'Test','Patient','M',30,'Dakar','Wolof','Ingénieur','1234567890123',NULL,'221771234567','test.patient@example.com','oui','non','non',70.50,175.00,40.29,5.83,23.02,'Consultation de routine','negatif','Patient en bonne santé','2026-01-21 20:05:14.391679','2026-01-21 20:05:14.420909',1,9,151,25),(4,'Kouma','Mamadou','M',26,'Dakar','Sonike','Etudiant','1223389844',NULL,'788749980','k.moh9315@gmail.com','non','non','non',30.00,170.00,17.65,6.54,10.38,'mot de tête','negatif','En parfaite santé','2026-01-24 19:34:52.019294','2026-01-24 19:34:52.075349',1,9,154,25),(5,'Dembele','Arouna','M',30,'Bamako','senofo','Etudiant','122334884',NULL,'73902244','arouna@gmail.com','oui','non','non',60.00,170.00,35.29,5.67,20.76,'Cethalee','negatif','paludisme simple','2026-01-24 20:17:25.036371','2026-01-24 20:17:25.071084',1,9,155,25),(6,'Doumbia','Ousmane','M',30,'Bamako','Nounou','Financier','12344245',NULL,'+223 78 89 40 09','ousmane@gmail.com','oui','non','non',60.00,180.00,33.33,6.00,18.52,'Paludisme','positif','mot de tête récurent','2026-01-27 21:30:47.273736','2026-01-27 21:30:47.302257',1,9,156,25),(7,'Kouma','Mamadou','M',20,'Dakar','Sonike','Etudiant','11233455',NULL,'788749980','mamadoukouma@gmail.com','oui','non','non',70.00,170.00,41.18,8.50,24.22,'le paludisme','negatif','Palu','2026-02-01 05:33:59.491057','2026-02-01 05:33:59.532864',1,7,157,36);
/*!40000 ALTER TABLE `registres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rendez_vous`
--

DROP TABLE IF EXISTS `rendez_vous`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rendez_vous` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `datetime` datetime(6) NOT NULL,
  `statut` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `motif` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `confirme_par_specialiste` tinyint(1) NOT NULL,
  `date_confirmation` datetime(6) DEFAULT NULL,
  `date_refus` datetime(6) DEFAULT NULL,
  `motif_refus` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `hopital_id` bigint DEFAULT NULL,
  `patient_id` bigint NOT NULL,
  `specialiste_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rendez_vous_datetim_e59ee2_idx` (`datetime`),
  KEY `rendez_vous_statut_b81f5f_idx` (`statut`),
  KEY `rendez_vous_patient_517e5a_idx` (`patient_id`,`datetime`),
  KEY `rendez_vous_special_9e5061_idx` (`specialiste_id`,`datetime`),
  KEY `rendez_vous_hopital_d334d5_idx` (`hopital_id`),
  CONSTRAINT `rendez_vous_hopital_id_35b799fd_fk_hopitaux_id` FOREIGN KEY (`hopital_id`) REFERENCES `hopitaux` (`id`),
  CONSTRAINT `rendez_vous_patient_id_c9468442_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  CONSTRAINT `rendez_vous_specialiste_id_d7e04663_fk_specialistes_id` FOREIGN KEY (`specialiste_id`) REFERENCES `specialistes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=316 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rendez_vous`
--

LOCK TABLES `rendez_vous` WRITE;
/*!40000 ALTER TABLE `rendez_vous` DISABLE KEYS */;
INSERT INTO `rendez_vous` VALUES (201,'2025-12-08 19:59:04.732966','annule','Consultation prénatale',0,NULL,NULL,'','Figure beau allumer apprendre. Défaut sentiment mon éprouver. Métier travailler entrer troubler véritable.\nImaginer éviter avance train user. Car attitude escalier déjà.','2025-12-27 04:08:59.600496','2025-12-27 04:08:59.600500',7,121,30),(202,'2025-10-28 09:00:06.656450','termine','Consultation de routine',1,NULL,NULL,'','Hiver membre mettre. Compagnon cours installer.\nPort rocher installer en créer tout autre.\nTout claire céder matin agir valoir continuer.','2025-12-27 04:08:59.601247','2025-12-27 04:08:59.601252',7,130,36),(203,'2025-12-05 17:43:02.658689','termine','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.601687','2025-12-27 04:08:59.601692',8,120,31),(204,'2026-01-11 04:50:28.515529','confirme','Problème gynécologique',1,NULL,NULL,'','','2025-12-27 04:08:59.602133','2025-12-27 04:08:59.602137',7,137,30),(205,'2025-11-26 12:54:07.110490','annule','Consultation de routine',0,NULL,NULL,'','','2025-12-27 04:08:59.602548','2025-12-27 04:08:59.602552',8,133,32),(206,'2026-01-30 10:48:39.710920','confirme','Consultation de routine',1,NULL,NULL,'','','2025-12-27 04:08:59.602968','2025-12-27 04:08:59.602972',8,150,31),(207,'2026-02-21 10:14:15.073910','en_attente','Consultation prénatale',0,NULL,NULL,'','Dur voyager étranger pénétrer. Creuser étroit épais depuis. Précéder battre quatre bande sans confondre. Léger quarante art mal.','2025-12-27 04:08:59.603469','2025-12-27 04:08:59.603473',9,121,27),(208,'2026-01-21 08:07:27.100042','confirme','Consultation prénatale',1,NULL,NULL,'','Recevoir étaler rester inconnu. Ruine fait mari droit parvenir pensée grain.\nBas sortir fixer. Peau en finir oeuvre croiser.','2025-12-27 04:08:59.604023','2025-12-27 04:08:59.604027',8,137,28),(209,'2025-11-05 07:23:02.584433','annule','Suivi contraceptif',0,NULL,NULL,'','Briller trembler rejoindre croire droit bien. Secret accepter désert tourner bleu dehors réveiller. Mort sien huit tellement saint point prix rang.','2025-12-27 04:08:59.604869','2025-12-27 04:08:59.604873',7,141,36),(210,'2026-01-18 21:47:02.335051','en_attente','Problème gynécologique',0,NULL,NULL,'','','2025-12-27 04:08:59.605334','2025-12-27 04:08:59.605338',9,130,34),(211,'2026-01-22 12:02:01.454369','en_attente','Consultation de routine',0,NULL,NULL,'','Papier toucher monter vif souvent importer. Nombre ventre beau. Dix contenter devenir précipiter intérieur obéir doute leur.','2025-12-27 04:08:59.605909','2025-12-27 04:08:59.605916',7,135,30),(212,'2025-10-15 20:12:03.477618','annule','Consultation post-partum',0,NULL,NULL,'','','2025-12-27 04:08:59.606313','2025-12-27 04:08:59.606316',8,103,28),(213,'2025-09-27 03:01:38.128447','termine','Consultation post-partum',1,NULL,NULL,'','Très avouer veille soir autant maintenant. Hiver produire apercevoir chacun soudain y chance simplement. Soudain mal calme honneur nation.','2025-12-27 04:08:59.606897','2025-12-27 04:08:59.606901',7,125,30),(214,'2025-10-08 09:24:28.727973','termine','Consultation prénatale',1,NULL,NULL,'','Revoir révéler montagne depuis joue intérêt. Espoir malheur journal juste. Petit bout à parfaitement secret étendre.','2025-12-27 04:08:59.607354','2025-12-27 04:08:59.607360',7,116,26),(215,'2026-01-11 09:10:44.669115','en_attente','Consultation de routine',0,NULL,NULL,'','','2025-12-27 04:08:59.607932','2025-12-27 04:08:59.607939',7,144,26),(216,'2025-10-18 04:07:31.788985','termine','Suivi contraceptif',1,NULL,NULL,'','Cou franc paquet rose. Cause condamner dépasser. Sembler occuper environ fixe.\nPhrase apparence absolu école droite réclamer.\nOu encore titre veille prouver. Parent pitié revoir obtenir.','2025-12-27 04:08:59.608502','2025-12-27 04:08:59.608506',7,117,36),(217,'2025-11-08 21:20:43.333653','termine','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.608919','2025-12-27 04:08:59.608923',8,123,31),(218,'2025-12-29 22:41:12.662931','confirme','Consultation prénatale',1,NULL,NULL,'','Reconnaître point nom histoire chef tromper. Discours journée curiosité voler hors prêter.\nSecrétaire lune près geste. Tirer plus simplement rire chute jusque hésiter.','2025-12-27 04:08:59.609411','2025-12-27 04:08:59.609415',8,104,28),(219,'2026-01-12 16:16:39.809181','en_attente','Suivi contraceptif',0,NULL,NULL,'','Accuser riche printemps simplement. Tendre faux diriger doute te forme.\nDavantage gris autour vent argent jamais an. Sauter amuser rentrer selon. Sauter guère étrange colon briser dernier.','2025-12-27 04:08:59.610050','2025-12-27 04:08:59.610054',8,118,31),(220,'2025-10-27 00:15:39.826443','annule','Problème gynécologique',0,NULL,NULL,'','Sommeil printemps coin lumière le intention tantôt guère. Énergie frère léger sien précéder comment.','2025-12-27 04:08:59.610546','2025-12-27 04:08:59.610550',9,147,25),(221,'2025-10-14 01:07:03.593160','termine','Consultation post-partum',1,NULL,NULL,'','','2025-12-27 04:08:59.610967','2025-12-27 04:08:59.610971',9,111,35),(222,'2026-01-18 03:59:08.926116','en_attente','Problème gynécologique',0,NULL,NULL,'','Allumer jusque sourire lisser chien souffler lutter. Quand secret douter éviter accent selon oh. Président mari mouvement journal voir. Calme aider auprès entourer source corde engager.','2025-12-27 04:08:59.611480','2025-12-27 04:08:59.611484',7,146,26),(223,'2026-02-05 01:11:56.588806','confirme','Consultation de routine',1,NULL,NULL,'','','2025-12-27 04:08:59.611919','2025-12-27 04:08:59.611923',8,137,32),(224,'2025-10-01 23:26:38.606326','annule','Suivi contraceptif',0,NULL,NULL,'','','2025-12-27 04:08:59.612340','2025-12-27 04:08:59.612344',7,126,33),(225,'2025-10-29 04:20:58.808327','termine','Consultation post-partum',1,NULL,NULL,'','','2025-12-27 04:08:59.612740','2025-12-27 04:08:59.612744',9,117,27),(226,'2025-10-18 12:11:45.642131','termine','Consultation post-partum',1,NULL,NULL,'','Pourquoi pouvoir animal oh planche. Fort diriger content arrivée étude frère manger corde. Leur étudier suffire veiller trop pur.','2025-12-27 04:08:59.616415','2025-12-27 04:08:59.616418',9,101,29),(227,'2026-02-07 01:05:18.777941','confirme','Problème gynécologique',1,NULL,NULL,'','','2025-12-27 04:08:59.617275','2025-12-27 04:08:59.617279',7,141,30),(228,'2026-01-15 13:31:56.199171','en_attente','Problème gynécologique',0,NULL,NULL,'','Flamme car interroger valeur céder demeurer traiter. Roche note place tendre genou autrefois tellement. Pays beauté sept palais.','2025-12-27 04:08:59.618189','2025-12-27 04:08:59.618193',8,115,31),(229,'2026-01-24 13:54:35.515433','en_attente','Consultation prénatale',0,NULL,NULL,'','','2025-12-27 04:08:59.618738','2025-12-27 04:08:59.618743',9,149,34),(230,'2025-11-05 02:11:15.593192','termine','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.619234','2025-12-27 04:08:59.619238',8,144,28),(231,'2025-09-29 10:42:46.330775','annule','Consultation prénatale',0,NULL,NULL,'','Voyager surveiller machine glisser animer beau ensemble. François principe déchirer obliger.\nFait mort donner ensemble visage moyen. Parfaitement visite circonstance public imaginer.','2025-12-27 04:08:59.619800','2025-12-27 04:08:59.619804',8,123,31),(232,'2025-11-29 11:52:50.642431','annule','Consultation prénatale',0,NULL,NULL,'','','2025-12-27 04:08:59.620270','2025-12-27 04:08:59.620274',8,132,28),(233,'2025-11-08 06:39:25.237149','termine','Consultation post-partum',1,NULL,NULL,'','Éloigner ligne reconnaître entier puisque aussitôt veiller. De chaise simple nécessaire mort suffire. Afin De sauvage personne vaste entre.','2025-12-27 04:08:59.620777','2025-12-27 04:08:59.620781',7,147,26),(234,'2025-10-20 12:21:31.416245','termine','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.621174','2025-12-27 04:08:59.621178',9,132,34),(235,'2025-12-15 01:24:45.135560','termine','Suivi contraceptif',1,NULL,NULL,'','','2025-12-27 04:08:59.621548','2025-12-27 04:08:59.621553',7,124,26),(236,'2025-11-11 14:48:27.777810','annule','Problème gynécologique',0,NULL,NULL,'','','2025-12-27 04:08:59.621983','2025-12-27 04:08:59.621987',7,126,33),(237,'2025-12-11 13:41:10.785094','termine','Suivi contraceptif',1,NULL,NULL,'','','2025-12-27 04:08:59.622477','2025-12-27 04:08:59.622481',8,125,31),(238,'2026-01-17 20:16:39.970522','confirme','Problème gynécologique',1,NULL,NULL,'','','2025-12-27 04:08:59.622886','2025-12-27 04:08:59.622890',7,103,33),(239,'2025-12-08 18:47:28.909365','termine','Consultation post-partum',1,NULL,NULL,'','','2025-12-27 04:08:59.624731','2025-12-27 04:08:59.624735',7,109,36),(240,'2026-02-25 05:58:09.075940','en_attente','Consultation de routine',0,NULL,NULL,'','','2025-12-27 04:08:59.625231','2025-12-27 04:08:59.625235',8,144,32),(241,'2025-11-28 14:13:30.522506','termine','Problème gynécologique',1,NULL,NULL,'','Chaise douter cabinet seconde gauche.\nRelation danser absolu devant fort accent. Cesser connaissance poser.','2025-12-27 04:08:59.625715','2025-12-27 04:08:59.625720',9,149,34),(242,'2026-02-20 02:51:45.129785','annule','Consultation de routine',1,NULL,NULL,'','','2025-12-27 04:08:59.626112','2026-02-03 18:00:45.623702',9,102,29),(243,'2025-12-03 12:20:40.749122','termine','Consultation post-partum',1,NULL,NULL,'','','2025-12-27 04:08:59.626606','2025-12-27 04:08:59.626611',9,128,25),(244,'2025-12-29 17:15:04.188234','en_attente','Consultation de routine',0,NULL,NULL,'','','2025-12-27 04:08:59.626972','2025-12-27 04:08:59.626977',7,142,36),(245,'2026-01-18 06:20:28.385392','en_attente','Consultation post-partum',0,NULL,NULL,'','Maintenant genre mort peser étude fidèle douze. Retour tout saint éclairer demander fils. Souvenir heureux lier différent confiance.','2025-12-27 04:08:59.627468','2025-12-27 04:08:59.627472',8,132,28),(246,'2026-01-24 14:56:44.349570','annule','Suivi contraceptif',1,NULL,NULL,'','Ce parent ferme jeunesse réserver vrai. Mais musique arrêter cou adresser commencer plaisir.','2025-12-27 04:08:59.627964','2026-02-10 14:07:27.467169',7,110,36),(247,'2026-01-25 17:00:46.256523','en_attente','Consultation de routine',0,NULL,NULL,'','Devoir journée jouer. Vite semblable guère fauteuil juger étage.\nSombre suivre glace tout an intérieur angoisse sortir. Danger début jaune rang. Face ensemble corde profiter route bête.','2025-12-27 04:08:59.628474','2025-12-27 04:08:59.628478',7,140,26),(248,'2026-01-16 14:31:32.738943','en_attente','Suivi contraceptif',0,NULL,NULL,'','','2025-12-27 04:08:59.628886','2025-12-27 04:08:59.628890',7,149,26),(249,'2025-12-24 01:17:38.645244','termine','Suivi contraceptif',1,NULL,NULL,'','Aujourd\'Hui arbre forme ruine. Rouge rendre révéler livre quand exécuter pont.','2025-12-27 04:08:59.629358','2025-12-27 04:08:59.629362',8,110,31),(250,'2025-11-06 09:56:19.975246','annule','Consultation prénatale',0,NULL,NULL,'','Bien jambe théâtre loin retourner. Quel rouge demi.\nCertain terrible par expérience assister vent verre cacher. Servir tantôt reconnaître paysage.','2025-12-27 04:08:59.629892','2025-12-27 04:08:59.629896',9,122,29),(251,'2026-01-16 13:43:40.983856','en_attente','Suivi contraceptif',0,NULL,NULL,'','','2025-12-27 04:08:59.630339','2025-12-27 04:08:59.630343',8,117,31),(252,'2025-12-28 04:43:56.761077','en_attente','Consultation post-partum',0,NULL,NULL,'','Terrain différent quarante soi. Tirer avance partir atteindre aspect.\nCuriosité amener signifier. Métier mon certainement appuyer signer.','2025-12-27 04:08:59.630845','2025-12-27 04:08:59.630849',8,122,32),(253,'2026-02-12 03:34:45.968867','confirme','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.631351','2025-12-27 04:08:59.631355',8,135,28),(254,'2025-12-21 04:01:21.983195','termine','Suivi contraceptif',1,NULL,NULL,'','Ombre avance intention nu franc plonger. Compte réserver docteur voisin absolument. Confondre léger race relever.\nRire certain soulever fait. Marché naturellement large court trait cheval forêt.','2025-12-27 04:08:59.631873','2025-12-27 04:08:59.631877',8,122,32),(255,'2026-02-16 10:24:49.511397','en_attente','Consultation prénatale',0,NULL,NULL,'','','2025-12-27 04:08:59.632406','2025-12-27 04:08:59.632410',8,123,32),(256,'2026-02-02 04:20:11.115543','en_attente','Consultation de routine',0,NULL,NULL,'','','2025-12-27 04:08:59.633118','2025-12-27 04:08:59.633122',9,127,29),(257,'2025-12-13 03:02:00.813741','termine','Problème gynécologique',1,NULL,NULL,'','','2025-12-27 04:08:59.633555','2025-12-27 04:08:59.633559',7,119,30),(258,'2025-10-03 18:28:48.900359','termine','Problème gynécologique',1,NULL,NULL,'','','2025-12-27 04:08:59.634000','2025-12-27 04:08:59.634004',7,114,33),(259,'2025-10-15 14:08:28.434283','termine','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.634472','2025-12-27 04:08:59.634476',8,108,32),(260,'2026-02-16 12:01:30.432666','confirme','Suivi contraceptif',1,NULL,NULL,'','','2025-12-27 04:08:59.634879','2025-12-27 04:08:59.634883',9,125,29),(261,'2025-12-30 19:39:23.096835','en_attente','Problème gynécologique',0,NULL,NULL,'','Entourer afin de perte me. Couler crise saisir beaucoup. Dépasser remettre attendre ceci joue plante.\nBruit voix seul tromper. Cause abandonner ouvrage suivant.','2025-12-27 04:08:59.635436','2025-12-27 04:08:59.635440',9,122,27),(262,'2025-12-13 07:30:12.250910','annule','Consultation prénatale',0,NULL,NULL,'','Deviner expression celui rouler inconnu blanc. Violent tandis que frère poésie prince longtemps d\'abord. Suffire passion déposer égal prétendre nez.','2025-12-27 04:08:59.635995','2025-12-27 04:08:59.635999',7,143,26),(263,'2026-01-27 20:58:55.837012','en_attente','Problème gynécologique',0,NULL,NULL,'','','2025-12-27 04:08:59.636410','2025-12-27 04:08:59.636414',9,123,27),(264,'2026-01-25 06:41:31.408863','en_attente','Consultation post-partum',0,NULL,NULL,'','Coeur vague sien protéger passer croire voici. Prière suite soit épaule jeter. Plusieurs mode homme premier second.','2025-12-27 04:08:59.636971','2025-12-27 04:08:59.636975',9,149,27),(265,'2026-01-02 04:40:03.038436','confirme','Problème gynécologique',1,NULL,NULL,'','','2025-12-27 04:08:59.637433','2025-12-27 04:08:59.637437',8,137,31),(266,'2025-12-11 11:15:51.408063','termine','Consultation post-partum',1,NULL,NULL,'','','2025-12-27 04:08:59.637908','2025-12-27 04:08:59.637913',8,108,28),(267,'2026-02-15 18:53:27.564294','confirme','Problème gynécologique',1,NULL,NULL,'','Terrain repousser paraître franchir auprès combien révéler elle. Disparaître rouge voix ça nuage. Aventure race expérience sommeil précis saisir douceur. Longtemps hésiter rouge silencieux.','2025-12-27 04:08:59.638548','2025-12-27 04:08:59.638552',9,108,27),(268,'2026-01-14 22:46:03.494421','en_attente','Consultation post-partum',0,NULL,NULL,'','Pas au gens. Herbe sérieux ville groupe cheval. Gouvernement pays combat.\nImpression rouge curiosité.\nConsidérer envie soleil ton calmer confondre demander beauté.','2025-12-27 04:08:59.639183','2025-12-27 04:08:59.639187',7,133,26),(269,'2025-10-25 10:58:58.881243','termine','Consultation de routine',1,NULL,NULL,'','','2025-12-27 04:08:59.639692','2025-12-27 04:08:59.639696',8,135,28),(270,'2026-01-10 00:44:54.213213','confirme','Suivi contraceptif',1,NULL,NULL,'','','2025-12-27 04:08:59.640148','2025-12-27 04:08:59.640152',9,125,25),(271,'2025-10-15 02:07:57.199114','annule','Consultation prénatale',0,NULL,NULL,'','Chose rose consulter selon. Classe ciel acte transformer. Debout silence tout vieillard.\nAffirmer principe colon vieil céder question. Suivant prier juge celui contenir accompagner table.','2025-12-27 04:08:59.640716','2025-12-27 04:08:59.640720',7,147,26),(272,'2026-01-12 17:46:36.991494','confirme','Problème gynécologique',1,NULL,NULL,'','Hasard siège oreille apercevoir en colon trace. Rocher ne coûter quand battre sombre simple.','2025-12-27 04:08:59.641187','2025-12-27 04:08:59.641191',7,113,30),(273,'2025-11-08 14:51:27.074576','annule','Consultation prénatale',0,NULL,NULL,'','','2025-12-27 04:08:59.641722','2025-12-27 04:08:59.641726',9,102,34),(274,'2025-12-03 23:14:37.944378','termine','Consultation prénatale',1,NULL,NULL,'','Noir produire absolument mille quelque sauvage présent président. Vide haine leur drôle. Devoir main titre et distinguer fort remplacer si.','2025-12-27 04:08:59.642535','2025-12-27 04:08:59.642539',7,140,30),(275,'2025-11-14 07:51:25.259094','annule','Consultation de routine',0,NULL,NULL,'','Recueillir éviter fait presser histoire cheval donc. Premier désert fin prison.','2025-12-27 04:08:59.643194','2025-12-27 04:08:59.643198',9,125,29),(276,'2025-12-13 00:13:02.698096','termine','Problème gynécologique',1,NULL,NULL,'','Genre rejoindre chef occuper roi hiver fort. Produire est tout brusquement soleil expression. Ton circonstance hasard fer compagnie.\nFer preuve succès. Lentement victime social.','2025-12-27 04:08:59.643897','2025-12-27 04:08:59.643901',7,111,30),(277,'2025-11-10 02:44:42.075083','annule','Problème gynécologique',0,NULL,NULL,'','Retourner seul honte. Entourer main proposer lier. Remplir arme été tantôt source façon.','2025-12-27 04:08:59.644563','2025-12-27 04:08:59.644567',9,109,27),(278,'2026-02-04 22:15:43.968897','en_attente','Suivi contraceptif',0,NULL,NULL,'','Long assez etc est figure être voisin. Nuage main an animer. Acheter distinguer briller couvrir dresser inviter.','2025-12-27 04:08:59.645182','2025-12-27 04:08:59.645186',9,102,34),(279,'2026-01-17 01:17:23.708987','confirme','Consultation prénatale',1,NULL,NULL,'','Santé recommencer malgré admettre avant appartement. Malheur rouge mer président vision pied je.\nExemple disposer enfermer tu drame bas manier diriger. Obliger appel relever tomber vêtement noir.','2025-12-27 04:08:59.645842','2025-12-27 04:08:59.645845',7,137,30),(280,'2025-11-05 21:17:34.814824','termine','Suivi contraceptif',1,NULL,NULL,'','Blond raconter éclairer quarante. Bas maintenir chaud porte. Sou sortir produire crier franchir noire.','2025-12-27 04:08:59.646330','2025-12-27 04:08:59.646334',9,107,25),(281,'2025-09-28 02:52:04.018506','termine','Suivi contraceptif',1,NULL,NULL,'','Paysan mon rocher mensonge examiner résoudre. Chemise habiller rapidement accent étendue. Protéger connaissance d\'abord combat juger faible disposer silence.','2025-12-27 04:08:59.646822','2025-12-27 04:08:59.646826',9,126,34),(282,'2025-12-28 03:09:05.268476','confirme','Consultation de routine',1,NULL,NULL,'','Mot science parfois conduire vêtir. Immobile ennemi grand.\nSoleil effacer village histoire regard fond. Ci sembler troubler nul chance public.','2025-12-27 04:08:59.647393','2025-12-27 04:08:59.647397',9,134,35),(283,'2025-12-01 12:02:31.532090','termine','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.647872','2025-12-27 04:08:59.647876',9,143,34),(284,'2025-10-08 21:29:20.321415','termine','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.648774','2025-12-27 04:08:59.648778',7,124,36),(285,'2025-12-30 13:45:36.671508','en_attente','Consultation de routine',0,NULL,NULL,'','','2025-12-27 04:08:59.649702','2025-12-27 04:08:59.649706',9,106,25),(286,'2025-10-28 14:26:57.344768','annule','Problème gynécologique',0,NULL,NULL,'','','2025-12-27 04:08:59.650134','2025-12-27 04:08:59.650138',7,126,36),(287,'2026-01-15 14:14:25.609245','confirme','Consultation prénatale',1,NULL,NULL,'','Rappeler son serrer hauteur fatigue. Impression pluie pleurer sang prévenir.','2025-12-27 04:08:59.650639','2025-12-27 04:08:59.650643',7,120,30),(288,'2025-12-29 00:11:07.314020','annule','Consultation prénatale',0,NULL,NULL,'','Patron songer offrir inviter centre droite. Volonté mensonge salut fin.\nPlonger pays patron. Ceci détacher premier yeux pousser lentement. Contre or pouvoir défaut.','2025-12-27 04:08:59.651143','2026-02-03 02:43:25.914941',9,102,25),(289,'2025-11-27 08:03:31.887458','annule','Problème gynécologique',0,NULL,NULL,'','','2025-12-27 04:08:59.651629','2025-12-27 04:08:59.651633',9,107,35),(290,'2026-01-27 22:58:56.274871','confirme','Consultation post-partum',1,NULL,NULL,'','','2025-12-27 04:08:59.652101','2025-12-27 04:08:59.652105',9,132,35),(291,'2025-11-15 02:36:21.641016','annule','Problème gynécologique',0,NULL,NULL,'','Forêt ensemble vieux. Dieu passer sentier attacher supérieur sol. Présenter prévoir ville cas ailleurs meilleur commencer défendre.','2025-12-27 04:08:59.652662','2025-12-27 04:08:59.652666',7,136,26),(292,'2026-01-06 18:20:34.061141','en_attente','Suivi contraceptif',0,NULL,NULL,'','','2025-12-27 04:08:59.653099','2025-12-27 04:08:59.653103',8,146,28),(293,'2026-01-06 02:26:09.496230','en_attente','Suivi contraceptif',0,NULL,NULL,'','','2025-12-27 04:08:59.653537','2025-12-27 04:08:59.653541',9,128,34),(294,'2025-11-02 18:35:40.222262','annule','Problème gynécologique',0,NULL,NULL,'','','2025-12-27 04:08:59.654083','2025-12-27 04:08:59.654088',7,123,33),(295,'2025-11-13 13:39:36.412109','annule','Consultation de routine',0,NULL,NULL,'','','2025-12-27 04:08:59.654480','2025-12-27 04:08:59.654484',8,139,28),(296,'2026-01-08 18:08:04.884736','en_attente','Suivi contraceptif',0,NULL,NULL,'','Parti eau rang dieu signer fin. Crainte sang couleur aimer geste. Prétendre éteindre nul envelopper pont beaucoup.','2025-12-27 04:08:59.654966','2025-12-27 04:08:59.654970',9,127,35),(297,'2025-11-16 03:19:56.916067','termine','Suivi contraceptif',1,NULL,NULL,'','Rideau sortir plein âgé causer plutôt beau paix. Grand mince fatigue ce jeu.\nTout action éclater vous recommencer partir prouver. Oh maître oui abattre enfoncer obtenir rare idée.','2025-12-27 04:08:59.655478','2025-12-27 04:08:59.655481',7,110,30),(298,'2026-02-23 21:04:04.897329','en_attente','Consultation post-partum',0,NULL,NULL,'','Enfoncer noire chez profond. Folie devenir soldat petit comme repousser voyager.','2025-12-27 04:08:59.655995','2025-12-27 04:08:59.655999',8,145,28),(299,'2026-02-21 17:55:29.667787','confirme','Consultation prénatale',1,NULL,NULL,'','Cercle donc quitter déclarer d\'abord brûler delà. Entourer naturel armer fumée.','2025-12-27 04:08:59.656745','2025-12-27 04:08:59.656749',9,113,29),(300,'2025-11-25 16:14:14.604095','termine','Consultation prénatale',1,NULL,NULL,'','','2025-12-27 04:08:59.657266','2025-12-27 04:08:59.657271',7,142,26),(313,'2001-09-01 08:00:00.000000','en_attente','pallu',0,NULL,NULL,'',NULL,'2026-02-03 17:34:25.016372','2026-02-03 17:34:25.016380',7,102,36),(314,'2001-09-01 10:00:00.000000','en_attente','lol',0,NULL,NULL,'',NULL,'2026-02-03 17:58:55.430626','2026-02-03 17:58:55.430635',7,102,36),(315,'2026-01-03 08:00:00.000000','confirme','pallu',0,NULL,NULL,'',NULL,'2026-02-03 23:24:03.496123','2026-02-10 14:07:14.314655',7,158,36);
/*!40000 ALTER TABLE `rendez_vous` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titre` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `contenu_detail` longtext COLLATE utf8mb4_unicode_ci,
  `icone` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ordre` int NOT NULL,
  `landing_page_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `services_landing_page_id_f5fec77f_fk_landing_page_content_id` (`landing_page_id`),
  CONSTRAINT `services_landing_page_id_f5fec77f_fk_landing_page_content_id` FOREIGN KEY (`landing_page_id`) REFERENCES `landing_page_content` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (17,'Consultation Gynécologique','Consultations spécialisées en gynécologie',NULL,'Heart',0,1),(18,'Planification Familiale','Conseils et méthodes contraceptives',NULL,'Users',1,1),(19,'Suivi de Grossesse','Accompagnement pendant la grossesse',NULL,'Baby',2,1),(20,'Urgences','Prise en charge des urgences 24h/24',NULL,'AlertCircle',3,1);
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions_utilisateurs`
--

DROP TABLE IF EXISTS `sessions_utilisateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions_utilisateurs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` char(39) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_agent` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `device_info` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `derniere_activite` datetime(6) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_key` (`session_key`),
  KEY `sessions_ut_user_id_01e723_idx` (`user_id`,`active`),
  KEY `sessions_ut_session_ddea74_idx` (`session_key`),
  CONSTRAINT `sessions_utilisateurs_user_id_b59106ea_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions_utilisateurs`
--

LOCK TABLES `sessions_utilisateurs` WRITE;
/*!40000 ALTER TABLE `sessions_utilisateurs` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessions_utilisateurs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specialistes`
--

DROP TABLE IF EXISTS `specialistes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `specialistes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_ordre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `titre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `annees_experience` int NOT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `tarif_consultation` decimal(10,2) NOT NULL,
  `duree_consultation` int NOT NULL,
  `photo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `accepte_nouveaux_patients` tinyint(1) NOT NULL,
  `consultation_en_ligne` tinyint(1) NOT NULL,
  `note_moyenne` decimal(3,2) NOT NULL,
  `nombre_avis` int NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `hopital_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `specialite_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_ordre` (`numero_ordre`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `specialistes_user_id_hopital_id_78bbfe84_uniq` (`user_id`,`hopital_id`),
  KEY `specialiste_hopital_e39e76_idx` (`hopital_id`,`specialite_id`),
  KEY `specialiste_actif_abba09_idx` (`actif`),
  KEY `specialistes_specialite_id_053f71b7_fk_specialites_id` (`specialite_id`),
  CONSTRAINT `specialistes_hopital_id_f2f0baa7_fk_hopitaux_id` FOREIGN KEY (`hopital_id`) REFERENCES `hopitaux` (`id`),
  CONSTRAINT `specialistes_specialite_id_053f71b7_fk_specialites_id` FOREIGN KEY (`specialite_id`) REFERENCES `specialites` (`id`),
  CONSTRAINT `specialistes_user_id_6f5d0906_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specialistes`
--

LOCK TABLES `specialistes` WRITE;
/*!40000 ALTER TABLE `specialistes` DISABLE KEYS */;
INSERT INTO `specialistes` VALUES (25,'ORD1000','Docteur en Médecine',2,'Spécialiste en Pédiatrie avec 16 années d\'expérience.',30000.00,45,'',0,1,0.00,0,1,'2025-12-27 04:08:59.399830','2025-12-27 04:08:59.399863',9,157,19),(26,'ORD1001','Docteur en Médecine',5,'Spécialiste en Gynécologie-Obstétrique avec 14 années d\'expérience.',30000.00,60,'',1,0,0.00,0,1,'2025-12-27 04:08:59.402940','2025-12-27 04:08:59.402973',7,158,17),(27,'ORD1002','Docteur en Médecine',6,'Spécialiste en Médecine Générale avec 10 années d\'expérience.',25000.00,30,'',1,0,0.00,0,1,'2025-12-27 04:08:59.404010','2025-12-27 04:08:59.404046',9,159,18),(28,'ORD1003','Docteur en Médecine',12,'Spécialiste en Gynécologie-Obstétrique avec 13 années d\'expérience.',20000.00,30,'',1,0,0.00,0,1,'2025-12-27 04:08:59.406776','2025-12-27 04:08:59.406800',8,160,17),(29,'ORD1004','Docteur en Médecine',24,'Spécialiste en Pédiatrie avec 17 années d\'expérience.',20000.00,60,'',1,0,0.00,0,1,'2025-12-27 04:08:59.414929','2025-12-27 04:08:59.415198',9,161,19),(30,'ORD1005','Docteur en Médecine',9,'Spécialiste en Médecine Générale avec 12 années d\'expérience.',20000.00,45,'',1,1,0.00,0,1,'2025-12-27 04:08:59.416504','2025-12-27 04:08:59.416523',7,162,18),(31,'ORD1006','Docteur en Médecine',12,'Spécialiste en Pédiatrie avec 4 années d\'expérience.',25000.00,60,'',1,0,0.00,0,1,'2025-12-27 04:08:59.417738','2025-12-27 04:08:59.417772',8,163,19),(32,'ORD1007','Docteur en Médecine',17,'Spécialiste en Gynécologie-Obstétrique avec 20 années d\'expérience.',20000.00,60,'',1,0,0.00,0,1,'2025-12-27 04:08:59.420552','2025-12-27 04:08:59.420570',8,164,17),(33,'ORD1008','Docteur en Médecine',20,'Spécialiste en Cardiologie avec 21 années d\'expérience.',25000.00,30,'',1,0,0.00,0,1,'2025-12-27 04:08:59.421338','2025-12-27 04:08:59.421349',7,165,20),(34,'ORD1009','Docteur en Médecine',25,'Spécialiste en Dermatologie avec 24 années d\'expérience.',25000.00,60,'',1,0,0.00,0,1,'2025-12-27 04:08:59.421906','2025-12-27 04:08:59.421913',9,166,21),(35,'ORD1010','Docteur en Médecine',18,'Spécialiste en Pédiatrie avec 20 années d\'expérience.',30000.00,60,'',1,1,0.00,0,1,'2025-12-27 04:08:59.422721','2025-12-27 04:08:59.422730',9,167,19),(36,'ORD1011','Dr',23,'Spécialiste en Psychiatrie avec 18 années d\'expérience.',15000.00,60,'',1,1,0.00,0,1,'2025-12-27 04:08:59.424136','2026-01-13 20:20:58.128550',7,168,24);
/*!40000 ALTER TABLE `specialistes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specialites`
--

DROP TABLE IF EXISTS `specialites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `specialites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `icone` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specialites`
--

LOCK TABLES `specialites` WRITE;
/*!40000 ALTER TABLE `specialites` DISABLE KEYS */;
INSERT INTO `specialites` VALUES (17,'Gynécologie-Obstétrique','GYNO','Santé reproductive féminine','Heart',1,'2025-12-27 04:08:59.380112'),(18,'Médecine Générale','MGEN','Médecine générale et familiale','Stethoscope',1,'2025-12-27 04:08:59.380748'),(19,'Pédiatrie','PEDI','Médecine des enfants','Baby',1,'2025-12-27 04:08:59.381818'),(20,'Cardiologie','CARD','Maladies cardiovasculaires','Heart',1,'2025-12-27 04:08:59.382320'),(21,'Dermatologie','DERM','Maladies de la peau','Scan',1,'2025-12-27 04:08:59.382822'),(22,'Ophtalmologie','OPHT','Maladies des yeux','Eye',1,'2025-12-27 04:08:59.383983'),(23,'Endocrinologie','ENDO','Troubles hormonaux','Activity',1,'2025-12-27 04:08:59.389472'),(24,'Psychiatrie','PSYC','Santé mentale','Brain',1,'2025-12-27 04:08:59.391175');
/*!40000 ALTER TABLE `specialites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stocks`
--

DROP TABLE IF EXISTS `stocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stocks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantite` int NOT NULL,
  `seuil` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `methode_id` bigint NOT NULL,
  `pharmacie_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stocks_pharmacie_id_methode_id_77365598_uniq` (`pharmacie_id`,`methode_id`),
  KEY `stocks_pharmac_8e3d94_idx` (`pharmacie_id`,`methode_id`),
  KEY `stocks_methode_id_92e8e6a1_fk_methodes_contraceptives_id` (`methode_id`),
  CONSTRAINT `stocks_pharmacie_id_070f5649_fk_pharmacies_id` FOREIGN KEY (`pharmacie_id`) REFERENCES `pharmacies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stocks`
--

LOCK TABLES `stocks` WRITE;
/*!40000 ALTER TABLE `stocks` DISABLE KEYS */;
INSERT INTO `stocks` VALUES (61,188,6,'2025-12-27 04:08:59.558688','2025-12-27 04:08:59.558694',29,11),(62,187,5,'2025-12-27 04:08:59.559227','2025-12-27 04:08:59.559236',29,12),(63,69,17,'2025-12-27 04:08:59.559795','2025-12-27 04:08:59.559801',29,13),(64,136,20,'2025-12-27 04:08:59.560155','2025-12-27 04:08:59.560161',30,11),(65,15,6,'2025-12-27 04:08:59.560858','2025-12-27 04:08:59.560864',30,12),(66,15,17,'2025-12-27 04:08:59.561800','2025-12-27 04:08:59.561805',30,13),(67,20,18,'2025-12-27 04:08:59.562283','2025-12-27 04:08:59.562287',31,11),(68,113,19,'2025-12-27 04:08:59.562809','2025-12-27 04:08:59.562814',31,12),(69,30,19,'2025-12-27 04:08:59.563261','2025-12-27 04:08:59.563266',31,13),(70,63,11,'2025-12-27 04:08:59.563702','2025-12-27 04:08:59.563707',32,11),(71,180,13,'2025-12-27 04:08:59.564176','2025-12-27 04:08:59.564181',32,12),(72,113,12,'2025-12-27 04:08:59.564737','2025-12-27 04:08:59.564742',32,13),(73,67,12,'2025-12-27 04:08:59.565205','2025-12-27 04:08:59.565210',33,11),(74,129,19,'2025-12-27 04:08:59.566112','2025-12-27 04:08:59.566117',33,12),(75,199,17,'2025-12-27 04:08:59.566583','2025-12-27 04:08:59.566588',33,13),(76,106,18,'2025-12-27 04:08:59.567953','2025-12-27 04:08:59.567958',34,11),(77,189,20,'2025-12-27 04:08:59.568304','2025-12-27 04:08:59.568311',34,12),(78,142,14,'2025-12-27 04:08:59.568649','2025-12-27 04:08:59.568654',34,13),(79,24,6,'2025-12-27 04:08:59.569097','2025-12-27 04:08:59.569102',35,11),(80,64,13,'2025-12-27 04:08:59.569579','2025-12-27 04:08:59.569584',35,12),(81,46,14,'2025-12-27 04:08:59.570043','2025-12-27 04:08:59.570047',35,13),(82,45,10,'2025-12-27 04:08:59.570482','2025-12-27 04:08:59.570486',36,11),(83,184,6,'2025-12-27 04:08:59.571297','2025-12-27 04:08:59.571302',36,12),(84,164,14,'2025-12-27 04:08:59.571778','2025-12-27 04:08:59.571783',36,13),(85,47,19,'2025-12-27 04:08:59.572243','2025-12-27 04:08:59.572249',37,11),(86,127,6,'2025-12-27 04:08:59.572742','2025-12-27 04:08:59.572746',37,12),(87,104,17,'2025-12-27 04:08:59.573229','2025-12-27 04:08:59.573233',37,13),(88,56,5,'2025-12-27 04:08:59.573673','2025-12-27 04:08:59.573678',38,11),(89,132,17,'2025-12-27 04:08:59.574106','2025-12-27 04:08:59.574111',38,12),(90,96,10,'2025-12-27 04:08:59.575290','2025-12-27 04:08:59.575297',38,13);
/*!40000 ALTER TABLE `stocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stocks_produits`
--

DROP TABLE IF EXISTS `stocks_produits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stocks_produits` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantite` int NOT NULL,
  `seuil_alerte` int NOT NULL,
  `numero_lot` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_expiration` date DEFAULT NULL,
  `prix_vente` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `pharmacie_id` bigint NOT NULL,
  `produit_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stocks_produits_pharmacie_id_produit_id_numero_lot_ed9537b2_uniq` (`pharmacie_id`,`produit_id`,`numero_lot`),
  KEY `stocks_prod_pharmac_a4f931_idx` (`pharmacie_id`,`produit_id`),
  KEY `stocks_prod_date_ex_16cb07_idx` (`date_expiration`),
  KEY `stocks_produits_produit_id_757f3521_fk_produits_id` (`produit_id`),
  CONSTRAINT `stocks_produits_pharmacie_id_398a4d41_fk_pharmacies_id` FOREIGN KEY (`pharmacie_id`) REFERENCES `pharmacies` (`id`),
  CONSTRAINT `stocks_produits_produit_id_757f3521_fk_produits_id` FOREIGN KEY (`produit_id`) REFERENCES `produits` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stocks_produits`
--

LOCK TABLES `stocks_produits` WRITE;
/*!40000 ALTER TABLE `stocks_produits` DISABLE KEYS */;
INSERT INTO `stocks_produits` VALUES (64,104,18,'LOT714158','2027-06-05',712.10,'2025-12-27 04:08:59.576435','2025-12-27 04:08:59.576441',13,21),(65,59,6,'LOT289035','2026-05-05',663.81,'2025-12-27 04:08:59.579132','2025-12-27 04:08:59.579137',15,21),(66,65,7,'LOT903896','2027-09-22',992.25,'2025-12-27 04:08:59.579616','2026-02-13 20:46:07.508257',11,22),(67,52,20,'LOT148818','2026-03-05',832.56,'2025-12-27 04:08:59.580056','2025-12-27 04:08:59.580060',13,22),(68,35,6,'LOT782775','2026-08-23',936.03,'2025-12-27 04:08:59.580501','2025-12-27 04:08:59.580505',14,22),(69,50,7,'LOT135704','2027-10-24',860.39,'2025-12-27 04:08:59.580932','2025-12-27 04:08:59.580936',15,22),(70,6,18,'LOT606659','2026-12-18',1407.31,'2025-12-27 04:08:59.581397','2026-02-13 20:41:51.807754',11,23),(71,37,15,'LOT275946','2026-03-20',1654.92,'2025-12-27 04:08:59.581902','2025-12-27 04:08:59.581908',13,23),(72,90,19,'LOT669466','2026-09-17',1355.05,'2025-12-27 04:08:59.582983','2025-12-27 04:08:59.582988',15,23),(73,40,16,'LOT193022','2026-05-25',1334.58,'2025-12-27 04:08:59.583414','2025-12-27 04:08:59.583418',14,23),(74,88,7,'LOT234170','2027-10-24',1632.43,'2025-12-27 04:08:59.584367','2025-12-27 04:08:59.584372',12,23),(75,10,13,'LOT197161','2026-03-09',3149.92,'2025-12-27 04:08:59.584998','2026-01-08 03:32:02.011781',11,24),(76,23,23,'LOT245602','2027-06-08',3086.62,'2025-12-27 04:08:59.585449','2025-12-27 04:08:59.585455',13,24),(77,60,7,'LOT657181','2026-11-21',3423.73,'2025-12-27 04:08:59.585850','2025-12-27 04:08:59.585855',15,24),(78,120,16,'LOT539085','2027-10-29',3623.16,'2025-12-27 04:08:59.586284','2025-12-27 04:08:59.586289',14,24),(79,106,5,'LOT527056','2027-09-19',3003.80,'2025-12-27 04:08:59.586789','2025-12-27 04:08:59.586794',12,24),(80,115,23,'LOT718327','2027-11-12',1872.03,'2025-12-27 04:08:59.587282','2025-12-27 04:08:59.587286',13,25),(81,0,7,'LOT523654','2027-03-16',1734.86,'2025-12-27 04:08:59.587739','2025-12-27 04:08:59.587744',14,25),(83,51,16,'LOT709303','2026-08-18',1907.21,'2025-12-27 04:08:59.588690','2025-12-27 04:08:59.588696',15,25),(84,14,14,'LOT361727','2026-05-25',2323.79,'2025-12-27 04:08:59.589155','2025-12-27 04:08:59.589160',13,26),(85,108,20,'LOT797688','2027-11-08',2267.01,'2025-12-27 04:08:59.589593','2025-12-27 04:08:59.589597',11,26),(86,0,20,'LOT135822','2027-02-15',2925.30,'2025-12-27 04:08:59.590132','2025-12-27 04:08:59.590137',12,26),(87,132,23,'LOT695189','2026-04-27',2363.38,'2025-12-27 04:08:59.590553','2025-12-27 04:08:59.590558',15,26),(88,66,25,'LOT264482','2027-12-10',2239.57,'2025-12-27 04:08:59.591057','2025-12-27 04:08:59.591063',14,26),(89,123,13,'LOT354529','2026-10-13',3573.67,'2025-12-27 04:08:59.591562','2025-12-27 04:08:59.591567',14,27),(90,30,13,'LOT662450','2026-06-10',4387.05,'2025-12-27 04:08:59.591959','2025-12-27 04:08:59.591964',12,27),(91,70,21,'LOT979780','2027-05-15',4088.90,'2025-12-27 04:08:59.592370','2025-12-27 04:08:59.592375',13,27),(92,75,21,'LOT740997','2026-06-16',3379.26,'2025-12-27 04:08:59.592807','2025-12-27 04:08:59.592812',11,27),(93,69,18,'LOT100142','2026-11-25',3308.83,'2025-12-27 04:08:59.593303','2025-12-27 04:08:59.593308',15,27),(94,95,15,'LOT948363','2026-11-03',2749.33,'2025-12-27 04:08:59.593770','2025-12-27 04:08:59.593775',13,28),(95,41,9,'LOT873101','2026-07-31',2493.74,'2025-12-27 04:08:59.594906','2025-12-27 04:08:59.594911',14,28),(96,22,12,'LOT666182','2026-11-28',3090.52,'2025-12-27 04:08:59.595585','2025-12-27 04:08:59.595590',12,28),(97,109,9,'LOT681514','2026-07-07',3271.04,'2025-12-27 04:08:59.596031','2025-12-27 04:08:59.596035',15,28),(98,24,18,'LOT816146','2027-05-29',998.59,'2025-12-27 04:08:59.596431','2026-02-12 00:14:48.457962',12,29),(99,85,14,'LOT389698','2026-09-03',887.25,'2025-12-27 04:08:59.596828','2025-12-27 04:08:59.596833',14,29),(100,143,16,'LOT727392','2026-03-01',952.39,'2025-12-27 04:08:59.597227','2025-12-27 04:08:59.597232',13,29),(101,54,22,'LOT863877','2027-11-10',909.34,'2025-12-27 04:08:59.597666','2025-12-27 04:08:59.597671',11,29),(102,51,24,'LOT435485','2026-12-02',1089.96,'2025-12-27 04:08:59.598094','2025-12-27 04:08:59.598099',15,29),(103,93,20,'LOT455732','2027-03-28',1635.70,'2025-12-27 04:08:59.598486','2025-12-27 04:08:59.598490',12,30),(104,136,11,'LOT718806','2026-04-21',1664.99,'2025-12-27 04:08:59.598947','2025-12-27 04:08:59.598952',15,30),(105,1000,10,'LOT-2024-001','2026-05-23',130.00,'2026-02-13 19:45:08.252351','2026-02-13 19:45:08.273382',11,23);
/*!40000 ALTER TABLE `stocks_produits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=244 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('pbkdf2_sha256$1000000$vTX9cI2ejZ3DvpMfRQn5GM$d/A+04rfO+0J5P7wR11oikpRqZUwPt9iyMRbvy80dl4=',153,'Super Administrateur','admin@system.sn','super_admin',1,0,0,'2025-12-27 04:08:49.732322',NULL),('pbkdf2_sha256$1000000$PM2y7LfN19vyYL4nZaVdMN$HNE0wdJXPD9kZ27kXnGysbmwvMivpnOX7Kq20CWhPEc=',154,'Dr. Amadou Ba','admin.abassndao@hopital.sn','admin_hopital',1,0,0,'2025-12-27 04:08:49.930189',NULL),('pbkdf2_sha256$1000000$m3TULGTeB8Fjs3oZOFjoqZ$28NtBpQfhVCLmiE8Er4wS4fGamlCdAcH7Yw+ulZRVf0=',155,'Dr. Fatou Sall','admin.hoggy@hopital.sn','admin_hopital',1,0,0,'2025-12-27 04:08:50.226656',NULL),('pbkdf2_sha256$1000000$iFCt3IOLfo67hfnPIRsCZv$ffCu8VtNaS71+6BAAl2L1dmhCcOVlN3c+e4gDhKQlWI=',156,'Dr. Ousmane Diop','admin.dalal@hopital.sn','admin_hopital',1,0,0,'2025-12-27 04:08:50.354441',NULL),('pbkdf2_sha256$1000000$e1CGTA3rQvEZYcvrw6JrmC$rWg7usiJpGDk9NmscJ57PvG1+393TuXiYTBTBMTtLcs=',157,'Dr. Aissatou Diallo','aissatou.diallo@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:50.477248',NULL),('pbkdf2_sha256$1000000$0SO0713xPRYni8CG9hKSjv$WOZ/wMiJ0BInbw1Yoxc2Wsi19tYfWw/oME/gg76sPFM=',158,'Dr. Mamadou Ndiaye','mamadou.ndiaye@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:50.592501',NULL),('pbkdf2_sha256$1000000$iRZzr4J4rYSZNxHarxYtBK$r/1Ue/9zWpaPRoVw1RCsGHeIcq8lbf9mfWKKDUZCK8A=',159,'Dr. Khadija Fall','khadija.fall@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:50.708534',NULL),('pbkdf2_sha256$1000000$4cwt4EUf184MiO38jEwApb$Bk+IU5S7ONaNmOtUxoBdjhzI3aPaeAc87tgI0Je+S90=',160,'Dr. Ibrahima Sarr','ibrahima.sarr@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:50.827802',NULL),('pbkdf2_sha256$1000000$DGt779i4WlgmXWc6h487ZK$IiQB7aLsp6qW2bWY3DwArkwF0/UfpXD70QbBYeEUcfc=',161,'Dr. Mariama Cissé','mariama.cissé@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:50.946816',NULL),('pbkdf2_sha256$1000000$4nVgWzTeXTdsoYJRmht1mz$LH2vsXQXeekNf6uTiEIyIJWBQhaUW5SoO+GZZHQj42c=',162,'Dr. Cheikh Sy','cheikh.sy@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:51.063222',NULL),('pbkdf2_sha256$1000000$DiVEgd1H6pTL8APNftzXHQ$UYuAbJHPHXES99ukM+lbScWy3Hz/U1ajFMav0v2mvDY=',163,'Dr. Aminata Touré','aminata.touré@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:51.181202',NULL),('pbkdf2_sha256$1000000$MxTzhPwFTwrTAJDxdfwYNB$5yIrEyvxNmlFfjV8jEaATbNut7fbfWeZlQbwHJlEE5c=',164,'Dr. Moussa Kane','moussa.kane@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:51.297745',NULL),('pbkdf2_sha256$1000000$9QaMqOcPvdVIpN5KnxcgZS$8oiRkWUq6HRC83hPARjAIp4UL8axmT+0OZoUAaBdt/A=',165,'Dr. Binta Sow','binta.sow@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:51.419572',NULL),('pbkdf2_sha256$1000000$8ETFCDWHYFhSM2nt7IaJmj$56JzetbaJ4IeRcotZYgyPwivUc33bpvI7ls6+5kgj6g=',166,'Dr. Alioune Badara','alioune.badara@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:51.539108',NULL),('pbkdf2_sha256$1000000$G0WPKMEGCfiyizZdoXUXKL$Vl9kFNoNqdzQ103Iuey79deAxDQ03XygMee4zQiFm9o=',167,'Dr. Ndeye Fatou','ndeye.fatou@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:51.656101',NULL),('pbkdf2_sha256$1000000$hxLIsM3kPSC712YKpAUZuY$ygp2sqVOfYzzbfY+QA0KbAMyFc7UzI25V8jb3qzV2kk=',168,'Dr. Babacar Dieng','babacar.dieng@hopital.sn','specialiste',1,0,0,'2025-12-27 04:08:51.777358',NULL),('pbkdf2_sha256$1000000$foN8Aj5c4Oxxu9klbk9e0j$M1LJtvDP5AX+0HVjMfDxwt8kuH2fSGSbsd7JyuZkgx8=',169,'Pharmacien Abdou Diouf','abdou.diouf@pharma.sn','pharmacien',1,0,0,'2025-12-27 04:08:51.894026',NULL),('pbkdf2_sha256$1000000$sABvv4VvmVTaESavaFiBJE$Q5c6avr7WwaLWy9XfEUi5kDtxiHfHUM+FCArxsn6Q6M=',170,'Pharmacienne Rama Seck','rama.seck@pharma.sn','pharmacien',1,0,0,'2025-12-27 04:08:52.012851',NULL),('pbkdf2_sha256$1000000$3ZAq0pPMRwgtW2Ll4dzCP1$udQViAy3xCePNf0MWYMSC77p6gjR8kutOk2sG13Uam0=',171,'Pharmacien Modou Faye','modou.faye@pharma.sn','pharmacien',1,0,0,'2025-12-27 04:08:52.134917',NULL),('pbkdf2_sha256$1000000$tQjOqAZSulLcmhVTlIOqhz$Dn98OmQrn3fmZekAWn9zwaENPX9wThtza5H3GmaWfAw=',172,'Pharmacienne Awa Diop','awa.diop@pharma.sn','pharmacien',1,0,0,'2025-12-27 04:08:52.257977',NULL),('pbkdf2_sha256$1000000$iB8vn2bsttt8GDf7Ho9YO8$LTHvHny6ijw1ufI1HZAWXnNPs03+sAoygDIUThBCRa4=',173,'Pharmacien Saliou Ba','saliou.ba@pharma.sn','pharmacien',1,0,0,'2025-12-27 04:08:52.381162',NULL),('pbkdf2_sha256$1000000$d7lPcW3Ra0erjmIPMH2EXk$/CQMBxoPnZikvSOzc+CHib0q4FckDuLXc49ldbhv1q8=',174,'Agent Alves','agent1@hopital.sn','agent_enregistrement',1,0,0,'2025-12-27 04:08:52.512765',NULL),('pbkdf2_sha256$1000000$ybe2pIhm4FmnoRVNbRj8Ia$/pCQiBpyTeeHf2SRO8D9qlQIY9Lt2Tr1oItNJfninm0=',175,'Agent Marty','agent2@hopital.sn','agent_enregistrement',1,0,0,'2025-12-27 04:08:52.640656',NULL),('pbkdf2_sha256$1000000$UFAf4zPQ64XoW6MuWaFF3a$9sGHfLF7i7pAMS84dkvQf8L64rLyURzfPIsY7QGDAU8=',176,'Agent Pineau','agent3@hopital.sn','agent_enregistrement',1,0,0,'2025-12-27 04:08:52.765026',NULL),('pbkdf2_sha256$1000000$k3RNTKjGeYmw4dbbDFa2oX$xxyygCTUKb6SbtrgeySfQ/ThQUCyH649udxDx3wSBmE=',177,'Agent Lopes','agent4@hopital.sn','agent_enregistrement',1,0,0,'2025-12-27 04:08:52.928094',NULL),('pbkdf2_sha256$1000000$LRoQQtbumoKfEVG4IFR5KQ$ApdAlY1RU3g1tX6t7zo2nG0HtaemsB0PT7imbt23aXI=',178,'Agent Carpentier','agent5@hopital.sn','agent_enregistrement',1,0,0,'2025-12-27 04:08:53.055266',NULL),('pbkdf2_sha256$1000000$cL8IJsx6QyengaDKsYh7Ti$68AfNIEjmrh2BtkplaIiL0hfmYuPTUJ4GDoHy8blCtU=',179,'Gosselin','lecomtedaniel@example.net','patient',1,0,0,'2025-12-27 04:08:53.174628',NULL),('pbkdf2_sha256$1000000$2MBrwYXGxrKMNxoGrBWgtY$acghqjbSqeuJAyntiCof+e0AeNv9m9vsHVR4xq9EnSM=',180,'Gilles','margot68@example.net','patient',1,0,0,'2025-12-27 04:08:53.292351',NULL),('pbkdf2_sha256$1000000$hFnjUDbSpQOwtL8T8waWdy$iBCs1Amyy1+VCdKKT/3UcB9MdAJrBA5JLk7lVcXOlK8=',181,'Carlier','mauriceribeiro@example.org','patient',1,0,0,'2025-12-27 04:08:53.411855',NULL),('pbkdf2_sha256$1000000$epNm8cPBY0enORtZc28Dh9$tpR2FP5GgAi+SnyN2Gs2IpkZeRWBphih7UDRIqMUysU=',182,'Carpentier','wdufour@example.org','patient',1,0,0,'2025-12-27 04:08:53.534969',NULL),('pbkdf2_sha256$1000000$cMGPyPCvXPF4wXUKWfJrM3$49SdhYEHjosSpVsoI+pIXza3xSOnfawo8fFdySFvzgM=',183,'Lefort','andre55@example.com','patient',1,0,0,'2025-12-27 04:08:53.669885',NULL),('pbkdf2_sha256$1000000$aNNbAkq5b2xGTsSH7jTfZq$GhG2pNtwR3pM9eDK4jgWCiG2vzbLodOBa3PW/Vdcp0A=',184,'Bodin','andresauvage@example.org','patient',1,0,0,'2025-12-27 04:08:53.789664',NULL),('pbkdf2_sha256$1000000$GwfVRc1PCygB8oLSDNtMiQ$YZG7MJ9JBnjhYNzJ8qsXFetcUUFvhcH6gABpMyms7Vc=',185,'Lebon','david93@example.net','patient',1,0,0,'2025-12-27 04:08:53.906038',NULL),('pbkdf2_sha256$1000000$rq02njmKBCXvBtN62bI2Qx$5P3aBqZnypf/HBfOOc5obVJJCDkMm/kRM+bqr4Jz6k4=',186,'Lévêque','georges24@example.com','patient',1,0,0,'2025-12-27 04:08:54.105005',NULL),('pbkdf2_sha256$1000000$5bAga3hrc58um6CRmeai1j$6E+c0ejUmfw7Oj7tHihP2KvlUekC2A/ISLvfok/p0Ag=',187,'Potier','drocher@example.com','patient',1,0,0,'2025-12-27 04:08:54.248961',NULL),('pbkdf2_sha256$1000000$lu3XR571M60hpqGjYMj7uk$N5DbqMaphXXkz+yCeKneyC0WWC3ArkKe/zgZzvtiDgE=',188,'Guillot','margaud21@example.com','patient',1,0,0,'2025-12-27 04:08:54.371695',NULL),('pbkdf2_sha256$1000000$3EhspWdUZQHoXmJguL4SFy$2IWFa6W98/A/4pD/vU79thOFK+oCwNCNvF6nzftJyLM=',189,'Charles','marthe63@example.net','patient',1,0,0,'2025-12-27 04:08:54.495527',NULL),('pbkdf2_sha256$1000000$yph4GM2mN7arA7YIDK231F$OGrzeFY0ipri01nxY+GiOSOBBhJrfqbkUNzazl0yYM4=',190,'Étienne','bertrand94@example.com','patient',1,0,0,'2025-12-27 04:08:54.617154',NULL),('pbkdf2_sha256$1000000$WSl82quA29hyKAYlGFQHNZ$Kc8D9PeRFftgzR2MD5dtvnyOdmyfNAknNpcMW8mviRo=',191,'Bourdon','duhamelsophie@example.net','patient',1,0,0,'2025-12-27 04:08:54.737453',NULL),('pbkdf2_sha256$1000000$2yAAKmSq1QcUo73jj2pfFl$TACKalxyRN2NFIlHANfuJwwza5u1U+JgDPqKYWgV+YI=',192,'Aubert','luc33@example.org','patient',1,0,0,'2025-12-27 04:08:54.870115',NULL),('pbkdf2_sha256$1000000$euBIqnyaqnQaxlEsHRBZXF$GTeI7t1WTTcqLMmtuZibLc/gjjXQuLCZXz2CRsREH6g=',193,'Leblanc','pmartin@example.net','patient',1,0,0,'2025-12-27 04:08:54.996491',NULL),('pbkdf2_sha256$1000000$C14zzdj4E0E16yv85zTLhk$GAPTwTtrdK22MAOhtrJ4mhFKZcuQbVjP1iL4ZjgYWAU=',194,'Toussaint','aimeeguerin@example.net','patient',1,0,0,'2025-12-27 04:08:55.116339',NULL),('pbkdf2_sha256$1000000$9GXU6j62FVRa9TrTVVrWpz$pJ/Dzbzi5dhA+1jKxtjXgXf7pZA1xjUk9FvFkvVgVGY=',195,'Denis','thereselemonnier@example.net','patient',1,0,0,'2025-12-27 04:08:55.233272',NULL),('pbkdf2_sha256$1000000$1IpCyly2za8UR4sQbuxD41$lWYqDxzdvS824iFxEWG93WmdIoS0Wfb4rUN0ktmv34o=',196,'Roche','dominiquemunoz@example.net','patient',1,0,0,'2025-12-27 04:08:55.353196',NULL),('pbkdf2_sha256$1000000$XH53bEkzHmfava5gQDiTj4$X4edtVeVnvHhcWE9FObarRhGjQVBve6wIxCKrg1Zy+o=',197,'Robert','aimeevincent@example.org','patient',1,0,0,'2025-12-27 04:08:55.474190',NULL),('pbkdf2_sha256$1000000$JQZrzaICdEzIh9u4vvgxil$ScsJ4JTVff5FeL18vtULXvKDASP9qiZKWfW0jD/JSy8=',198,'Bouvet','charlesdiane@example.net','patient',1,0,0,'2025-12-27 04:08:55.589488',NULL),('pbkdf2_sha256$1000000$AbDHKN6FhZhs2dRwY4kRwA$X4b/A2sXGEgnD62WleM6ihocbs0f3+1LVBjgp0LTJ5Y=',199,'Marchal','suzanneduhamel@example.net','patient',1,0,0,'2025-12-27 04:08:55.705166',NULL),('pbkdf2_sha256$1000000$Sl5WRHPze7iP6kBDW3FTA0$iTuYnW4HWTJBUVbio7gTVF+LWC7OCs0X5EfnO1F41dc=',200,'Hubert','adrienne07@example.com','patient',1,0,0,'2025-12-27 04:08:55.822569',NULL),('pbkdf2_sha256$1000000$MOuhOGaWer1iFAAHFOVaVn$ugfqjB0rf0s4JQjwt8i3gqEHJRQxnxnnA5NOmvvXUHw=',201,'Lambert','martinedijoux@example.net','patient',1,0,0,'2025-12-27 04:08:55.943464',NULL),('pbkdf2_sha256$1000000$pxrmueFip1xresb4fRq4CB$zY0FdK+74CV/dSXivF58WNVCza+uB5k0vl3rto/kGTw=',202,'Descamps','williamchretien@example.org','patient',1,0,0,'2025-12-27 04:08:56.057799',NULL),('pbkdf2_sha256$1000000$YrM9nKWeOAn81SUDZI631I$zdR+AS5vQ2jBVdECQYseUpos24/GzQU17kH6VZd4X9I=',203,'Morvan','frederic21@example.org','patient',1,0,0,'2025-12-27 04:08:56.175468',NULL),('pbkdf2_sha256$1000000$ihAoSzekxK4X61kK8M3gag$qi+d+qu+FHnzJmvHlOk5IyYQty7ihlhTQtOYKfN8bwk=',204,'Cordier','danielstephanie@example.net','patient',1,0,0,'2025-12-27 04:08:56.289121',NULL),('pbkdf2_sha256$1000000$k5k4KTGEszPxskEVGUr4De$JZfD29nIsj3v3WTOVMOlv2uL17Qb+bB9/f5bEi7GMTo=',205,'Pierre','julien85@example.net','patient',1,0,0,'2025-12-27 04:08:56.403514',NULL),('pbkdf2_sha256$1000000$hZOS8bGo5TWLoHeAH4KaIQ$zq/BwdXAWLcdxdZEMu+uAFTxV7eyEXtmv/ybFXqp9jY=',206,'Cordier','martinezalfred@example.org','patient',1,0,0,'2025-12-27 04:08:56.517557',NULL),('pbkdf2_sha256$1000000$man3DgPJZrpORyPPOxgIr0$jz/YP8sLhS/cOpl6w5qP35yg7a+mSSJbcYtABk0BMxA=',207,'Martel','perriercharles@example.org','patient',1,0,0,'2025-12-27 04:08:56.631957',NULL),('pbkdf2_sha256$1000000$2orGWeKIpK75Ot1vjWkU7E$0kE9be/EgfbTI5y8Si5bEzef7e13rUjIbsP75LAgY7A=',208,'Bonneau','charrierlucas@example.net','patient',1,0,0,'2025-12-27 04:08:56.749149',NULL),('pbkdf2_sha256$1000000$kAfSOi8jT1nM1bpZPwizSG$KpP0Jjel5hveLvYJVheDwy0ITi//iNm6Jf8xu6GIMy8=',209,'Perrin','paulette55@example.com','patient',1,0,0,'2025-12-27 04:08:56.865911',NULL),('pbkdf2_sha256$1000000$Pjqf9ZLl0OorM1EtQQMBz2$alYWzyTGYwhKLfTO2n/8c2DDWIkxyRSKA+qs258yPHE=',210,'Traore','fouchergabrielle@example.org','patient',1,0,0,'2025-12-27 04:08:56.982390',NULL),('pbkdf2_sha256$1000000$n7DJoMIUxp9OyWsVoq8TbJ$if8dfHQNxxYrcvJkEpqdEG28K56NOrmEKl+EybrsFZ0=',211,'Charrier','honore83@example.com','patient',1,0,0,'2025-12-27 04:08:57.097957',NULL),('pbkdf2_sha256$1000000$k1ISr6LMIAAjUGupVPT82D$jIkb6VdARkMlxPCkOTtv7QTw/WIz/G9u5fmKUo7edRE=',212,'Mace','hubertfrancoise@example.net','patient',1,0,0,'2025-12-27 04:08:57.213939',NULL),('pbkdf2_sha256$1000000$zLTiG1LeUBKdIRIhgHfF3j$W8lbH7OyusrWlkW3iuX+XZJYxr0/RGqA1jLVGwe60uM=',213,'Roy','vlejeune@example.org','patient',1,0,0,'2025-12-27 04:08:57.331764',NULL),('pbkdf2_sha256$1000000$BBWbRRyNw0aqr19USKUZbf$cRty8XFaDvRUY/4uGh0Yn2Y06rWxoThAoVlu/XnbSSg=',214,'Diallo','francois97@example.org','patient',1,0,0,'2025-12-27 04:08:57.449713',NULL),('pbkdf2_sha256$1000000$zklvqy5Y9wnvXsqOANWN9P$HHU22x+275+Q4ZOAhFNTi3HJn+7kyvUseMLX6IMqR5E=',215,'Giraud','remydelahaye@example.com','patient',1,0,0,'2025-12-27 04:08:57.567527',NULL),('pbkdf2_sha256$1000000$b9TXeY0gXU9Oo7gQFIRoGL$XtFuGVpQmbbwFNwHF49SEP6GqfQSXNnNE8V5fm9YMJM=',216,'Lejeune','aime24@example.net','patient',1,0,0,'2025-12-27 04:08:57.686512',NULL),('pbkdf2_sha256$1000000$auvKxiSVczSdvFU7XMGrRL$ozaKOntRFfArdweF2t/4IyDlAaf5RllDhVSZmdRpu1E=',217,'Adam','colinclaude@example.com','patient',1,0,0,'2025-12-27 04:08:57.805014',NULL),('pbkdf2_sha256$1000000$HurZxPf9PTeH8Bw7qtX6uL$Vx9YtVGZfQJ4wkIONGM0Tz6+gyjfxkzv+VSaUZGd7SE=',218,'Lemaître','denisejacquet@example.com','patient',1,0,0,'2025-12-27 04:08:57.924472',NULL),('pbkdf2_sha256$1000000$KGKe4IJToNlz6IiaWna4KM$hOp8kKySkjIaV12+8Ze/fvStpEg/4qRNY8ZsIg49+wM=',219,'Dufour','dupuypatrick@example.net','patient',1,0,0,'2025-12-27 04:08:58.040880',NULL),('pbkdf2_sha256$1000000$AgHVG5HHt6qbMOFvIM6Ifs$VgMYo2ATgTSy2HutT1xY7Yzqijv7k7stTczyeeTTAEE=',220,'Simon','alexandrietecher@example.com','patient',1,0,0,'2025-12-27 04:08:58.190394',NULL),('pbkdf2_sha256$1000000$7Lz6ELYCberYw1Z5z2EKqG$/jCXufEiFRXeh00ZVViCg1m91r09hSyNvJMR3Xikuds=',221,'Letellier','lcaron@example.net','patient',1,0,0,'2025-12-27 04:08:58.353623',NULL),('pbkdf2_sha256$1000000$AyiFiIdYQQplP2BpVBV6my$NuwpjeOnh3Kqh7Lsy8ZjCQeQ/YlLJmofFe6z6iDOOpc=',222,'Cohen','josephine36@example.net','patient',1,0,0,'2025-12-27 04:08:58.564744',NULL),('pbkdf2_sha256$1000000$rxk6C88XJiyDPrY5Scx9Bf$sTjVjnDqGVhhXif+i6CFUVXhMnLTsrXbWASqp6q/nfk=',223,'Raynaud','cordiergilles@example.org','patient',1,0,0,'2025-12-27 04:08:58.687561',NULL),('pbkdf2_sha256$1000000$xE6bX6fSu03qantKKf1WAd$8kRkkmvPAR8SBojsoT1aEBywXCr0xox4iVGjtx+du6A=',224,'Roche','josephinelefevre@example.org','patient',1,0,0,'2025-12-27 04:08:58.806689',NULL),('pbkdf2_sha256$1000000$mLliQZ7vxrR39XLMFkuP5F$ipKzf9nltJl4R0PJ7Bzo8WLWNV3bvdbv9vF4WFsKlDc=',225,'Leroy','arthur44@example.net','patient',1,0,0,'2025-12-27 04:08:58.924284',NULL),('pbkdf2_sha256$1000000$HuPscFRhKWZG9GxquW96oj$OioS3+Wzslg0IXQeBiIk8doaKfNVjRL4veT6Q6LF09Y=',226,'Étienne','uguillou@example.org','patient',1,0,0,'2025-12-27 04:08:59.042029',NULL),('pbkdf2_sha256$1000000$B64wbdoX4Ie3UG7cNimEhm$/Y7X+9QwahrhOaZtARFG8GNMcpZMuauJIoDgCXuENuM=',227,'Lagarde','ilemoine@example.net','patient',1,0,0,'2025-12-27 04:08:59.213081',NULL),('pbkdf2_sha256$1000000$lQhBnxsoct7UKfMwgrFmxA$NMBoZIt8J4fMtPE5O0LxLj2rn4n+Sn6tZVvXwwBGo40=',228,'Potier','emilieferreira@example.org','patient',1,0,0,'2025-12-27 04:08:59.362132',NULL),('pbkdf2_sha256$1000000$vfRr1TmnoyfLhqKMPfoCY9$nxRgnH+qk7bF/cO3M2a2NyuVTq5EGQjbjWvSqM6aSS0=',229,'Marie Diop','marie.diop@pharma.sn','employe_pharmacie',1,0,0,'2026-01-08 01:50:06.733903',NULL),('pbkdf2_sha256$1000000$13NrWnKbQPIswzq6YdR839$JDynbAX0nyLJncU2sAywwXt+evWrBoEPaBaW6kOiUsg=',230,'Test Employé','test.employe@pharma.sn','employe_pharmacie',1,0,0,'2026-01-08 02:19:32.979936',NULL),('pbkdf2_sha256$1000000$W1DN3wPtrlVvp2W8HlrNUx$16Nh8hZSNM3RpCv8kofoNAvCznO/aUs72lG3pOwsa/o=',231,'Employé Complet','employe.complet@pharma.sn','employe_pharmacie',1,0,0,'2026-01-08 02:38:24.262161',NULL),('pbkdf2_sha256$1000000$XunwDNwmUzulbSBHbw7mCJ$rhJL//MSKaSKen0TtcM140ofocyzganNJ8S5vJk6HeI=',232,'Mamadou Kouma','k.moh9315@gmail.com','employe_pharmacie',1,0,0,'2026-01-08 02:58:09.984860',NULL),('pbkdf2_sha256$1000000$LAZSdrsgqfhZqRAKAommgv$cK1laYUDUeH6/MIi0ghvkEI5yeujpcgh9zNz6tbUWRU=',233,'hamala Diarra','hamala@gmail.com','employe_pharmacie',1,0,0,'2026-01-08 03:09:50.767204',NULL),('pbkdf2_sha256$1000000$Hy6PXOaovUQMxQWXn1W92n$Q/RSj5kQT7QP6Mx3XlNfopHJfkWse7VHtTI3cSMjWEE=',234,'Arouna Dembele','arouna@gmail.com','employe_pharmacie',1,0,0,'2026-01-11 22:13:27.056128',NULL),('pbkdf2_sha256$1000000$UPVskylt97S7D445nk1Nkj$KD+usR61+4gQDfQhNsqwDYspmv3t4MyMxc55b2Nu61I=',235,'Test','test@esora.com','patient',1,0,0,'2026-02-03 23:20:02.659829',NULL),('pbkdf2_sha256$1000000$GNrHyLcqKdJB2PaeKgmBld$6ANXG7/HqIjrY+NVBC0YV8arwQ3mm4ndKJSbA1Z4ysQ=',236,'Admin Hôpital de Test Auto','admin.testauto001@hôpitaldetestauto.sn','admin_hopital',1,0,0,'2026-02-05 08:00:22.632978',NULL),('pbkdf2_sha256$1000000$nGtYdJTh9GjG86M6B026gQ$niuxNbgROKitgwndNNFrm+1aNMVtMDg0TbrC1wQxbqs=',237,'Admin Hôpital Général de Dakar','admin.hgd001@hopitalgeneraldedakar.sn','admin_hopital',1,0,0,'2026-02-05 08:02:01.275410',NULL),('pbkdf2_sha256$1000000$SmeNI5kqy4qmJmST8UrKIb$axBEc542c2PvPgmjs41xzXc6oWCgK9+4ERjn5LXv3Y8=',238,'Admin centre de lafiabougou','admin.cla0234@centredelafiabougou.sn','admin_hopital',1,0,0,'2026-02-05 08:06:58.185707',NULL),('pbkdf2_sha256$1000000$JWpMQNLovu3nLrGD39S5Kl$3ie/EmtF+qsCB4xWbkqi2ArMkv6PiaJvVkdfDXBlabU=',239,'Admin Hôpital Lafia','admin.lafia@lafia.com','admin_hopital',1,0,0,'2026-02-05 08:12:33.066720',NULL),('pbkdf2_sha256$1000000$uJBgIq1mrGAKfYo7CjIhzE$VnR+8B1rve1ZCF4tU6h8dV973Xo2tRotCuSM1qSqXjU=',240,'Admin Hôpital de Test Final 2','contact@hopital-test.sn','admin_hopital',1,0,0,'2026-02-05 15:22:21.381591',NULL),('pbkdf2_sha256$1000000$fCYQJ4wmRVYN6MRpGbbkkh$rJcejSpOqAOW4VJm3t4/AQCEh8IjYE6Jg46CgzBDgiE=',241,'djibril traore','djibril@gmail.com','employe_pharmacie',1,0,0,'2026-02-13 23:21:08.556331',NULL),('pbkdf2_sha256$1000000$VdscRI4LEUiwl1uVxfEIeZ$uY+eZdmOQ/5yPh7TccZwk6hdER0A5UfsuKtZbNHQXRs=',242,'Baba','baba@gmail.com','employe_pharmacie',1,0,0,'2026-02-13 23:22:15.189851',NULL),('pbkdf2_sha256$1000000$8QLnrCV5jl4eVgxZHkUJFJ$IX81zM40cO72abvg6dwIBMkWjKg4mymYKjJz2dLBc5g=',243,'SODIPHARM','sodipharm@gmail.com','fournisseur',1,0,0,'2026-02-15 21:30:29.357531',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_groups`
--

DROP TABLE IF EXISTS `users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_user_id_group_id_fc7788e8_uniq` (`user_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_groups`
--

LOCK TABLES `users_groups` WRITE;
/*!40000 ALTER TABLE `users_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_permissions`
--

DROP TABLE IF EXISTS `users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` (`user_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_permissions`
--

LOCK TABLES `users_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `values`
--

DROP TABLE IF EXISTS `values`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `values` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titre` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `icone` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ordre` int NOT NULL,
  `landing_page_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `values_landing_page_id_c3a5e064_fk_landing_page_content_id` (`landing_page_id`),
  CONSTRAINT `values_landing_page_id_c3a5e064_fk_landing_page_content_id` FOREIGN KEY (`landing_page_id`) REFERENCES `landing_page_content` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `values`
--

LOCK TABLES `values` WRITE;
/*!40000 ALTER TABLE `values` DISABLE KEYS */;
INSERT INTO `values` VALUES (17,'Excellence','Nous visons l\'excellence dans tous nos services','Award',0,1),(18,'Compassion','Nous traitons chaque patient avec empathie','Heart',1,1),(19,'Innovation','Nous adoptons les dernières technologies','Lightbulb',2,1),(20,'Intégrité','Nous agissons avec transparence et honnêteté','Shield',3,1);
/*!40000 ALTER TABLE `values` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventes_pharmacies`
--

DROP TABLE IF EXISTS `ventes_pharmacies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventes_pharmacies` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_vente` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom_client` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone_client` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `montant_total` decimal(10,2) NOT NULL,
  `montant_paye` decimal(10,2) NOT NULL,
  `montant_rendu` decimal(10,2) NOT NULL,
  `mode_paiement` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reference_paiement` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prescription_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_vente` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `pharmacie_id` bigint NOT NULL,
  `vendeur_id` bigint NOT NULL,
  `annulee` tinyint(1) NOT NULL,
  `motif_annulation` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_annulation` datetime(6) DEFAULT NULL,
  `annulee_par_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_vente` (`numero_vente`),
  KEY `ventes_phar_numero__02bb7e_idx` (`numero_vente`),
  KEY `ventes_phar_pharmac_16a21a_idx` (`pharmacie_id`,`date_vente`),
  KEY `ventes_phar_vendeur_89ac58_idx` (`vendeur_id`,`date_vente`),
  KEY `ventes_phar_mode_pa_e1e4ef_idx` (`mode_paiement`),
  KEY `ventes_pharmacies_annulee_par_id_f203c510_fk_users_id` (`annulee_par_id`),
  CONSTRAINT `ventes_pharmacies_annulee_par_id_f203c510_fk_users_id` FOREIGN KEY (`annulee_par_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ventes_pharmacies_pharmacie_id_b3e597d0_fk_pharmacies_id` FOREIGN KEY (`pharmacie_id`) REFERENCES `pharmacies` (`id`),
  CONSTRAINT `ventes_pharmacies_vendeur_id_3d5ab52d_fk_users_id` FOREIGN KEY (`vendeur_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventes_pharmacies`
--

LOCK TABLES `ventes_pharmacies` WRITE;
/*!40000 ALTER TABLE `ventes_pharmacies` DISABLE KEYS */;
INSERT INTO `ventes_pharmacies` VALUES (3,'VTE86663349','Test Client 2','123456789',992.25,1000.00,7.75,'especes','','','Test vente 2','2026-01-07 00:42:43.689748','2026-01-07 00:42:43.690383','2026-01-07 00:42:43.707037',11,169,0,'',NULL,NULL),(4,'VTE80437892','Client Test Revenus','777123456',1885.28,500.00,0.00,'especes','','','Test vente pour revenus','2026-01-07 00:58:49.774736','2026-01-07 00:58:49.775325','2026-01-07 00:58:49.802681',11,169,0,'',NULL,NULL),(5,'VTE15405316','','',1407.31,1408.00,0.69,'especes','','','','2026-01-07 01:07:48.461320','2026-01-07 01:07:48.461439','2026-01-07 01:07:48.503748',11,169,0,'',NULL,NULL),(6,'VTE05278373','','',2399.56,20000.00,17600.44,'especes','','','','2026-01-07 22:22:54.102343','2026-01-07 22:22:54.102358','2026-01-07 22:22:54.116343',11,169,0,'',NULL,NULL),(8,'VTE72262357','Test Client Vendeur','',1500.00,1500.00,0.00,'especes','','','Vente test avec vendeur automatique','2026-01-08 02:02:50.709255','2026-01-08 02:02:50.709399','2026-02-13 20:46:07.511658',11,169,1,'hj','2026-02-13 20:46:07.511545',234),(9,'VTE11094461','Client Employé','',750.00,800.00,50.00,'especes','','','Vente effectuée par employé Marie','2026-01-08 02:05:45.414820','2026-01-08 02:05:45.414860','2026-02-13 20:45:38.900824',11,229,1,'tromperie','2026-02-13 20:45:38.900468',234),(10,'VTE50945957','','',2814.62,3000.00,185.38,'especes','','','','2026-01-11 22:07:59.890838','2026-01-11 22:07:59.890901','2026-02-13 20:41:51.813021',11,169,1,'dd','2026-02-13 20:41:51.812622',234),(11,'VTE99916891','','',4221.93,5000.00,778.07,'especes','','','','2026-01-26 18:12:19.208573','2026-01-26 18:12:19.208596','2026-02-13 20:41:10.442509',11,169,1,'ddf','2026-02-13 20:41:10.442079',234),(12,'VTE50004580','','',998.59,1000.00,1.41,'especes','','','','2026-02-12 00:14:48.420478','2026-02-12 00:14:48.420506','2026-02-12 00:14:48.462962',12,170,0,'',NULL,NULL);
/*!40000 ALTER TABLE `ventes_pharmacies` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-15 21:56:03
