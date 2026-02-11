
import asyncio
from datetime import timedelta
from temporalio import workflow, activity

@activity.defn
async def dbt_run(model: str) -> str:
    print(f"[ACTIVITY] Running dbt: {model}")
    return "OK"

@activity.defn
async def file_scan(path: str) -> list[str]:
    print(f"[ACTIVITY] Scanning path: {path}")
    return ["file1", "file2"]

@workflow.defn
class MasterWorkflow:
    @workflow.run
    async def run(self) -> str:
        print("[WORKFLOW] Start Migration")

        await workflow.execute_activity(dbt_run, "complaints_historical", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "dim_agegroup", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "dim_borough", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "dim_kycode", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "dim_KY_CD", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "dim_Law_", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "dim_PD_code", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "dim_race", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "dim_transit", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "fact_complaints", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "fact_complaint", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "fact_shooting_incident", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "fact_summon", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "load_complaints_historical", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "load_dim_pdcode", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "load_dim_race", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "shootingincidents_historical1", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "summonscases_historical", start_to_close_timeout=timedelta(minutes=5))

        await workflow.execute_activity(dbt_run, "summons_historical", start_to_close_timeout=timedelta(minutes=5))

        return "Done"
