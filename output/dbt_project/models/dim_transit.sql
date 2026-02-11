-- Migrated Job: dim_transit
WITH 
tFileInputDelimited_1 AS ( SELECT * FROM {{ source('raw', 'dim_transit') }} ),
tMap_1 AS (
 WITH mapped_data AS (SELECT transit.STATION_SK, transit.STATION_NAME, transit.TRANSIT_DISTRICT, pid, TalendDate.getCurrentDate() AS DI_CREATE_DT FROM transit LEFT JOIN tFileInputDelimited_1 ON transit.STATION_SK = tFileInputDelimited_1.STATION_SK) SELECT STATION_SK, STATION_NAME, TRANSIT_DISTRICT, DI_PID, CAST(DI_CREATE_DT AS DATE) AS DI_CREATE_DT FROM mapped_data 
),
final_cte AS ( SELECT * FROM tMap_1 )

SELECT * FROM final_cte