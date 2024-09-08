-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: truckman
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('61336ea1b06e');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int DEFAULT NULL,
  `content` text NOT NULL,
  `create_date` datetime NOT NULL,
  `user_id` int NOT NULL,
  `modify_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`) ON DELETE CASCADE,
  CONSTRAINT `answer_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `answer_voter`
--

DROP TABLE IF EXISTS `answer_voter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answer_voter` (
  `user_id` int NOT NULL,
  `answer_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`answer_id`),
  KEY `answer_id` (`answer_id`),
  CONSTRAINT `answer_voter_ibfk_1` FOREIGN KEY (`answer_id`) REFERENCES `answer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `answer_voter_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer_voter`
--

LOCK TABLES `answer_voter` WRITE;
/*!40000 ALTER TABLE `answer_voter` DISABLE KEYS */;
/*!40000 ALTER TABLE `answer_voter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `register_date` date NOT NULL,
  `modify_date` datetime DEFAULT NULL,
  `company_class` varchar(1) NOT NULL,
  `business_no` varchar(12) NOT NULL,
  `firm` varchar(32) NOT NULL,
  `president` varchar(16) DEFAULT NULL,
  `zip` varchar(6) DEFAULT NULL,
  `address` varchar(56) DEFAULT NULL,
  `business_status` varchar(16) DEFAULT NULL,
  `business_item` varchar(16) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `cellphone` varchar(13) DEFAULT NULL,
  `tel` varchar(12) DEFAULT NULL,
  `fax` varchar(12) DEFAULT NULL,
  `note` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'2024-07-01',NULL,'P','497-33-01443','부림손수제비칼국수','천관후','','부산 북구 만덕3로 46 ','','','','','','',''),(2,'2024-07-05',NULL,'R','490-45-00811','재유건설','조종윤','','부산광역시 동래구 시실로168번길 6 ','건설업','토목공사','','','','',''),(3,'2024-07-06',NULL,'P','238-88-01714','(주)알베로','박영선','','경남 김해시 대동면 동남로49번길 93-14 ','','','','','','',''),(4,'2024-07-06',NULL,'P','530-31-01372','알베로 베이커리','황현민','','경남 김해시 대동면 동남로49번길 93-14 ','','','','','','',''),(5,'2024-07-09',NULL,'R','610-81-84562','(주)천일특수','안태준','446-32','울산 남구 북부순환도로 17, 1401호 ','운수업','일반운송주선','','','','',''),(6,'2024-07-12',NULL,'R','613-81-25451','백광화물(주)','임봉성','','경남 사천시 사천읍 사천대로 2005 ','운보','화물운송업','bkcsjnaver.com','','055-855-0113','',''),(7,'2024-07-17',NULL,'R','606-81-25133','(주)협성정밀','장병덕','','부산광역시 사상구 학장동 278-11 ','제조','수송용기구','','','','',''),(8,'2024-07-21',NULL,'P','607-13-82405','삼학주유소','나병문','','부산 연제구 월드컵대로 249','','','','','051-505-7090','',''),(9,'2024-07-22',NULL,'R','607-81-25043','(주)부산시멘트','박현국','467-21','부산 강서구 유통단지1로 41 (대저2동) ','제조업','시멘트벽돌','','','055-323-0015','055-323-2734','경남 김해시 상동면 상동로 608-11'),(10,'2024-07-23',NULL,'P','306-92-01066','가덕활어','손병극','','부산 사하구 다대동로 20','','','','','051-263-1274','',''),(11,'2024-07-26',NULL,'R','615-81-75054','삼성그린스톤(주)','김경령','','경남 김해시 상동면 묵방로120번길 29','제조업','콘크리트제품','','','','',''),(12,'2024-07-26',NULL,'P','606-81-39904','삼보1주유소','이만덕','','부산광역시 북구 만덕동 산19-5 ','','','','','051-336-2000','',''),(13,'2024-07-29',NULL,'R','247-88-01421','(주)제이더블유로직스','홍진원','470-31','부산광역시 사상구 강변대로 570','운수','화물운수알선및주선업','','','','',''),(14,'2024-07-29',NULL,'P','607-85-19404','광신석유(주)충렬대로','최우형','','부산광역시 동래구 충렬대로 95 ','','','','','','',''),(15,'2024-08-08',NULL,'R','609-54-60813','팔도물류','정병철','','경남 창원시 의창구 창원대로397번길 8-9 ','운보','운송주선','','','055-276-2424','',''),(16,'2024-08-08',NULL,'R','877-55-00813','인로지스','손민호','','부산광역시 사하구 동매로120','운수','화물운송주선','','','','',''),(17,'2024-08-16',NULL,'P','615-19-42916','대동촌국시','왕금선','','경남 김해시 대동면 동남로49번길 24 ','','','','','055-335-6616','',''),(18,'2024-08-16',NULL,'R','621-04-49827','부산퀵서비스','김대영','','부산 사상구 사상로104번길 10(감전동) ','서비스','퀵서비스','','','','',''),(19,'2024-08-16',NULL,'R','602-81-54295','(주)삼화트랜스포테이션','박배근','489-38','부산광역시 중구 충장대로13번길 17, 4층 ','운송','하역보조','','','051-466-5748','',''),(20,'2024-08-16',NULL,'R','369-87-02612','멀티전기','윤인찬','','부산광역시 강서구 유통단지1로5동 207호 ','','','','','','',''),(21,'2024-08-19',NULL,'R','180-04-01389','태영종합물류','최윤희','467-35','부산광역시 강서구 화전산단5로 117번길 38 ','운수업','화물운송주선','','','','',''),(22,'2024-08-19',NULL,'R','614-87-02318','(주)대양화물','이재빈','467-35','부산광역시 강서구 화전산단5로 117번길 38 ','운수업','운송주선업','','','','',''),(23,'2024-08-21',NULL,'P','554-82-00589','서부산농협 주유소','김금철','','부산광역시 사하구 장평로 177 ','','','','','051-262-0072','',''),(24,'2024-08-23',NULL,'R','615-15-32254','대성통운','김종규','508-01','경남 김해시 생림면 나전리 810-21','서비스','화물주선','','010-6484-2404','055-324-9500','','우편:경남 김해시 생림면 생림대로 503 (나전리)'),(25,'2024-07-01',NULL,'R','615-10-21276','세기가설','김두택','508-07','경남 김해시 대동면 월촌리 274-2','건설업','건설가설재','','010-6611-6052','','',''),(26,'2024-07-01',NULL,'R','621-81-89927','(주)용성디와이디','박성빈','','부산시 수영구 광안해변로 344번길 17-17 ','운수업','화물자동차운송','','','','',''),(27,'2024-07-01',NULL,'R','606-17-71392','삼성화이바','하명찬','618-17','부산광역시 강서구 녹산산업중로167번길 32','','토기, 가정용','','','','',''),(28,'2024-07-01',NULL,'R','606-86-11798','(주)에이탑이엔지','정진철','','부산광역시 강서구 호계로79번길 56','제조','구조금속제품','','','','',''),(29,'2024-07-01',NULL,'R','606-86-06989','(주)엔투로지스틱스','김연란','467-48','부산 강서구 미음산단로 85 (구랑동)','운수업','화물운송주선','n2.2800@daum.net','','','',''),(30,'2024-07-01',NULL,'R','314-81-31696','(주)로지스퀘어','김신배','085-05','서울 금천구 가산디지털2로 123 (가산동, 월드메르디앙2차) ','운수','운송주선','tax@logisquare ','','','',''),(31,'2024-07-01',NULL,'R','606-24-86078','대교종합화물','정화자','','','화물운송','주선','','','','',''),(32,'2024-07-01',NULL,'R','481-11-01427','미래물류','이명화','509-39','경남 김해시 전하로222번길 3-3 (전하동) ','운수업','화물운송주선','','','','',''),(33,'2024-07-01',NULL,'R','314-05-30295','믿음운수','이승민','058-38','서울 송파구 충민로 66 (문정동, 가든파이브라이프) 리빙관 9027','운수업','운송주선','redfox205@daum.net','','','',''),(34,'2024-07-01',NULL,'R','602-08-69679','성원종합물류','채길상','490-75','부산 영도구 중복길 276 (신선동2가, 팔공빌라) ','운수업','화물주선업','','','','',''),(35,'2024-07-01',NULL,'R','615-16-13628','에이스물류','최남순','508-08','경남 김해시 대동면 동남로49번길 7-45 (초정리) ','서비스','운송주선','sprintercns1@naver.com','','','',''),(36,'2024-07-01',NULL,'P','638-03-00072','청송보리밥','이지수','','부산 강서구 대저로 57 (대저1동)','','','','','','',''),(37,'2024-07-01',NULL,'P','606-85-18343','(주)우양네트웍스','조영준','','부산시 강서구 공항로 799','','','','','051-941-5188','',''),(38,'2024-07-01',NULL,'P','617-01-88475','공항대로주유소','박비주','','부산광역시 강서구 공항로 1217','','','','','051-973-8122','',''),(39,'2024-07-01',NULL,'P','783-85-01760','우리2주유소','이지훈','','부산광역시 강서구 낙동북로 142','','','','','051-971-5585','',''),(40,'2024-07-06',NULL,'P','510-85-11409','동방석유(주)직영대저','박현병','','부산광역시 낙동북로 209','','','','','051-971-2135','',''),(41,'2024-08-21',NULL,'P','596-36-00128','마당쇠민속보쌈','박균이','','부산광역시 북구 백양대로 1058','','','','','051-341-7852','',''),(42,'2024-07-01',NULL,'P','201-24-70787','노포축산(구포점)','이동진','','','','','','','051-583-3445','',''),(43,'2024-08-09',NULL,'P','622-01-84637','조은낙지','황금영','','부산 강서구 평강로 304','','','','','051-971-8002','','테스트'),(44,'2024-07-17',NULL,'P','606-06-14338','논두렁칼국수','김미영','','','','','','','051-972-7936','',''),(45,'2024-07-29',NULL,'P','606-16-27453','명가밀면','유소정','','부산시 북구 금고대로 303번길 70','','','','','051-335-4604','',''),(46,'2024-07-27',NULL,'P','744-85-01673','하나로마트 부산점','이상문','','부산 북구 금곡도 1874-3','','','','','051-330-9000','',''),(47,'2024-07-01',NULL,'P','239-50-00919','고스고스','박지해','467-02','부산 강서구 공항로 1315 (대저1동)','','','','','','',''),(48,'2024-07-01',NULL,'P','622-82-00048','대저농협 하나로마트','류태윤','467-02','부산 강서구 대저로 229 (대저1동) ','도매','생활용품','','','','',''),(49,'2024-07-01',NULL,'P','606-28-38685','만덕한사랑약국','최주화','466-12','부산 북구 은행나무로 6 (만덕동) ','','','','','','',''),(51,'2024-09-02',NULL,'P','606-24-42522','툇마루','','','부산 북구 금곡대로285번길 81','','','','','','',''),(52,'2024-09-03',NULL,'P','354-92-00426','홍지호치과의원','홍지호','','부산 북구 백양대로 1196','','','','','','','');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cost`
--

DROP TABLE IF EXISTS `cost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cost` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cost_date` date NOT NULL,
  `modify_date` datetime DEFAULT NULL,
  `cost_company` varchar(32) NOT NULL,
  `cost_class` varchar(1) NOT NULL,
  `statement` varchar(32) DEFAULT NULL,
  `payment` varchar(1) NOT NULL,
  `bank_card` varchar(32) DEFAULT NULL,
  `cost_amount` int DEFAULT NULL,
  `memo` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cost`
--

LOCK TABLES `cost` WRITE;
/*!40000 ALTER TABLE `cost` DISABLE KEYS */;
INSERT INTO `cost` VALUES (1,'2024-07-01',NULL,'대저농협 하나로마트','N','맥심','C','농협',11455,''),(2,'2024-07-01',NULL,'청송보리밥','M','중식','C','부산',6364,''),(3,'2024-07-01',NULL,'우리2주유소','D','OK-Oil','C','국민',72727,'1438/55'),(4,'2024-07-01',NULL,'한화손해보험','T','8974 자동차보험','C','농협',812850,'6개월 무이자할부'),(5,'2024-07-02',NULL,'(주)이도','T','BN8000 스피커 교체','C','부산',24700,'택배포함'),(6,'2024-07-04',NULL,'부산개별화물협회','T','8877 정비/633,513   Km ','C','삼성',640819,'타이어2개/5개월'),(7,'2024-07-04',NULL,'만덕한사랑약국','O','당뇨약','C','부산',46900,''),(8,'2024-07-05',NULL,'부림손수제비칼국수','M','중식','C','부산',17273,''),(9,'2024-07-06',NULL,'알베로 베이커리','N','빵','C','농협',21546,''),(10,'2024-07-06',NULL,'(주)알베로','N','가족커피','C','농협',48363,''),(11,'2024-07-07',NULL,'공항대로주유소','G','OK유류','C','우리',81818,'1648/54'),(12,'2024-07-07',NULL,'노포축산(구포점)','F','삼겹살','C','농협',45586,''),(13,'2024-07-08','2024-08-24 07:21:28','동방석유(주)직영대저','D','SK-Oil','C','신한',70000,'1463/52'),(14,'2024-07-09',NULL,'(주)부산정비','T','8877 자동차 정기검사','C','농협',45455,'안개등/후미 반사체'),(15,'2024-07-09',NULL,'청송보리밥','M','중식','C','부산',6364,''),(16,'2024-07-12',NULL,'청송보리밥','M','중식','C','부산',6364,''),(17,'2024-07-12',NULL,'전국통운','T','주차비','C','농협',170000,''),(18,'2024-07-13',NULL,'(주)우양네트웍스','D','S-Oil','C','국민',63636,'1525/46'),(19,'2024-07-15',NULL,'청송보리밥','M','중식','C','농협',6364,''),(20,'2024-07-15',NULL,'대저우체국','O','우표10장','M','',4300,''),(21,'2024-07-15',NULL,'하나로마트 부산점','N','생필품','C','농협',66716,'2개월'),(22,'2024-07-16',NULL,'청송보리밥','M','중식','C','농협',6364,''),(23,'2024-07-17',NULL,'논두렁칼국수','M','칼국수','C','농협',5910,''),(24,'2024-07-18',NULL,'명가밀면','M','밀면','C','농협',15455,'경숙'),(25,'2024-07-19',NULL,'공항대로주유소','G','OK-Oil','C','우리',72727,'1655/48'),(26,'2024-07-20',NULL,'삼학주유소','D','OK-Oil','C','우리',93637,'1508/68'),(27,'2024-07-21',NULL,'가덕활어','N','활어','C','농협',100000,'3개월'),(28,'2024-07-23',NULL,'청송보리밥','M','중식','C','농협',6364,''),(29,'2024-07-25',NULL,'청송보리밥','M','중식','C','농협',6364,''),(30,'2024-07-26',NULL,'삼보1주유소','D','GS 칼텍스','C','삼성',45455,'1519/33'),(31,'2024-07-26',NULL,'청송보리밥','M','중식','C','농협',6364,''),(32,'2024-07-29',NULL,'광신석유(주)충렬대로','D','SK-Oil','C','신한',72727,'1499/53'),(33,'2024-07-29',NULL,'청송보리밥','M','중식','C','농협',6364,''),(34,'2024-07-29',NULL,'명가밀면','M','밀면','C','농협',15455,''),(35,'2024-07-29',NULL,'하나로마트 부산점','N','생활필수품','C','농협',61773,'2개월'),(36,'2024-07-30',NULL,'청송보리밥','M','중식','C','농협',6364,''),(37,'2024-07-31',NULL,'공항대로주유소','G','OK-Oil','C','국민',72727,'1649/48'),(38,'2024-08-01',NULL,'노포축산(구포점)','F','삼겹살 외','C','농협',25597,''),(39,'2024-08-01',NULL,'고스고스','N','가족 커피','C','농협',28638,'본인 생일'),(40,'2024-08-05',NULL,'삼성전자서비스(주)','N','에어컨 냉매 주입','C','농협',90910,'디지털구포센터'),(41,'2024-08-06',NULL,'청송보리밥','M','중식','C','농협',7273,' 08/05 인상'),(42,'2024-08-06',NULL,'만덕한사랑약국','O','본인 당뇨약대','C','농협',39300,''),(43,'2024-08-06',NULL,'(주)우양네트웍스','D','S-Oil','C','국민',63636,'1499/47'),(44,'2024-08-08',NULL,'청송보리밥','M','중식','C','농협',14546,'만수'),(45,'2024-08-09',NULL,'조은낙지','M','중식','C','농협',9091,''),(46,'2024-08-11',NULL,'전국통운','T','주차비','C','농협',170000,''),(47,'2024-08-15',NULL,'대동촌국시','M','국수','C','농협',10909,'경숙'),(48,'2024-08-16',NULL,'공항대로주유소','D','OK-Oil','C','우리',71991,'1475/54'),(49,'2024-08-19',NULL,'청송보리밥','M','중식','C','농협',7273,''),(50,'2024-08-19',NULL,'공항대로주유소','G','OK-Oil','C','국민',72727,'1628/49'),(51,'2024-08-21',NULL,'서부산농협 주유소','D','농협직영','C','신한',71960,'1404/56'),(52,'2024-08-21',NULL,'마당쇠민속보쌈','M','석식','C','농협',27273,'경숙'),(53,'2024-08-21',NULL,'노포축산(구포점)','F','쇠고기외','C','농협',41499,''),(54,'2024-08-23',NULL,'청송보리밥','M','중식','C','농협',7273,''),(55,'2024-08-26',NULL,'청송보리밥','M','중식','C','농협',7273,''),(56,'2024-08-27',NULL,'장자주유소','D','S-Oil','C','국민',63636,'1446/48'),(57,'2024-08-27',NULL,'청송보리밥','M','중식','C','농협',7273,''),(59,'2024-09-03',NULL,'공항대로주유소','G','OK-Oil','C','국민',72727,'1589/50'),(60,'2024-09-02',NULL,'툇마루','M','중식','C','부산',79091,'한나/경숙'),(61,'2024-09-01',NULL,'명가밀면','M','석식','C','부산',15455,'경숙'),(62,'2024-08-29',NULL,'청송보리밥','M','중식','C','농협',7273,''),(63,'2024-09-01',NULL,'하나로마트 부산점','N','생활필수품','C','농협',86154,''),(64,'2024-09-03',NULL,'홍지호치과의원','O','잇몸치료','C','부산',9000,'첫진료'),(65,'2024-09-04',NULL,'청송보리밥','M','중식','C','부산',7273,''),(66,'2024-09-05',NULL,'동방석유(주)직영대저','D','SK-Oil','C','신한',58182,'1404/45');
/*!40000 ALTER TABLE `cost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `create_date` datetime NOT NULL,
  `user_id` int NOT NULL,
  `modify_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,'화물운송 종사자들의 자부심','세상에는 직업의 귀천이 없다고 합니다.\r\n그렇습니다. 우리는 사람답게 살 권리가 있으며, 이러한 인간 존엄과 행복의 권리는 \r\n헌법에도 명시되어 있습ㄴ다.\r\n그러나, 무엇보다 중요한 사실은 우리 모두 스스로 자존감을 지킬 때 비로소 지킬수 \r\n있다고 생각합니다.                        \r\n            ','2024-08-31 21:23:24',1,NULL);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_voter`
