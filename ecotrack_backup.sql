-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: ecotrack_db
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `accounts_customuser`
--

DROP TABLE IF EXISTS `accounts_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `zone_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser`
--

LOCK TABLES `accounts_customuser` WRITE;
/*!40000 ALTER TABLE `accounts_customuser` DISABLE KEYS */;
INSERT INTO `accounts_customuser` VALUES (1,'pbkdf2_sha256$870000$ykzKBUdDM6KnHu2LRUgS94$dTq/1n+Sr8lxC/susjQsDcBfLmGJCR3FCTvzHffi4Rc=','2025-08-24 02:43:24.343347',1,'admin@gmail.com','Admin',NULL,'','admin',1,1,'2025-08-23 18:25:01.405470',NULL),(2,'pbkdf2_sha256$870000$DXkngruZrlcTorzVWeFhuO$SE95RVprjjav4R8yMurgwJBTQUOvFb8ePQ7TNN8D8WA=',NULL,0,'collector@gmail.com','Collector Ecotrack ','7654321890','','collector',1,0,'2025-08-23 18:42:25.116152','Kottayam'),(3,'pbkdf2_sha256$870000$qhADLARhEzdIlhk54wfoSQ$z9IP6ho3iageqkLR+kiaFNdzuFf7aENghwyzmxWU+PI=',NULL,1,'newuser@gmail.com','New Admin',NULL,'','admin',1,1,'2025-08-24 04:20:06.310288',NULL);
/*!40000 ALTER TABLE `accounts_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_groups`
--

DROP TABLE IF EXISTS `accounts_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq` (`customuser_id`,`group_id`),
  KEY `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_customuser__customuser_id_bc55088e_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_groups`
--

LOCK TABLES `accounts_customuser_groups` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_user_permissions`
--

DROP TABLE IF EXISTS `accounts_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_user_customuser_id_permission_9632a709_uniq` (`customuser_id`,`permission_id`),
  KEY `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_customuser__customuser_id_0deaefae_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_user_permissions`
--

