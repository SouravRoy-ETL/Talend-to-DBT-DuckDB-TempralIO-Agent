-- Migrated Job: dim_KY_CD
WITH 
tFileInputDelimited_1 AS ( SELECT * FROM {{ source('raw', 'KY_CD') }} ),
tMap_1 AS (
 SELECT Nypd_ky.KY_SK AS KY_SK, Nypd_ky.KY_CD AS KY_CD, Nypd_ky.OFNS_DESC AS OFNS_DESC, pid AS DI_PID, cast(TalendDate.getCurrentDate() as timestamp) AS DI_CREATE_DT FROM Nypd_ky LEFT JOIN (SELECT DISTINCT 1 AS _distinql_0, KY_SK, KY_CD, OFNS_DESC, pid, TalendDate.getCurrentDate() AS DI_CREATE_DT FROM tFileInputDelimited_1) AS temp ON Nypd_ky.KY_SK = temp.KY_SK AND Nypd_ky.KY_CD = temp.KY_CD 
),
final_cte AS ( SELECT * FROM tMap_1 )

SELECT * FROM final_cte