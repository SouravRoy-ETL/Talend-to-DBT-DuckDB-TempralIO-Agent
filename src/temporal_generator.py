import os
import networkx as nx

class TemporalGenerator:
    def __init__(self, graph, output_dir):
        self.graph = graph
        self.out_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate(self):
        print("[INFO] Generating Temporal Workflow...")
        content = """
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
"""
        # Add Logic
        for node in self.graph.nodes:
            content += f"""
        await workflow.execute_activity(dbt_run, "{node}", start_to_close_timeout=timedelta(minutes=5))
"""
        content += """
        return "Done"
"""
        # UTF-8 ENFORCED
        with open(os.path.join(self.out_dir, "workflow.py"), "w", encoding='utf-8') as f:
            f.write(content)