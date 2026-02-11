-- Migrated Job: dim_race
WITH 
tFileInputDelimited_1 AS ( SELECT * FROM {{ source('raw', 'perpvic_race') }} ),
tMap_1 AS (
 WITH race AS (
  SELECT * FROM tFileInputDelimited_1
),
final AS (
  SELECT 
    race.RACE_SK,
    race.PERP_RACE_CODE,
    race.PERP_RACE,
    race.VIC_RACE_CODE,
    race.VIC_RACE,
    pid,
    TalendDate.getCurrentDate() AS DI_CREATE_DT
  FROM race
)
SELECT 
  final.RACE_SK,
  final.PERP_RACE_CODE,
  final.PERP_RACE,
  final.VIC_RACE_CODE,
  final.VIC_RACE,
  final.DI_PID,
  final.DI_CREATE_DT
FROM final 
),
final_cte AS ( SELECT * FROM tMap_1 )

SELECT * FROM final_cte