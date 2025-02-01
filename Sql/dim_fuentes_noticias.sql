CREATE OR REPLACE TABLE `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_fuentes_noticias` (
    id_fuente INT64,         -- Identificador unico de la fuente
    nombre_fuente STRING,    -- Nombre del sitio de noticias
    url STRING,              -- Enlace al sitio de noticias
    puntuacion_confiabilidad FLOAT64 -- Puntaje de confiabilidad de la fuente
);

