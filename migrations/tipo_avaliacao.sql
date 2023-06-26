USE calculaNota;

CREATE TABLE IF NOT exists `tipo_avaliacao` (
  `idtipo_avaliacao` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtipo_avaliacao`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
