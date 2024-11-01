CREATE TABLE funcionarios (
    id_funcionario INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) NOT NULL UNIQUE,
    correo VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE ubicaciones (
    id_ubicacion INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE tipos_activo (
    id_tipo INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE activos (
    id_activo INT PRIMARY KEY,
    id_tipo INT,
    id_ubicacion INT,
    id_modelo INT,
    n_parte VARCHAR(50),
    serial VARCHAR(50) UNIQUE,
    procesador VARCHAR(50),
    disco_duro VARCHAR(50),
    memoria_ram VARCHAR(50),
    FOREIGN KEY (id_tipo) REFERENCES tipos_activo(id_tipo),
    FOREIGN KEY (id_ubicacion) REFERENCES ubicaciones(id_ubicacion),
    FOREIGN KEY (id_modelo) REFERENCES modelos(id_modelo)
);

CREATE TABLE marcas (
    id_marca INT PRIMARY KEY AUTO_INCREMENT,
    marca VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE modelos (
    id_modelo INT PRIMARY KEY AUTO_INCREMENT,
    modelo VARCHAR(100) NOT NULL,
    id_marca INT,
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca)
);

CREATE TABLE responsabilidades (
    id_responsabilidad INT PRIMARY KEY AUTO_INCREMENT,
    id_activo INT,
    id_funcionario INT,
    fecha_asignacion DATE,
    fecha_fin DATE,
    FOREIGN KEY (id_activo) REFERENCES activos(id_activo),
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);