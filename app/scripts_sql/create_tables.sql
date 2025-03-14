CREATE TABLE `Usuarios` (
  `id_usuario` bigint(20) auto_increment,
  `nombre_usuario` varchar(20),
  `apellido_usuario` varchar(20),
  `fecha_nacimiento_usuario` date,
  `email_usuario` varchar(30),
  `contrasenia_usuario` varchar(15),
  `fecha_registro_usuario` date,
  `codigo_estudiante_upb` bigint(5),
  PRIMARY KEY (`id_usuario`)
);

CREATE TABLE `Libreros` (
  `id_librero` bigint(20) auto_increment,
  `Usuarios_id_usuario` bigint(20),
  PRIMARY KEY (`id_librero`),
    FOREIGN KEY (`Usuarios_id_usuario`) references Usuarios(id_usuario)
);



CREATE TABLE `Libros` (
  `id_libro` bigint(20) auto_increment,
  `isbn` varchar(20),
  `titulo_libro` varchar(30),
  `descripcion_libro` text,
  `imagen_libro` text,
  `fecha_publicacion_libro` date,
  `enlace_libro` text,
  PRIMARY KEY (`id_libro`)
);

CREATE TABLE `Autores` (
  `id_autor` bigint(20) auto_increment,
  `nombre_autor` varchar(20),
  `apellido_autor` varchar(20),
  `fecha_nacimiento_autor` date,
  PRIMARY KEY (`id_autor`)
);

CREATE TABLE `Libreros_Libros` (
  `libreros_id_librero` bigint(20) ,
  `libros_id_libro` bigint(20),
  FOREIGN KEY (`libros_id_libro`) REFERENCES `Libros`(`id_libro`),
  FOREIGN KEY (`libreros_id_librero`) REFERENCES `Libreros`(`id_librero`)
);

CREATE TABLE `Libros_Autores` (
  `libros_id_libro` bigint(20),
  `autores_id_autor` bigint(20),
  FOREIGN KEY (`libros_id_libro`) REFERENCES `Libros`(`id_libro`),
  FOREIGN KEY (`autores_id_autor`) REFERENCES `Autores`(`id_autor`)
);

CREATE TABLE `Categorias` (
  `id_categoria` bigint(20) auto_increment,
  `nombre_categoria` varchar(20),
  PRIMARY KEY (`id_categoria`)
);

CREATE TABLE `Libros_Categorias` (
  `libros_id_libro` bigint(20),
  `categorias_id_categoria` bigint(20),
  FOREIGN KEY (`categorias_id_categoria`) REFERENCES `Categorias`(`id_categoria`),
  FOREIGN KEY (`libros_id_libro`) REFERENCES `Libros`(`id_libro`)
);

