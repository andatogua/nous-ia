-- =====================================================
-- SCRIPT DE CREACIÓN: Sistema de Apoyo a la Salud Mental
-- Base de datos: nousia_db
-- =====================================================

-- =====================================================
-- TABLAS DE CATÁLOGO
-- =====================================================

CREATE TABLE IF NOT EXISTS TB_SEXOS (
    ID_SEXO INT AUTO_INCREMENT PRIMARY KEY,
    DESCRIPCION VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TB_ROLES (
    ID_ROL INT AUTO_INCREMENT PRIMARY KEY,
    NOMBRE_ROL VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TB_EMOCIONES (
    ID_EMOCION INT AUTO_INCREMENT PRIMARY KEY,
    NOMBRE_EMOCION VARCHAR(100) NOT NULL UNIQUE
);

-- =====================================================
-- TABLAS DE USUARIOS Y PACIENTES
-- =====================================================

CREATE TABLE IF NOT EXISTS TB_USUARIOS (
    ID_USUARIO INT AUTO_INCREMENT PRIMARY KEY,
    CEDULA VARCHAR(20) UNIQUE,
    NOMBRE VARCHAR(100) NOT NULL,
    APELLIDO VARCHAR(100) NOT NULL,
    CORREO VARCHAR(255) UNIQUE NOT NULL,
    TELEFONO VARCHAR(20),
    FECHA_NACIMIENTO DATE,
    ID_SEXO INT,
    USERNAME VARCHAR(100) UNIQUE NOT NULL,
    PASSWORD_HASH TEXT NOT NULL,
    ID_ROL INT DEFAULT 2,
    ESTADO_CUENTA VARCHAR(20) DEFAULT 'ACTIVO',
    FECHA_CREACION DATETIME DEFAULT CURRENT_TIMESTAMP,
    FECHA_ACTUALIZACION DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_SEXO) REFERENCES TB_SEXOS(ID_SEXO) ON DELETE SET NULL,
    FOREIGN KEY (ID_ROL) REFERENCES TB_ROLES(ID_ROL) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS TB_PACIENTES (
    ID_PACIENTE INT AUTO_INCREMENT PRIMARY KEY,
    ID_USUARIO INT NOT NULL UNIQUE,
    FECHA_REGISTRO DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_USUARIO) REFERENCES TB_USUARIOS(ID_USUARIO) ON DELETE CASCADE
);

-- =====================================================
-- TABLAS DE CUESTIONARIOS
-- =====================================================

CREATE TABLE IF NOT EXISTS TB_CUESTIONARIOS (
    ID_CUESTIONARIO INT AUTO_INCREMENT PRIMARY KEY,
    CODIGO VARCHAR(50) UNIQUE NOT NULL,
    NOMBRE VARCHAR(255) NOT NULL,
    DESCRIPCION TEXT,
    ACTIVO TINYINT(1) DEFAULT 1
);

CREATE TABLE IF NOT EXISTS TB_PREGUNTAS (
    ID_PREGUNTA INT AUTO_INCREMENT PRIMARY KEY,
    ID_CUESTIONARIO INT NOT NULL,
    TEXTO_PREGUNTA TEXT NOT NULL,
    ORDEN_PREGUNTA INT DEFAULT 0,
    ACTIVA TINYINT(1) DEFAULT 1,
    FOREIGN KEY (ID_CUESTIONARIO) REFERENCES TB_CUESTIONARIOS(ID_CUESTIONARIO) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TB_OPCIONES_RESPUESTA (
    ID_OPCION INT AUTO_INCREMENT PRIMARY KEY,
    ID_CUESTIONARIO INT NOT NULL,
    ID_PREGUNTA INT NOT NULL,
    TEXTO_OPCION TEXT NOT NULL,
    VALOR NUMERIC(5,2) NOT NULL,
    ORDEN_OPCION INT DEFAULT 0,
    FOREIGN KEY (ID_CUESTIONARIO) REFERENCES TB_CUESTIONARIOS(ID_CUESTIONARIO) ON DELETE CASCADE,
    FOREIGN KEY (ID_PREGUNTA) REFERENCES TB_PREGUNTAS(ID_PREGUNTA) ON DELETE CASCADE
);

-- =====================================================
-- TABLAS DE EVALUACIONES Y RESULTADOS
-- =====================================================

CREATE TABLE IF NOT EXISTS TB_EVALUACIONES (
    ID_EVALUACION INT AUTO_INCREMENT PRIMARY KEY,
    ID_PACIENTE INT NOT NULL,
    ID_CUESTIONARIO INT NOT NULL,
    FECHA_INICIO DATETIME DEFAULT CURRENT_TIMESTAMP,
    FECHA_FIN DATETIME DEFAULT CURRENT_TIMESTAMP,
    ESTADO_EVALUACION VARCHAR(50) DEFAULT 'COMPLETADA',
    OBSERVACION_GENERAL TEXT,
    FOREIGN KEY (ID_PACIENTE) REFERENCES TB_PACIENTES(ID_PACIENTE) ON DELETE CASCADE,
    FOREIGN KEY (ID_CUESTIONARIO) REFERENCES TB_CUESTIONARIOS(ID_CUESTIONARIO) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TB_RESPUESTAS_USUARIO (
    ID_RESPUESTA INT AUTO_INCREMENT PRIMARY KEY,
    ID_EVALUACION INT NOT NULL,
    ID_PREGUNTA INT NOT NULL,
    ID_OPCION INT NOT NULL,
    VALOR_OBTENIDO NUMERIC(5,2) NOT NULL,
    FOREIGN KEY (ID_EVALUACION) REFERENCES TB_EVALUACIONES(ID_EVALUACION) ON DELETE CASCADE,
    FOREIGN KEY (ID_PREGUNTA) REFERENCES TB_PREGUNTAS(ID_PREGUNTA) ON DELETE CASCADE,
    FOREIGN KEY (ID_OPCION) REFERENCES TB_OPCIONES_RESPUESTA(ID_OPCION) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TB_RESULTADOS_CUESTIONARIO (
    ID_RESULTADO INT AUTO_INCREMENT PRIMARY KEY,
    ID_EVALUACION INT NOT NULL UNIQUE,
    PUNTAJE_TOTAL NUMERIC(10,2) NOT NULL,
    PUNTAJE_ESCALADO NUMERIC(5,2),
    NIVEL_RESULTADO VARCHAR(100),
    INTERPRETACION TEXT,
    REQUIERE_ATENCION TINYINT(1) DEFAULT 0,
    FOREIGN KEY (ID_EVALUACION) REFERENCES TB_EVALUACIONES(ID_EVALUACION) ON DELETE CASCADE
);

-- =====================================================
-- TABLAS DE ESTADO DE ÁNIMO
-- =====================================================

CREATE TABLE IF NOT EXISTS TB_REGISTROS_ESTADO_ANIMO (
    ID_REGISTRO_ANIMO INT AUTO_INCREMENT PRIMARY KEY,
    ID_PACIENTE INT NOT NULL,
    ID_EMOCION INT NOT NULL,
    NIVEL_INTENSIDAD INT DEFAULT 5,
    OBSERVACION TEXT,
    FECHA_REGISTRO DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_PACIENTE) REFERENCES TB_PACIENTES(ID_PACIENTE) ON DELETE CASCADE,
    FOREIGN KEY (ID_EMOCION) REFERENCES TB_EMOCIONES(ID_EMOCION) ON DELETE CASCADE
);

-- =====================================================
-- TABLAS DE RECOMENDACIONES
-- =====================================================

CREATE TABLE IF NOT EXISTS TB_RECOMENDACIONES (
    ID_RECOMENDACION INT AUTO_INCREMENT PRIMARY KEY,
    ID_RESULTADO INT,
    ID_USUARIO INT NOT NULL,
    FUENTE_RECOMENDACION VARCHAR(50) DEFAULT 'GPT',
    TITULO VARCHAR(255) NOT NULL,
    DESCRIPCION TEXT,
    FECHA_GENERACION DATETIME DEFAULT CURRENT_TIMESTAMP,
    ESTADO VARCHAR(50) DEFAULT 'PENDIENTE',
    FOREIGN KEY (ID_RESULTADO) REFERENCES TB_RESULTADOS_CUESTIONARIO(ID_RESULTADO) ON DELETE SET NULL,
    FOREIGN KEY (ID_USUARIO) REFERENCES TB_USUARIOS(ID_USUARIO) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TB_SEGUIMIENTO_RECOMENDACIONES (
    ID_SEGUIMIENTO INT AUTO_INCREMENT PRIMARY KEY,
    ID_RECOMENDACION INT NOT NULL,
    ID_USUARIO INT NOT NULL,
    REALIZADA TINYINT(1) DEFAULT 0,
    FECHA_REGISTRO DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_RECOMENDACION) REFERENCES TB_RECOMENDACIONES(ID_RECOMENDACION) ON DELETE CASCADE,
    FOREIGN KEY (ID_USUARIO) REFERENCES TB_USUARIOS(ID_USUARIO) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TB_SEGUIMIENTO_EMOCIONAL_ACTIVIDAD (
    ID_SEGUIMIENTO_ACTIVIDAD INT AUTO_INCREMENT PRIMARY KEY,
    ID_USUARIO INT NOT NULL,
    ID_RECOMENDACION INT NOT NULL,
    ID_EMOCION INT NOT NULL,
    NIVEL_INTENSIDAD INT DEFAULT 5,
    OBSERVACION TEXT,
    REALIZADA TINYINT(1) DEFAULT 0,
    FECHA_REGISTRO DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_USUARIO) REFERENCES TB_USUARIOS(ID_USUARIO) ON DELETE CASCADE,
    FOREIGN KEY (ID_RECOMENDACION) REFERENCES TB_RECOMENDACIONES(ID_RECOMENDACION) ON DELETE CASCADE,
    FOREIGN KEY (ID_EMOCION) REFERENCES TB_EMOCIONES(ID_EMOCION) ON DELETE CASCADE
);

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

CREATE INDEX idx_usuarios_correo ON TB_USUARIOS(CORREO);
CREATE INDEX idx_usuarios_username ON TB_USUARIOS(USERNAME);
CREATE INDEX idx_evaluaciones_paciente ON TB_EVALUACIONES(ID_PACIENTE);
CREATE INDEX idx_evaluaciones_fecha ON TB_EVALUACIONES(FECHA_FIN);
CREATE INDEX idx_resultados_evaluacion ON TB_RESULTADOS_CUESTIONARIO(ID_EVALUACION);
CREATE INDEX idx_registros_paciente ON TB_REGISTROS_ESTADO_ANIMO(ID_PACIENTE);
CREATE INDEX idx_registros_fecha ON TB_REGISTROS_ESTADO_ANIMO(FECHA_REGISTRO);
CREATE INDEX idx_recomendaciones_usuario ON TB_RECOMENDACIONES(ID_USUARIO);
CREATE INDEX idx_seguimiento_usuario ON TB_SEGUIMIENTO_RECOMENDACIONES(ID_USUARIO);

-- =====================================================
-- DATOS INICIALES: CATÁLOGOS
-- =====================================================

INSERT IGNORE INTO TB_SEXOS (ID_SEXO, DESCRIPCION) VALUES
(1, 'Masculino'),
(2, 'Femenino'),
(3, 'Otro');

INSERT IGNORE INTO TB_ROLES (ID_ROL, NOMBRE_ROL) VALUES
(1, 'Administrador'),
(2, 'Paciente'),
(3, 'Profesional');

INSERT IGNORE INTO TB_EMOCIONES (ID_EMOCION, NOMBRE_EMOCION) VALUES
(1, 'Alegría'),
(2, 'Tristeza'),
(3, 'Enojo'),
(4, 'Miedo'),
(5, 'Sorpresa'),
(6, 'Disgusto'),
(7, 'Ansiedad'),
(8, 'Calma'),
(9, 'Frustración'),
(10, 'Esperanza'),
(11, 'Gratitud'),
(12, 'Culpa'),
(13, 'Vergüenza'),
(14, 'Aburrimiento'),
(15, 'Entusiasmo'),
(16, 'Confusión'),
(17, 'Soledad'),
(18, 'Satisfacción'),
(19, 'Orgullo'),
(20, 'Preocupación');

-- =====================================================
-- DATOS INICIALES: CUESTIONARIOS
-- =====================================================

INSERT IGNORE INTO TB_CUESTIONARIOS (ID_CUESTIONARIO, CODIGO, NOMBRE, DESCRIPCION, ACTIVO) VALUES
(1, 'PHQ-9', 'Patient Health Questionnaire-9', 'Cuestionario de 9 preguntas para evaluar la depresión. Escala de 0-27 puntos.', 1),
(2, 'WHO-5', 'Well-Being Index-5', 'Cuestionario de 5 preguntas para evaluar el bienestar psicológico general. Escala de 0-100.', 1);

-- =====================================================
-- DATOS INICIALES: PREGUNTAS PHQ-9
-- =====================================================

INSERT IGNORE INTO TB_PREGUNTAS (ID_PREGUNTA, ID_CUESTIONARIO, TEXTO_PREGUNTA, ORDEN_PREGUNTA, ACTIVA) VALUES
(1, 1, '¿Con qué frecuencia le han molestado los siguientes problemas: Poco interés o placer para hacer cosas?', 1, 1),
(2, 1, '¿Con qué frecuencia se ha sentido triste, deprimido o sin esperanza?', 2, 1),
(3, 1, '¿Con qué frecuencia le ha costado dormirse o mantenerse dormido, o ha dormido demasiado?', 3, 1),
(4, 1, '¿Con qué frecuencia se ha sentido cansado o con poca energía?', 4, 1),
(5, 1, '¿Con qué frecuencia ha tenido poco apetito o ha comido en exceso?', 5, 1),
(6, 1, '¿Con qué frecuencia se ha sentido mal consigo mismo, que es un fracaso o que no vale nada?', 6, 1),
(7, 1, '¿Con qué frecuencia le ha costado concentrarse en cosas como leer el periódico o ver la televisión?', 7, 1),
(8, 1, '¿Con qué frecuencia se ha movido o hablado tan lentamente que otras personas podrían haberlo notado? O lo contrario, ¿se ha sentido tan inquieto que se ha movido mucho más de lo habitual?', 8, 1),
(9, 1, '¿Con qué frecuencia ha tenido pensamientos de que estaría mejor muerto o de hacerse daño de alguna manera?', 9, 1);

-- =====================================================
-- DATOS INICIALES: OPCIONES PHQ-9
-- =====================================================

INSERT IGNORE INTO TB_OPCIONES_RESPUESTA (ID_OPCION, ID_CUESTIONARIO, ID_PREGUNTA, TEXTO_OPCION, VALOR, ORDEN_OPCION) VALUES
(1, 1, 1, 'Nunca', 0.00, 1),
(2, 1, 1, 'Varios días', 1.00, 2),
(3, 1, 1, 'Más de la mitad de los días', 2.00, 3),
(4, 1, 1, 'Casi todos los días', 3.00, 4),
(5, 1, 2, 'Nunca', 0.00, 1),
(6, 1, 2, 'Varios días', 1.00, 2),
(7, 1, 2, 'Más de la mitad de los días', 2.00, 3),
(8, 1, 2, 'Casi todos los días', 3.00, 4),
(9, 1, 3, 'Nunca', 0.00, 1),
(10, 1, 3, 'Varios días', 1.00, 2),
(11, 1, 3, 'Más de la mitad de los días', 2.00, 3),
(12, 1, 3, 'Casi todos los días', 3.00, 4),
(13, 1, 4, 'Nunca', 0.00, 1),
(14, 1, 4, 'Varios días', 1.00, 2),
(15, 1, 4, 'Más de la mitad de los días', 2.00, 3),
(16, 1, 4, 'Casi todos los días', 3.00, 4),
(17, 1, 5, 'Nunca', 0.00, 1),
(18, 1, 5, 'Varios días', 1.00, 2),
(19, 1, 5, 'Más de la mitad de los días', 2.00, 3),
(20, 1, 5, 'Casi todos los días', 3.00, 4),
(21, 1, 6, 'Nunca', 0.00, 1),
(22, 1, 6, 'Varios días', 1.00, 2),
(23, 1, 6, 'Más de la mitad de los días', 2.00, 3),
(24, 1, 6, 'Casi todos los días', 3.00, 4),
(25, 1, 7, 'Nunca', 0.00, 1),
(26, 1, 7, 'Varios días', 1.00, 2),
(27, 1, 7, 'Más de la mitad de los días', 2.00, 3),
(28, 1, 7, 'Casi todos los días', 3.00, 4),
(29, 1, 8, 'Nunca', 0.00, 1),
(30, 1, 8, 'Varios días', 1.00, 2),
(31, 1, 8, 'Más de la mitad de los días', 2.00, 3),
(32, 1, 8, 'Casi todos los días', 3.00, 4),
(33, 1, 9, 'Nunca', 0.00, 1),
(34, 1, 9, 'Varios días', 1.00, 2),
(35, 1, 9, 'Más de la mitad de los días', 2.00, 3),
(36, 1, 9, 'Casi todos los días', 3.00, 4);

-- =====================================================
-- DATOS INICIALES: PREGUNTAS WHO-5
-- =====================================================

INSERT IGNORE INTO TB_PREGUNTAS (ID_PREGUNTA, ID_CUESTIONARIO, TEXTO_PREGUNTA, ORDEN_PREGUNTA, ACTIVA) VALUES
(10, 2, 'Me he sentido alegre y de buen humor', 1, 1),
(11, 2, 'Me he sentido tranquilo/a y relajado/a', 2, 1),
(12, 2, 'Me he sentido activo/a y con energía', 3, 1),
(13, 2, 'Al despertar me he sentido fresco/a y descansado/a', 4, 1),
(14, 2, 'Mi vida cotidiana ha estado llena de cosas que me interesan', 5, 1);

-- =====================================================
-- DATOS INICIALES: OPCIONES WHO-5
-- =====================================================

INSERT IGNORE INTO TB_OPCIONES_RESPUESTA (ID_OPCION, ID_CUESTIONARIO, ID_PREGUNTA, TEXTO_OPCION, VALOR, ORDEN_OPCION) VALUES
(37, 2, 10, 'En ningún momento', 0.00, 1),
(38, 2, 10, 'Rara vez', 1.00, 2),
(39, 2, 10, 'A veces', 2.00, 3),
(40, 2, 10, 'Frecuentemente', 3.00, 4),
(41, 2, 10, 'Todo el tiempo', 4.00, 5),
(42, 2, 11, 'En ningún momento', 0.00, 1),
(43, 2, 11, 'Rara vez', 1.00, 2),
(44, 2, 11, 'A veces', 2.00, 3),
(45, 2, 11, 'Frecuentemente', 3.00, 4),
(46, 2, 11, 'Todo el tiempo', 4.00, 5),
(47, 2, 12, 'En ningún momento', 0.00, 1),
(48, 2, 12, 'Rara vez', 1.00, 2),
(49, 2, 12, 'A veces', 2.00, 3),
(50, 2, 12, 'Frecuentemente', 3.00, 4),
(51, 2, 12, 'Todo el tiempo', 4.00, 5),
(52, 2, 13, 'En ningún momento', 0.00, 1),
(53, 2, 13, 'Rara vez', 1.00, 2),
(54, 2, 13, 'A veces', 2.00, 3),
(55, 2, 13, 'Frecuentemente', 3.00, 4),
(56, 2, 13, 'Todo el tiempo', 4.00, 5),
(57, 2, 14, 'En ningún momento', 0.00, 1),
(58, 2, 14, 'Rara vez', 1.00, 2),
(59, 2, 14, 'A veces', 2.00, 3),
(60, 2, 14, 'Frecuentemente', 3.00, 4),
(61, 2, 14, 'Todo el tiempo', 4.00, 5);
