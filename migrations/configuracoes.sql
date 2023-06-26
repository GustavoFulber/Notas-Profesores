USE calculaNota;

CREATE TABLE IF NOT exists `avaliacao_360` (
  `idavaliacao_360` int NOT NULL AUTO_INCREMENT,
  `comunicacao` decimal(4,2) DEFAULT NULL,
  `cognitivo` decimal(4,2) DEFAULT NULL,
  `autogestao` decimal(4,2) DEFAULT NULL,
  `autonomia` decimal(4,2) DEFAULT NULL,
  `protagonismo` decimal(4,2) DEFAULT NULL,
  `interacao` decimal(4,2) DEFAULT NULL,
  `tipo_avaliacao` int DEFAULT NULL,
  `idmateria` int DEFAULT NULL,
  PRIMARY KEY (`idavaliacao_360`),
  KEY `tipo_avaliacao` (`tipo_avaliacao`),
  KEY `idmateria_idx` (`idmateria`),
  CONSTRAINT `avaliacao_360_ibfk_1` FOREIGN KEY (`tipo_avaliacao`) REFERENCES `tipo_avaliacao` (`idtipo_avaliacao`),
  CONSTRAINT `idmateria2` FOREIGN KEY (`idmateria`) REFERENCES `materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
