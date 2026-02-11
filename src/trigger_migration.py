import asyncio
import uuid
from temporalio.client import Client

async def main():
    # Connect
    client = await Client.connect("localhost:7233")

    # Generate a unique ID for this run
    run_id = f"migration-run-{uuid.uuid4().hex[:6]}"

    print(f"[INFO] Triggering Workflow ID: {run_id}")
    
    try:
        handle = await client.start_workflow(
            "MasterWorkflow",
            id=run_id,
            task_queue="talend-migration-queue",
        )

        print(f"[SUCCESS] Workflow Started!")
        print(f"[INFO] View Progress: http://localhost:8233/namespaces/default/workflows/{run_id}")
        
        # Optional: Wait for result (blocking)
        # result = await handle.result()
        # print(f"[RESULT] {result}")

    except Exception as e:
        print(f"[ERROR] Failed to trigger workflow: {e}")

if __name__ == "__main__":
    asyncio.run(main())