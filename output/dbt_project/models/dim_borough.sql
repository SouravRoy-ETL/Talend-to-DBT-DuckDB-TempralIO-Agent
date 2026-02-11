-- Migrated Job: dim_borough
WITH 
tFileInputDelimited_1 AS ( SELECT * FROM {{ source('raw', 'nyc_boro') }} ),
tMap_1 AS (
 SELECT borough.BORO_SK AS BORO_SK, borough.BORO_CODE AS BORO_CODE, borough.Borough AS BOROUGH, borough.PATROL_BORO_CODE AS PATROL_BORO_CODE, borough.PATROL_BORO AS PATROL_BORO, TalendDate.getCurrentDate() AS DI_CREATE_DT FROM borough 
),
final_cte AS ( SELECT * FROM tMap_1 )

SELECT * FROM final_cte