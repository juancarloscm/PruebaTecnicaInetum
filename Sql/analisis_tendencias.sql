SELECT FORMAT_DATE('%Y-%m', fecha_publicacion) AS mes, nombre, COUNT(*) AS total
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos`
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_temas`
ON fact_articulos.topic_id = dim_temas.topic_id
GROUP BY mes, nombre ORDER BY mes DESC, total DESC
