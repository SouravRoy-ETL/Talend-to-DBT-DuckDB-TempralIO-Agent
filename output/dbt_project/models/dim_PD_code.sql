-- Migrated Job: dim_PD_code
WITH 
tFileInputDelimited_1 AS ( SELECT * FROM {{ source('raw', 'dim_pd_cd.tsv') }} ),
tMap_1 AS (
 WITH pd_code AS (SELECT PD_SK, PD_CD, PD_DESC, DI_PID, DI_CREATE_DT FROM tFileInputDelimited_1), dim_pd_code AS (SELECT PD_SK, PD_CD, PD_DESC, DI_PID, current_date() AS DI_CREATE_DT FROM pd_code) SELECT PD_SK, PD_CD, PD_DESC, DI_PID, DI_CREATE_DT FROM dim_pd_code 
),
final_cte AS ( SELECT * FROM tMap_1 )

SELECT * FROM final_cte