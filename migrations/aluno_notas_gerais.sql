USE calculaNota;

CREATE TABLE IF NOT exists `aluno_notas_gerais` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idAluno` int DEFAULT NULL,
  `idnotas_gerais` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idAluno` (`idAluno`),
  KEY `idnotas_gerais` (`idnotas_gerais`),
  CONSTRAINT `aluno_notas_gerais_ibfk_1` FOREIGN KEY (`idAluno`) REFERENCES `aluno` (`idAluno`),
  CONSTRAINT `aluno_notas_gerais_ibfk_2` FOREIGN KEY (`idnotas_gerais`) REFERENCES `notas_gerais` (`idnotas_gerais`)
) ENGINE=InnoDB AUTO_INCREMENT=146 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