LOCK TABLES `accounts_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add custom user',6,'add_customuser'),(22,'Can change custom user',6,'change_customuser'),(23,'Can delete custom user',6,'delete_customuser'),(24,'Can view custom user',6,'view_customuser'),(25,'Can add pickup request',7,'add_pickuprequest'),(26,'Can change pickup request',7,'change_pickuprequest'),(27,'Can delete pickup request',7,'delete_pickuprequest'),(28,'Can view pickup request',7,'view_pickuprequest'),(29,'Can add complaint',8,'add_complaint'),(30,'Can change complaint',8,'change_complaint'),(31,'Can delete complaint',8,'delete_complaint'),(32,'Can view complaint',8,'view_complaint'),(33,'Can add notification',9,'add_notification'),(34,'Can change notification',9,'change_notification'),(35,'Can delete notification',9,'delete_notification'),(36,'Can view notification',9,'view_notification'),(37,'Can add leave request',10,'add_leaverequest'),(38,'Can change leave request',10,'change_leaverequest'),(39,'Can delete leave request',10,'delete_leaverequest'),(40,'Can view leave request',10,'view_leaverequest'),(41,'Can add collector',11,'add_collector'),(42,'Can change collector',11,'change_collector'),(43,'Can delete collector',11,'delete_collector'),(44,'Can view collector',11,'view_collector'),(45,'Can add zone',12,'add_zone'),(46,'Can change zone',12,'change_zone'),(47,'Can delete zone',12,'delete_zone'),(48,'Can view zone',12,'view_zone');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','customuser'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(11,'ecotracksys','collector'),(8,'ecotracksys','complaint'),(10,'ecotracksys','leaverequest'),(9,'ecotracksys','notification'),(7,'ecotracksys','pickuprequest'),(12,'ecotracksys','zone'),(5,'sessions','session');
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
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-08-23 18:23:02.632505'),(2,'contenttypes','0002_remove_content_type_name','2025-08-23 18:23:02.768391'),(3,'auth','0001_initial','2025-08-23 18:23:03.164542'),(4,'auth','0002_alter_permission_name_max_length','2025-08-23 18:23:03.261108'),(5,'auth','0003_alter_user_email_max_length','2025-08-23 18:23:03.270018'),(6,'auth','0004_alter_user_username_opts','2025-08-23 18:23:03.281172'),(7,'auth','0005_alter_user_last_login_null','2025-08-23 18:23:03.291507'),(8,'auth','0006_require_contenttypes_0002','2025-08-23 18:23:03.296545'),(9,'auth','0007_alter_validators_add_error_messages','2025-08-23 18:23:03.306131'),(10,'auth','0008_alter_user_username_max_length','2025-08-23 18:23:03.316168'),(11,'auth','0009_alter_user_last_name_max_length','2025-08-23 18:23:03.327839'),(12,'auth','0010_alter_group_name_max_length','2025-08-23 18:23:03.356225'),(13,'auth','0011_update_proxy_permissions','2025-08-23 18:23:03.368490'),(14,'auth','0012_alter_user_first_name_max_length','2025-08-23 18:23:03.380702'),(15,'accounts','0001_initial','2025-08-23 18:23:03.847717'),(16,'accounts','0002_rename_full_name_customuser_name_and_more','2025-08-23 18:23:04.018838'),(17,'accounts','0003_customuser_user_id_customuser_username','2025-08-23 18:23:04.222063'),(18,'accounts','0004_remove_customuser_user_id_remove_customuser_username','2025-08-23 18:23:04.401719'),(19,'accounts','0005_customuser_date_joined','2025-08-23 18:23:04.504250'),(20,'admin','0001_initial','2025-08-23 18:23:04.733292'),(21,'admin','0002_logentry_remove_auto_add','2025-08-23 18:23:04.746533'),(22,'admin','0003_logentry_add_action_flag_choices','2025-08-23 18:23:04.759884'),(23,'core','0001_initial','2025-08-23 18:23:04.796971'),(24,'core','0002_delete_pickuprequest','2025-08-23 18:23:04.821128'),(25,'ecotracksys','0001_initial','2025-08-23 18:23:04.946985'),(26,'ecotracksys','0002_remove_pickuprequest_updated_at_and_more','2025-08-23 18:23:05.529142'),(27,'ecotracksys','0003_complaint','2025-08-23 18:23:05.642892'),(28,'ecotracksys','0004_notification','2025-08-23 18:23:05.760723'),(29,'ecotracksys','0005_leaverequest','2025-08-23 18:23:05.880474'),(30,'ecotracksys','0006_collector','2025-08-23 18:23:05.912229'),(31,'sessions','0001_initial','2025-08-23 18:23:06.039662'),(32,'accounts','0006_customuser_zone','2025-08-23 18:35:04.000803'),(33,'ecotracksys','0007_zone_alter_collector_options_alter_complaint_options_and_more','2025-08-23 19:02:29.787757'),(34,'ecotracksys','0008_remove_zone_location_pickuprequest_lat_and_more','2025-08-24 05:49:03.644399');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('hx7ints4jfjomuwzy0wycbmqja1ync44','.eJxVjM0OwiAQhN-FsyH8bIV69O4zkF0WpGogKe3J-O62SQ86x_m-mbcIuC4lrD3NYWJxEVqcfjvC-Ex1B_zAem8ytrrME8ldkQft8tY4va6H-3dQsJdtDXmgbPwWq1ykhERsjYtALmsLTIB-TEYNkG22aPkMKhrPo8kKQRvx-QLyXjf3:1uq0hY:d7oGMpChzeGfjYze6VRvwzuBLHPtp5n7FEPTNJ_ZsXg','2025-09-07 02:43:24.356555');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecotracksys_collector`
--

DROP TABLE IF EXISTS `ecotracksys_collector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecotracksys_collector` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `zone` varchar(120) NOT NULL,
  `status` varchar(8) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecotracksys_collector`
--

LOCK TABLES `ecotracksys_collector` WRITE;
/*!40000 ALTER TABLE `ecotracksys_collector` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecotracksys_collector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecotracksys_complaint`
--

