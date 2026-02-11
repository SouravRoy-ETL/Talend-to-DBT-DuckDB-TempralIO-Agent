-- Migrated Job: dim_agegroup
WITH 
tFileInputDelimited_1 AS ( SELECT * FROM {{ source('raw', 'age_groups') }} ),
tMap_1 AS (
 SELECT agegroup.AGE_SK AS AGE_SK, agegroup.AGE_GROUP AS AGE_GROUP, pid AS DI_PID, TalendDate.getCurrentDate() AS DI_CREATE_DT FROM agegroup LEFT JOIN (SELECT * FROM tFileInputDelimited_1) AS input ON agegroup.AGE_SK = input.AGE_SK 
),
final_cte AS ( SELECT * FROM tMap_1 )

SELECT * FROM final_cte