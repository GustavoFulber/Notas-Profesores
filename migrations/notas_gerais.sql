USE calculaNota;

CREATE TABLE IF NOT exists `notas_gerais` (
  `idnotas_gerais` int NOT NULL AUTO_INCREMENT,
  `avalicao_objetiva` decimal(4,2) DEFAULT NULL,
  `avaliacao_dissertativa` decimal(4,2) DEFAULT NULL,
  `entregas` decimal(4,2) DEFAULT NULL,
  `uas` decimal(4,2) DEFAULT NULL,
  `idmateria` int DEFAULT NULL,
  PRIMARY KEY (`idnotas_gerais`),
  KEY `idmateria_idx` (`idmateria`),
  CONSTRAINT `idmateria3` FOREIGN KEY (`idmateria`) REFERENCES `materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
