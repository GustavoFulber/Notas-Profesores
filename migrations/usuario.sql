USE calculaNota;

CREATE TABLE IF NOT exists `usuario` (
  `idusuario` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(45) DEFAULT NULL,
  `senha` varchar(255) DEFAULT NULL,
  `nome` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `aprovado` tinyint DEFAULT '0',
  `perfil` varchar(45) DEFAULT NULL,
  `verificado` tinyint DEFAULT '0',
  `codigo` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
