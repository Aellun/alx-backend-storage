-- SQL script to list all bands with Glam rock as their main style,
-- ranked by their longevity
SELECT 
    band_name AS band_name,
    (2022 - formed) AS lifespan
FROM 
    metal_bands
WHERE 
    main_style = 'Glam rock'
    AND split IS NOT NULL
    AND split > formed
ORDER BY 
    lifespan DESC;
