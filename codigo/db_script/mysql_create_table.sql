CREATE DATABASE  IF NOT EXISTS `academia_apostas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `academia_apostas`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: academia_apostas
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `analise_gols`
--

DROP TABLE IF EXISTS `analise_gols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `analise_gols` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` datetime NOT NULL,
  `campeonato` varchar(45) NOT NULL,
  `time_home` varchar(45) NOT NULL,
  `time_away` varchar(45) NOT NULL,
  `url` varchar(200) NOT NULL,
  `HT` int DEFAULT NULL COMMENT 'Soma de gols no HT contando ultimos 10 jogos do mandante jogando em casa e do visitante jogando fora de casa',
  `FT` int DEFAULT NULL COMMENT 'Soma de gols no FT contando ultimos 10 jogos do mandante jogando em casa e do visitante jogando fora de casa',
  `0 - 15` int DEFAULT NULL,
  `15 - 30` int DEFAULT NULL,
  `30 - 45` int DEFAULT NULL,
  `45 - 60` int DEFAULT NULL,
  `60 - 75` int DEFAULT NULL,
  `75 - 90` int DEFAULT NULL,
  `FM 0 - 15` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FM 15 - 30` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FM 30 - 45` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FM 45 - 60` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FM 60 - 75` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FM 75 - 90` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SM 0 - 15` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SM 15 - 30` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SM 30 - 45` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SM 45 - 60` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SM 60 - 75` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SM 75 - 90` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FV 0 - 15` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FV 15 - 30` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FV 30 - 45` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FV 45 - 60` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FV 60 - 75` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `FV 75 - 90` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SV 0 - 15` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SV 15 - 30` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SV 30 - 45` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SV 45 - 60` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SV 60 - 75` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  `SV 75 - 90` int DEFAULT NULL COMMENT 'FM = Feitos pelo mandante\nSM = Sofridos pelo mandante\n\nFV = Feitos pelo visitante\nSV = Sofridos pelo visitante',
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_UNIQUE` (`url`)
)