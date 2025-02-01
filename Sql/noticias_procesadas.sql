-- Tabla de Hechos
CREATE OR REPLACE TABLE `analitica-contact-center-dev.Entorno_Pruebas_modelo.noticias_procesadas` (
    id_articulo INT64,         -- Identificador unico del artículo
    id_fuente INT64,           -- Relación con `dim_fuentes_noticias`
    id_tema INT64,             -- Relación con `dim_temas`
    fecha_publicacion TIMESTAMP, -- Fecha y hora de publicación
    titulo STRING,             -- Título del articulo
    resumen STRING,            -- Resumen del articulo
    url STRING,                -- Enlace al articulo
    visitas INT64,             -- Cantidad de visitas del articulo
    compartidos INT64          -- Cantidad de veces compartido
);

