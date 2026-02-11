-- Migrated Job: dim_Law_
WITH 
tFileInputDelimited_1 AS ( SELECT * FROM {{ source('raw', 'dim_law') }} ),
tMap_1 AS (
 WITH mapped_data AS (SELECT nypdlaw.LAW_SK, nypdlaw.LAW_DESC, nypdlaw.LAW_SECTION_NUMBER, pid, TalendDate.getCurrentDate() AS DI_CREATE_DT FROM nypdlaw LEFT JOIN input_tables ON nypdlaw.LAW_SK = input_tables.LAW_SK) SELECT LAW_SK, LAW_DESC, LAW_SECTION_NUMBER, DI_PID, CAST(DI_CREATE_DT AS DATE) AS DI_CREATE_DT FROM mapped_data 
),
final_cte AS ( SELECT * FROM tMap_1 )

SELECT * FROM final_cte