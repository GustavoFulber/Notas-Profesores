USE calculaNota;

CREATE TABLE IF NOT exists `materia` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) DEFAULT NULL,
  `idresponsavel` int DEFAULT NULL,
  `idturma` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idresponsavel_idx` (`idresponsavel`),
  KEY `idturma_idx` (`idturma`),
  CONSTRAINT `idresponsavel` FOREIGN KEY (`idresponsavel`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `idturma` FOREIGN KEY (`idturma`) REFERENCES `turma` (`idturma`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