DROP TABLE IF EXISTS `ecotracksys_complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecotracksys_complaint` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) NOT NULL,
  `complaint_type` varchar(20) NOT NULL,
  `related_pickup_id` bigint DEFAULT NULL,
  `description` longtext NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `date_submitted` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecotracksys_complaint_user_id_51fa33d7_fk_accounts_customuser_id` (`user_id`),
  KEY `ecotracksys_complaint_related_pickup_id_8c564b7a` (`related_pickup_id`),
  CONSTRAINT `ecotracksys_complain_related_pickup_id_8c564b7a_fk_ecotracks` FOREIGN KEY (`related_pickup_id`) REFERENCES `ecotracksys_pickuprequest` (`id`),
  CONSTRAINT `ecotracksys_complaint_user_id_51fa33d7_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecotracksys_complaint`
--

LOCK TABLES `ecotracksys_complaint` WRITE;
/*!40000 ALTER TABLE `ecotracksys_complaint` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecotracksys_complaint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecotracksys_leaverequest`
--

DROP TABLE IF EXISTS `ecotracksys_leaverequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecotracksys_leaverequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `leave_type` varchar(20) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `reason` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `collector_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecotracksys_leavereq_collector_id_a30a04f6_fk_accounts_` (`collector_id`),
  CONSTRAINT `ecotracksys_leavereq_collector_id_a30a04f6_fk_accounts_` FOREIGN KEY (`collector_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecotracksys_leaverequest`
--

LOCK TABLES `ecotracksys_leaverequest` WRITE;
/*!40000 ALTER TABLE `ecotracksys_leaverequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecotracksys_leaverequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecotracksys_notification`
--

DROP TABLE IF EXISTS `ecotracksys_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecotracksys_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `type` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL,
  `is_important` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecotracksys_notifica_user_id_7ee941f4_fk_accounts_` (`user_id`),
  CONSTRAINT `ecotracksys_notifica_user_id_7ee941f4_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecotracksys_notification`
--

LOCK TABLES `ecotracksys_notification` WRITE;
/*!40000 ALTER TABLE `ecotracksys_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecotracksys_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecotracksys_pickuprequest`
--

DROP TABLE IF EXISTS `ecotracksys_pickuprequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecotracksys_pickuprequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` longtext NOT NULL,
  `pickup_date` date NOT NULL,
  `pickup_time` time(6) NOT NULL,
  `waste_type` varchar(20) NOT NULL,
  `special_instructions` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `user_id` bigint NOT NULL,
  `collector_id` bigint DEFAULT NULL,
  `notes` longtext,
  `pickup_time_slot` varchar(20) NOT NULL,
  `quantity` int unsigned NOT NULL,
  `lat` double NOT NULL,
  `lng` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecotracksys_pickupre_user_id_68dbb503_fk_accounts_` (`user_id`),
  KEY `ecotracksys_pickupre_collector_id_87fdfa0b_fk_accounts_` (`collector_id`),
  CONSTRAINT `ecotracksys_pickupre_collector_id_87fdfa0b_fk_accounts_` FOREIGN KEY (`collector_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `ecotracksys_pickupre_user_id_68dbb503_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `ecotracksys_pickuprequest_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecotracksys_pickuprequest`
--

LOCK TABLES `ecotracksys_pickuprequest` WRITE;
/*!40000 ALTER TABLE `ecotracksys_pickuprequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecotracksys_pickuprequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecotracksys_zone`
--

DROP TABLE IF EXISTS `ecotracksys_zone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecotracksys_zone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `collector_id` bigint DEFAULT NULL,
  `lat_max` double NOT NULL,
  `lat_min` double NOT NULL,
  `lng_max` double NOT NULL,
  `lng_min` double NOT NULL,
  `ward` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecotracksys_zone_collector_id_a9f40c69_fk_accounts_customuser_id` (`collector_id`),
  CONSTRAINT `ecotracksys_zone_collector_id_a9f40c69_fk_accounts_customuser_id` FOREIGN KEY (`collector_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecotracksys_zone`
--

LOCK TABLES `ecotracksys_zone` WRITE;
/*!40000 ALTER TABLE `ecotracksys_zone` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecotracksys_zone` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-24 11:43:05
