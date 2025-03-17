CREATE TABLE `Usuarios` (
  `id_usuario` bigint(20) auto_increment PRIMARY KEY,
  `nombre_usuario` varchar(20) NOT NULL,
  `apellido_usuario` varchar(20) NOT NULL,
  `fecha_nacimiento_usuario` date NOT NULL,
  `email_usuario` varchar(100) NOT NULL UNIQUE,
  `contrasenia_usuario` varchar(255) NOT NULL,
  `fecha_registro_usuario` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `codigo_estudiante_upb` bigint(5) UNIQUE
);

CREATE TABLE `Libreros` (
  `id_librero` bigint(20) auto_increment PRIMARY KEY,
  `Usuarios_id_usuario` bigint(20) UNIQUE NOT NULL,
  FOREIGN KEY (`Usuarios_id_usuario`) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE `Libros` (
  `id_libro` bigint(20) auto_increment PRIMARY KEY,
  `titulo_libro` varchar(100) NOT NULL,
  `descripcion_libro` text NOT NULL,
  `imagen_libro` text NOT NULL,
  `fecha_publicacion_libro` date NOT NULL
);

CREATE TABLE `Ediciones` (
  `id_edicion` bigint(20) auto_increment PRIMARY KEY,
  `libros_id_libro` bigint(20) NOT NULL,
  `isbn` varchar(13) UNIQUE NOT NULL,
  `enlace_libro` text NOT NULL,
  `fecha_edicion` date NOT NULL,
  FOREIGN KEY (`libros_id_libro`) REFERENCES `Libros`(`id_libro`) ON DELETE CASCADE
);

CREATE TABLE `Autores` (
  `id_autor` bigint(20) auto_increment PRIMARY KEY,
  `nombre_autor` varchar(50) NOT NULL,
  `apellido_autor` varchar(50) NOT NULL,
  `fecha_nacimiento_autor` date NOT NULL
);

CREATE TABLE `Libreros_Libros` (
  `libreros_id_librero` bigint(20),
  `libros_id_libro` bigint(20),
  PRIMARY KEY (`libreros_id_librero`, `libros_id_libro`),
  FOREIGN KEY (`libros_id_libro`) REFERENCES `Libros`(`id_libro`) ON DELETE CASCADE,
  FOREIGN KEY (`libreros_id_librero`) REFERENCES `Libreros`(`id_librero`) ON DELETE CASCADE
);

CREATE TABLE `Libros_Autores` (
  `libros_id_libro` bigint(20),
  `autores_id_autor` bigint(20),
  PRIMARY KEY (`libros_id_libro`, `autores_id_autor`),
  FOREIGN KEY (`libros_id_libro`) REFERENCES `Libros`(`id_libro`) ON DELETE CASCADE,
  FOREIGN KEY (`autores_id_autor`) REFERENCES `Autores`(`id_autor`) ON DELETE CASCADE
);

CREATE TABLE `Categorias` (
  `id_categoria` bigint(20) auto_increment PRIMARY KEY,
  `nombre_categoria` varchar(50) NOT NULL UNIQUE
);

CREATE TABLE `Libros_Categorias` (
  `libros_id_libro` bigint(20),
  `categorias_id_categoria` bigint(20),
  PRIMARY KEY (`libros_id_libro`, `categorias_id_categoria`),
  FOREIGN KEY (`categorias_id_categoria`) REFERENCES `Categorias`(`id_categoria`) ON DELETE CASCADE,
  FOREIGN KEY (`libros_id_libro`) REFERENCES `Libros`(`id_libro`) ON DELETE CASCADE
);