--

DROP TABLE IF EXISTS `question_voter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_voter` (
  `user_id` int NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`question_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `question_voter_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`) ON DELETE CASCADE,
  CONSTRAINT `question_voter_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_voter`
--

LOCK TABLES `question_voter` WRITE;
/*!40000 ALTER TABLE `question_voter` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_voter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transport`
--

DROP TABLE IF EXISTS `transport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transport` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trans_date` date DEFAULT NULL,
  `modify_date` datetime DEFAULT NULL,
  `trans_company` varchar(32) DEFAULT NULL,
  `consignor` varchar(32) DEFAULT NULL,
  `load_region` varchar(64) DEFAULT NULL,
  `unload_date` date DEFAULT NULL,
  `consignee` varchar(32) DEFAULT NULL,
  `unload_region` varchar(64) DEFAULT NULL,
  `terms` varchar(2) NOT NULL,
  `trans_amount` int NOT NULL,
  `payment` varchar(1) DEFAULT NULL,
  `trans_set_date` date DEFAULT NULL,
  `brokerage_fee` int DEFAULT NULL,
  `brokerage_date` date DEFAULT NULL,
  `trans_type` varchar(1) NOT NULL,
  `comment` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transport`
--

LOCK TABLES `transport` WRITE;
/*!40000 ALTER TABLE `transport` DISABLE KEYS */;
INSERT INTO `transport` VALUES (1,'2024-07-01',NULL,'에이스물류','동해종합맨홀','경남 김해시 상동면 우계리 847-3','2024-07-01','010-7544-2140','부산 동래구 온천동 269-7','TF',80000,'E','2024-07-02',0,NULL,'N',''),(2,'2024-07-02',NULL,'(주)한길종합화물','서부산동일도기','부산 강서구 GY세라믹','2024-07-02','010-3567-0817','경남 김해시 장유동 843-1','TF',80000,'O','2024-08-10',0,NULL,'N',''),(3,'2024-07-03',NULL,'(주)한길종합화물','그란츠','부산 강서구 BH/GY 세라믹','2024-07-03','010-7501-0914','부산 해운대구 우동 1513','TF',100000,'O','2024-08-10',0,NULL,'N',''),(4,'2024-07-04',NULL,'세기가설','세중조경','경남 김해시 대동면 월촌리','2024-07-04','푸른세상조경','부산 동래구 동래구청','TF',80000,'O','2024-08-23',0,NULL,'N',''),(5,'2024-07-05',NULL,'세기가설','세기가설','경남 김해시 대동면 월촌리','2024-07-05','재유건설','부산 기장군 테크','DF',110000,'E','2024-07-05',0,NULL,'N',''),(6,'2024-07-08',NULL,'대교종합화물','서원유통','경남 김해시 김해대로 2579번길 58','2024-07-08','서원유통 연제점','부산 연제구 연산동','TF',70000,'E','2024-07-12',0,NULL,'N',''),(7,'2024-07-09',NULL,'(주)한길종합화물','범일동 동일도기','경남 김해시 여여세라믹','2024-07-09','010-7599-7155','부산 부산진구 신천대로 215','TF',80000,'O','2024-08-10',0,NULL,'N',''),(8,'2024-07-09','2024-08-23 20:59:10','부산지방화물','(주)용성디와이디','경남 김해시 주촌면 서부로 1474-51','2024-07-09','국양로지텍','부산 남구 신선로 294','CF',90000,'P','2024-07-19',10000,NULL,'N','삼원수출포장'),(9,'2024-07-09',NULL,'(주)천일특수','디에스이','경남 김해시 상동면 상동로 265-23','2024-07-09','진흥테크','부산 사하구 다산로225번길 35','TF',70000,'E','2024-07-16',0,NULL,'N',''),(10,'2024-07-12',NULL,'반도종합화물','라움플러스','부산 강서구 대저2동','2024-07-13','010-3558-5445','부산 연제구 고분로13번길 9','CF',80000,'M','2024-07-14',10000,NULL,'N',''),(11,'2024-07-15',NULL,'(주)트럭인','삼성화이바','부산 강서구 송정동 1522-3','2024-07-16','010-3855-7147','경남 창원시 성산구 대원로93번길 12','CF',140000,'P','2024-07-16',0,NULL,'N',''),(12,'2024-07-17',NULL,'가야로지스틱','(주)협성정밀','부산 사상구 학장동 278-11','2024-07-17','더세이프티(주)','부산 강서구 지사동 산268번지','CP',70000,'P','2024-07-17',10000,NULL,'N',''),(13,'2024-07-19',NULL,'성원종합물류','신동아이엔지','경남 김해시 상동면 매리 607-31','2024-07-19','010-3858-9257','부산 수영구 한바다중학교','TF',90000,'E','2024-08-30',0,NULL,'N',''),(14,'2024-07-22',NULL,'세기가설','세중조경','부산 동래구 동래구청','2024-07-22','세기가설','경남 김해시 대동면 월촌리','TF',80000,'O','2024-08-23',0,NULL,'N','대납'),(15,'2024-07-22',NULL,'세기가설','세기가설','경남 김해시 대동면 월촌리','2024-07-22','권명곤','부산 금정구 부산대학교 지하철4번','TF',70000,'O','2024-08-23',0,NULL,'N','대납'),(16,'2024-07-23',NULL,'세기가설','세기가설','경남 김해시 대동면 월촌리','2024-07-23','정명건설','부산 금정구 내성고등학교','TF',90000,'O','2024-08-23',0,NULL,'N','대납'),(17,'2024-07-23',NULL,'대교종합화물','(주)에이탑이엔지','부산 강서구 죽동동','2024-07-24','010-3654-1518','부산 기장군 철마면 장전리 263번지','CF',90000,'P','2024-07-29',10000,NULL,'N',''),(18,'2024-07-24',NULL,'박병수','동일','부산 북구 만덕동','2024-07-25','010-4544-8398','경남 양산시 물금읍 화합4길 15-18','TF',80000,'M','2024-07-25',0,NULL,'N',''),(19,'2024-07-25',NULL,'세기가설','세기가설','경남 김해시 대동면 월촌리','2024-07-25','정명건설','부산 금정구 내성고등학교','TF',80000,'O','2024-08-23',0,NULL,'N','대납'),(20,'2024-07-26',NULL,'박병수','동일몰딩','부산 북구 만덕동','2024-07-27','010-9665-1901','부산 해운대구 신도중학교','TP',90000,'M','2024-07-26',0,NULL,'N',''),(21,'2024-07-26',NULL,'아줌마화물','삼성그린스톤(주)','경남 김해시 상동면 우계리 110-44','2024-07-27','허세영','경남 김해시 대동면 대동로881번길 36','CF',80000,'P','2024-07-30',12000,NULL,'N',''),(22,'2024-07-26',NULL,'(주)제이더블유로직스','태원정공','부산 강서구 죽동동','2024-07-26','국양로지텍','부산 남구 신선로294','TF',100000,'E','2024-08-29',0,NULL,'N',''),(23,'2024-07-27',NULL,'(주)한길종합화물','범일동 동일도기','부산 강서구 BH세라믹','2024-07-28','010-4591-7119','부산 기장군 정관읍 산단4로 2-69 한국폴리텍대학','TF',100000,'O','2024-08-10',0,NULL,'N',''),(24,'2024-07-29',NULL,'세기가설','권명곤','부산 금정구 부산대학교 지하철역 4번 ','2024-07-29','세기가설','경남 김해시 대동면 월촌리','TF',70000,'O','2024-08-23',0,NULL,'N','대납'),(25,'2024-07-29',NULL,'세기가설','세기가설','경남 김해시 대동면 월촌리','2024-07-29','고려종합상사','부산 해운대구 수영강변대로 93','TF',90000,'O','2024-08-23',0,NULL,'N',' APEC 나루공원 주차장'),(26,'2024-07-30',NULL,'대교종합화물','삼락쇼트산업','경남 김해시 주촌면 망덕리 227번지','2024-07-30','010-35781444','부산 부산진구 연지동 60번지','TF',80000,'E','2024-08-02',0,NULL,'N','국제아트센터'),(27,'2024-07-31',NULL,'부산퀵서비스','동창종합건재','부산 사상구 낙동대로1002번길63','2024-08-01','010-384-4771','부산 수영구 황령산로7번길 78','TF',80000,'P','2024-08-02',0,NULL,'N',''),(28,'2024-08-01',NULL,'세기가설','에스알건설','부산 해운대구 해운대 해수욕장 공영주차장','2024-08-01','세기가설','경남 김해시 대동면 월촌리','TF',90000,'O',NULL,0,NULL,'N','대납'),(29,'2024-08-05',NULL,'믿음운수','유영화학(주)','경남 김해시 분성로569번길 21','2024-08-05','051-647-8405','부산 남구 문현동','TF',110000,'E','2024-08-22',0,NULL,'N',''),(30,'2024-08-07',NULL,'팔도물류','이브이메탈','부산 강서구 평강로249','2024-08-07','제이스펄씨젼','경남 양산시 산막공단북13길 42','TF',70000,'E','2024-08-16',0,NULL,'N',''),(31,'2024-08-08',NULL,'인로지스','(주)아티오','경남 김해시 생림면 생림대로 826-61','2024-08-08','010-3867-6008','부산 북구 화명동','TF',80000,'E','2024-09-03',0,NULL,'N',''),(32,'2024-08-09',NULL,'(주)로지스퀘어','동부산우체국','부산 부산진구 범일동 830-63','2024-08-09','부산우편집중국','부산 강서구 대저1동 1549','TF',80000,'E',NULL,0,NULL,'N',''),(33,'2024-08-09',NULL,'미래물류','쌍용전력','부산 강서구 구량동 1215-2','2024-08-09','쌍용전력','부산 강서구 구량동 1215-2','TF',80000,'E','2024-08-25',0,NULL,'N',''),(34,'2024-08-10',NULL,'세기가설','전결수','부산 수영구 광안동 490-5','2024-08-10','세기가설','경남 김해시 대동면 월촌리','TF',80000,'O',NULL,0,NULL,'N','대납'),(35,'2024-08-10','2024-08-29 22:48:45','세기가설','세기가설','경남 김해시 대동면 월촌리','2024-08-10','청호건설','부산 연제구 연산초등학교','TF',80000,'O',NULL,0,NULL,'N','대납'),(36,'2024-08-16',NULL,'(주)한트럭','멀티전기','부산 강서구 대저2동 5226-2','2024-08-16','010-5220-9111','경남 김해시 주촌면 망덕리 291-1','CP',90000,'P','2024-08-16',15000,NULL,'N','삼화고주파'),(37,'2024-08-16','2024-08-21 04:32:09','(주)삼화트랜스포테이션','영남수출포장','부산 강서구 대저1동 2735','2024-08-16','신국제여객터미널','부산 동구 충장대로 206','TF',80000,'E','2024-09-05',0,NULL,'N','범아상사'),(38,'2024-08-19',NULL,'태영종합물류','대진메탈','경남 김해시 주촌면 내삼리 730-2','2024-08-19','호성정밀','부산 사하구 장림동 442','TF',90000,'E',NULL,0,NULL,'N',''),(39,'2024-08-19',NULL,'(주)대양화물','태진철재','부산 강서구 평강로 355','2024-08-19','대림환경산업','부산 해운대구 해운대구 삼어로 190','TF',60000,'E','2024-08-20',0,NULL,'N',''),(40,'2024-08-21',NULL,'세기가설','강진규','부산 사하구 장림동/효림초등','2024-08-21','세기가설','경남 김해시 대동면 월촌리','TF',90000,'O',NULL,0,NULL,'N','대납'),(41,'2024-08-22',NULL,'(주)엔투로지스틱스','청호전기','부산 강서구 미음동 1536-6','2024-08-22','010-4585-2567','부산 북구 덕천동 361','TF',70000,'E','2024-09-03',0,NULL,'N',''),(42,'2024-08-22',NULL,'윤태열','동하가설','부산 강서구 대저1동 1737','2024-08-22','010-4573-8955','부산 동래구 사직여중','TP',60000,'M','2024-08-22',0,NULL,'N',''),(43,'2024-08-22',NULL,'대교종합화물','(주)부산시멘트','경남 김해시 상동면 상동로 608-11','2024-08-22','010-8535-0700','부산 북구 만덕동/백산초등','CF',90000,'P',NULL,0,NULL,'N',''),(44,'2024-08-23',NULL,'대성통운','010-4190-3443','부산 부산진구 양정동 37-78','2024-08-23','탑우드','경남 김해시 생림면 생림대로 519-44','TF',90000,'E',NULL,0,NULL,'N',''),(45,'2024-07-31','2024-08-23 20:57:22','세기가설','세기가설','경남 김해시 대동면 월촌리','2024-07-31','푸른세상조경','부산광역시 동래구 동래구청','TF',560000,'P','2024-08-23',0,NULL,'V','VAT'),(46,'2024-06-26','2024-08-26 03:44:11','세기가설','희진건설','','2024-06-26','(주)피제이엘','','TF',100000,'M',NULL,0,NULL,'N',''),(47,'2024-08-26','2024-08-27 21:04:27','하우징로지스틱','금빈타일','부산 강서구 대저1동 1827-1','2024-08-27','010-4444-7848','경남 진주시 공군교육사령부','CF',160000,'O','2024-08-27',0,NULL,'N','예가'),(48,'2024-08-27',NULL,'유한종합물류','하나앤스틸','경남 함안군 법수면 강주3길 74','2024-08-27','010-3507-7847','부산 금정구 두실초등앞','TF',100000,'E',NULL,0,NULL,'N',''),(51,'2024-08-28',NULL,'성충현','동일합판목재','강서구 식만로233번길','2024-08-28','010-3911-1807','해운대구 우동 638-1','TP',90000,'M','2024-08-28',10000,'2024-08-28','N',''),(55,'2024-08-30',NULL,'세기가설','세중조경','경남 김해시 대동면 월촌리','2024-08-30','세기가설','경남 김해시 대동면 월촌리','TF',340000,'P',NULL,0,'2024-08-30','V','청구용'),(56,'2024-09-03',NULL,'세기가설','권명곤','부산 기장군 동부산공영주차장','2024-09-03','세기가설','경남 김해시 대동면 월촌리','TF',100000,'O',NULL,0,'2024-09-03','N','대납'),(57,'2024-09-03',NULL,'(주)한길종합화물','범일동 동일도기','부산 강서구 평강','2024-09-04','010-9465-4832','부산 사상구 사상로211번길 52','TF',70000,'O',NULL,0,'2024-09-03','N',''),(58,'2024-09-04','2024-09-04 16:36:38','(주)전국화물','유진하우징','부산 강서구 대저1동','2024-09-05','010-3581-1437','경남 밀양시 초동면 성만남전로 28-29','DF',120000,'O','2024-09-05',0,'2024-09-04','N',''),(59,'2024-09-05',NULL,'세기가설','세기가설','경남 김해시 대동면 월촌리','2024-09-05','김기철','부산 금정구 금성동 398번지','TF',100000,'O',NULL,0,'2024-09-05','N','대납'),(60,'2024-09-05',NULL,'대교종합화물','(주)에이탑이엔지','부산 강서구 죽동동','2024-09-06','010-5680-8404','부산 동래구 부산교육대학교','CF',90000,'P',NULL,0,'2024-09-05','N','');
/*!40000 ALTER TABLE `transport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `register_date` date NOT NULL,
  `modify_date` datetime DEFAULT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(255) NOT NULL,
  `truck_name` varchar(16) DEFAULT NULL,
  `truck_no` varchar(12) NOT NULL,
  `truck_class` varchar(12) DEFAULT NULL,
  `truck_ton` decimal(3,1) NOT NULL,
  `business_no` varchar(12) NOT NULL,
  `company` varchar(32) NOT NULL,
  `member_name` varchar(16) NOT NULL,
  `zip` varchar(6) DEFAULT NULL,
  `address` varchar(56) DEFAULT NULL,
  `business_status` varchar(16) NOT NULL,
  `business_item` varchar(16) NOT NULL,
  `email` varchar(64) DEFAULT NULL,
  `cellphone` varchar(13) NOT NULL,
  `tel` varchar(12) DEFAULT NULL,
  `fax` varchar(12) DEFAULT NULL,
  `bank_name` varchar(24) DEFAULT NULL,
  `bank_no` varchar(24) DEFAULT NULL,
  `bank_account` varchar(16) DEFAULT NULL,
  `description` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'2024-08-20',NULL,'manchu51','scrypt:32768:8:1$v3pnvOUvqfuU4yPE$53061dd84284c1b34d99a629320e6c1990ca8a581e71b800d99d46d811499bce21ed9a70a9c28d4327a7a5761e7f57122103540d2b135e41f94e13d877a8222a','이마이티','부산90바8877','카고',3.5,'605-16-15352','트랜스콜','김영실','466-17','부산광역시 북구 함박봉로 140번길 21','운보','트럭','manchu5104@gmail.com','010-6611-6052','051-332-1128','051-333-1140','농협','','김영실','운영자');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-05 23:35:35
