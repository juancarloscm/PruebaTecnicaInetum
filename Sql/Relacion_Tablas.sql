-- Relaciones Entre las Tablas
SELECT 
    f.nombre_fuente, 
    t.nombre_tema, 
    n.fecha_publicacion, 
    n.titulo, 
    n.visitas, 
    n.compartidos
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.noticias_procesadas` n
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_fuentes_noticias` f 
    ON n.id_fuente = f.id_fuente
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_temas` t 
    ON n.id_tema = t.id_tema
ORDER BY n.fecha_publicacion DESC;

