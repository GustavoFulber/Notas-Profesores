USE calculaNota;

CREATE TABLE IF NOT exists `aluno` (
  `idAluno` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) DEFAULT 'Aluno',
  `nota` decimal(4,2) DEFAULT '0.00',
  `idusuario` int DEFAULT NULL,
  PRIMARY KEY (`idAluno`),
  KEY `idusuario_idx` (`idusuario`),
  CONSTRAINT `idusuario` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
