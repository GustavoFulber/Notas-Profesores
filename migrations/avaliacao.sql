USE calculaNota;

CREATE TABLE IF NOT exists `avaliacao` (
  `idavaliacao` int NOT NULL AUTO_INCREMENT,
  `completo` tinyint DEFAULT NULL,
  `idmateria` int DEFAULT NULL,
  `idaluno_avaliado` int DEFAULT NULL,
  `idaluno_realizando` int DEFAULT NULL,
  PRIMARY KEY (`idavaliacao`),
  KEY `idaluno_realizando_idx` (`idaluno_realizando`),
  KEY `idaluno_avaliado_idx` (`idaluno_avaliado`),
  KEY `idmateria_idx` (`idmateria`),
  CONSTRAINT `idaluno_avaliado` FOREIGN KEY (`idaluno_avaliado`) REFERENCES `aluno` (`idAluno`),
  CONSTRAINT `idaluno_realizando` FOREIGN KEY (`idaluno_realizando`) REFERENCES `aluno` (`idAluno`),
  CONSTRAINT `idmateria1` FOREIGN KEY (`idmateria`) REFERENCES `materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=319 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
