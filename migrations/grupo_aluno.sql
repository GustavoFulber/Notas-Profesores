USE calculaNota;

CREATE TABLE IF NOT exists `grupo` (
  `idgrupo` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(70) DEFAULT NULL,
  `idmateria` int DEFAULT NULL,
  PRIMARY KEY (`idgrupo`),
  KEY `idmateria_idx` (`idmateria`),
  CONSTRAINT `idmateria` FOREIGN KEY (`idmateria`) REFERENCES `materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
