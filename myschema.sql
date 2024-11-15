-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: ZachKesslerProject
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.24.04.2

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
-- Table structure for table `Band`
--

DROP TABLE IF EXISTS `Band`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Band` (
  `BandID` int NOT NULL AUTO_INCREMENT,
  `BandName` varchar(150) NOT NULL,
  `YearFormed` year DEFAULT NULL,
  `OriginCity` varchar(150) DEFAULT NULL,
  `OriginState` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`BandID`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Band`
--

LOCK TABLES `Band` WRITE;
/*!40000 ALTER TABLE `Band` DISABLE KEYS */;
INSERT INTO `Band` VALUES (1,'Umphrey\'s Mcgee',1997,'South Bend','Indiana'),(2,'King Gizzard and the Lizard Wizard',2010,'Melbourne','Victoria'),(3,'The Smashing Pumpkins',1988,'Chicago','Illinois'),(4,'The Murlocs',2010,'Melbourne','Victoria'),(5,'Tenacious D',1994,'Los Angeles','California'),(34,'Cake',1991,'Sacramento','California');
/*!40000 ALTER TABLE `Band` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `BandPerson`
--

DROP TABLE IF EXISTS `BandPerson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `BandPerson` (
  `BandID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(150) DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `RoleInBand` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`BandID`),
  CONSTRAINT `BandPerson_ibfk_1` FOREIGN KEY (`BandID`) REFERENCES `Band` (`BandID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BandPerson`
--

LOCK TABLES `BandPerson` WRITE;
/*!40000 ALTER TABLE `BandPerson` DISABLE KEYS */;
INSERT INTO `BandPerson` VALUES (1,'Jake Cinninger','1975-12-16','Lead Guitar'),(2,'Ambrose Kenny-Smith','1992-07-19','Harmonica'),(3,'Billy Corgan','1967-03-17','Front Man'),(4,'Ambrose Kenny-Smith','1992-07-19','Front Man');
/*!40000 ALTER TABLE `BandPerson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `KeySigniture`
--

DROP TABLE IF EXISTS `KeySigniture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `KeySigniture` (
  `KeySignitureID` int NOT NULL,
  `Tonic` varchar(7) DEFAULT NULL,
  `MajorMinor` enum('Major','Minor') DEFAULT NULL,
  `CircleOfFifthsPosition` smallint DEFAULT NULL,
  PRIMARY KEY (`KeySignitureID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `KeySigniture`
--

LOCK TABLES `KeySigniture` WRITE;
/*!40000 ALTER TABLE `KeySigniture` DISABLE KEYS */;
INSERT INTO `KeySigniture` VALUES (1,'B','Minor',6),(2,'E','Minor',5),(3,'C','Major',1),(4,'G','Minor',2);
/*!40000 ALTER TABLE `KeySigniture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LivePerformance`
--

DROP TABLE IF EXISTS `LivePerformance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LivePerformance` (
  `PerformanceID` int NOT NULL,
  `Venue` varchar(150) DEFAULT NULL,
  `IndoorOutdoor` enum('Indoor','Outdoor') DEFAULT NULL,
  `AppearanceAtVenue` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`PerformanceID`),
  CONSTRAINT `LivePerformance_ibfk_1` FOREIGN KEY (`PerformanceID`) REFERENCES `Performance` (`PerformanceID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LivePerformance`
--

LOCK TABLES `LivePerformance` WRITE;
/*!40000 ALTER TABLE `LivePerformance` DISABLE KEYS */;
INSERT INTO `LivePerformance` VALUES (2,'Red Rocks Amphitheater','Outdoor','First'),(3,'The Wilma Theater','Indoor','Eighth');
/*!40000 ALTER TABLE `LivePerformance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Performance`
--

DROP TABLE IF EXISTS `Performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Performance` (
  `PerformanceID` int NOT NULL,
  `BandID` int DEFAULT NULL,
  `PerformanceDate` date DEFAULT NULL,
  `Length` time DEFAULT NULL,
  `IncludesNonBandPerson` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`PerformanceID`),
  KEY `BandID` (`BandID`),
  CONSTRAINT `Performance_ibfk_1` FOREIGN KEY (`BandID`) REFERENCES `Band` (`BandID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Performance`
--

LOCK TABLES `Performance` WRITE;
/*!40000 ALTER TABLE `Performance` DISABLE KEYS */;
INSERT INTO `Performance` VALUES (1,1,'2007-04-03','00:05:50',1),(2,2,'2022-10-10','00:01:54',1),(3,1,'2017-03-04','00:04:34',0),(4,3,'1994-10-04','00:03:11',0);
/*!40000 ALTER TABLE `Performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PerformanceSong`
--

DROP TABLE IF EXISTS `PerformanceSong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PerformanceSong` (
  `PerformanceID` int NOT NULL,
  `SongID` int NOT NULL,
  PRIMARY KEY (`PerformanceID`,`SongID`),
  KEY `SongID` (`SongID`),
  CONSTRAINT `PerformanceSong_ibfk_1` FOREIGN KEY (`PerformanceID`) REFERENCES `Performance` (`PerformanceID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `PerformanceSong_ibfk_2` FOREIGN KEY (`SongID`) REFERENCES `Song` (`SongID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PerformanceSong`
--

LOCK TABLES `PerformanceSong` WRITE;
/*!40000 ALTER TABLE `PerformanceSong` DISABLE KEYS */;
INSERT INTO `PerformanceSong` VALUES (1,1),(2,2),(3,3),(4,4);
/*!40000 ALTER TABLE `PerformanceSong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Song`
--

DROP TABLE IF EXISTS `Song`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Song` (
  `SongID` int NOT NULL AUTO_INCREMENT,
  `Composer` varchar(150) DEFAULT NULL,
  `Title` varchar(150) DEFAULT NULL,
  `Album` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`SongID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Song`
--

LOCK TABLES `Song` WRITE;
/*!40000 ALTER TABLE `Song` DISABLE KEYS */;
INSERT INTO `Song` VALUES (1,'Umphrey\'s Mcgee','The Bottom Half','The Bottom Half'),(2,'King Gizzard and the Lizard Wizard','The Reticent Racounteur','Murder of the Universe'),(3,'Tenacious D','Kielbasa','Tenacious D'),(4,'Stevie Nicks','Landslide','Fleetwood Mac'),(6,'Umphrey\'s Mcgee','Ocean Billy','Safety in Numbers');
/*!40000 ALTER TABLE `Song` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SongKey`
--

DROP TABLE IF EXISTS `SongKey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SongKey` (
  `SongID` int NOT NULL,
  `KeySignitureID` int NOT NULL,
  PRIMARY KEY (`SongID`,`KeySignitureID`),
  KEY `KeySignitureID` (`KeySignitureID`),
  CONSTRAINT `SongKey_ibfk_1` FOREIGN KEY (`SongID`) REFERENCES `Song` (`SongID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `SongKey_ibfk_2` FOREIGN KEY (`KeySignitureID`) REFERENCES `KeySigniture` (`KeySignitureID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SongKey`
--

LOCK TABLES `SongKey` WRITE;
/*!40000 ALTER TABLE `SongKey` DISABLE KEYS */;
INSERT INTO `SongKey` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `SongKey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudioPerformance`
--

DROP TABLE IF EXISTS `StudioPerformance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `StudioPerformance` (
  `PerformanceID` int NOT NULL,
  `RecordLabel` varchar(150) DEFAULT NULL,
  `Description` text,
  `TrackNumberOnAlbum` int DEFAULT NULL,
  PRIMARY KEY (`PerformanceID`),
  CONSTRAINT `StudioPerformance_ibfk_1` FOREIGN KEY (`PerformanceID`) REFERENCES `Performance` (`PerformanceID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudioPerformance`
--

LOCK TABLES `StudioPerformance` WRITE;
/*!40000 ALTER TABLE `StudioPerformance` DISABLE KEYS */;
INSERT INTO `StudioPerformance` VALUES (1,'SCI Fidelity Records','On a Double Album',1),(4,'Virgin Records','On a Compilation Album',9);
/*!40000 ALTER TABLE `StudioPerformance` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-15 21:17:32
