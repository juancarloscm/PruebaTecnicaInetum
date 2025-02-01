-- Optimizacion:
-- FORMAT_DATE('%Y-%m', fecha_publicacion) → Agrupa los datos por mes.
-- COUNT(*) → Cuenta cuántos artículos hay por tema en cada mes.
-- Ordenado por mes y volumen de artículos publicados.
    
SELECT 
    FORMAT_DATE('%Y-%m', fecha_publicacion) AS mes,
    t.nombre AS tema,
    COUNT(*) AS total_articulos
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos` f
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_temas` t 
    ON f.topic_id = t.topic_id
GROUP BY mes, tema
ORDER BY mes DESC, total_articulos DESC;

-- ¿Cuáles son los temas más populares?

