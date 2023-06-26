USE calculaNota;

CREATE TABLE IF NOT exists `turma_aluno` (
  `idturma_aluno` int NOT NULL AUTO_INCREMENT,
  `idturma` int DEFAULT NULL,
  `idaluno` int DEFAULT NULL,
  PRIMARY KEY (`idturma_aluno`),
  KEY `idturma_idx` (`idturma`),
  KEY `idaluno_idx` (`idaluno`),
  CONSTRAINT `idaluno1` FOREIGN KEY (`idaluno`) REFERENCES `aluno` (`idAluno`),
  CONSTRAINT `idturma1` FOREIGN KEY (`idturma`) REFERENCES `turma` (`idturma`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
