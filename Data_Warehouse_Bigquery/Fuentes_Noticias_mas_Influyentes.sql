-- Optimizacion:
-- COUNT(article_id) → Numero de articulos publicados por fuente.
-- SUM(visitas) + SUM(compartidos) → Medida de impacto total.
-- ORDER BY impacto_total DESC LIMIT 10 → Muestra las 10 fuentes mas influyentes.
  
SELECT 
    f.nombre AS fuente, 
    COUNT(a.article_id) AS total_articulos,
    SUM(a.visitas) AS total_visitas,
    SUM(a.compartidos) AS total_compartidos,
    (SUM(a.visitas) + SUM(a.compartidos)) AS impacto_total
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos` a
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_fuentes_noticias` f
    ON a.source_id = f.source_id
GROUP BY fuente
ORDER BY impacto_total DESC
LIMIT 10;

--- Que medios generan mas impacto
