import os
import sys
import time
import subprocess
import webbrowser
from src.main_engine import MigrationEngine
from src.verify_migration import MigrationTester # <--- IMPORT

def main():
    # --- STEP 0: PRE-FLIGHT CHECKS ---
    if not os.path.exists("./input_data/TALEND_PROJECT"):
        print("[ERROR] Target folder './input_data/TALEND_PROJECT' not found.")
        sys.exit(1)

    # --- STEP 1: RUN MIGRATION ENGINE ---
    print("\n" + "="*60)
    print("[INFO] PHASE 1: GENERATING DBT & TEMPORAL CODE")
    print("="*60)
    
    try:
        engine = MigrationEngine()
        engine.run()
    except Exception as e:
        print(f"[FATAL] Migration failed: {e}")
        sys.exit(1)

    # --- STEP 1.5: VERIFY CODE QUALITY (NEW AGENT) ---
    print("\n" + "="*60)
    print("[INFO] PHASE 1.5: VERIFYING CODE INTEGRITY")
    print("="*60)
    
    tester = MigrationTester("./output/dbt_project")
    is_valid = tester.run_checks()
    
    if not is_valid:
        print("\n[STOP] Critical issues found in generated code.")
        print("       Aborting migration execution to prevent runtime errors.")
        print("       Please check ./output/dbt_project/models logs for details.")
        sys.exit(1)

    # --- STEP 2: START WORKER ---
    print("\n" + "="*60)
    print("[INFO] PHASE 2: STARTING TEMPORAL WORKER")
    print("="*60)
    
    worker_script = os.path.join("src", "run_temporal_worker.py")
    worker_process = subprocess.Popen([sys.executable, worker_script])
    
    print("[WORKER] Worker process spawned. Waiting 5s for initialization...")
    time.sleep(5) 

    try:
        # --- STEP 3: TRIGGER WORKFLOW ---
        print("\n" + "="*60)
        print("[INFO] PHASE 3: TRIGGERING MIGRATION JOB")
        print("="*60)
        
        trigger_script = os.path.join("src", "trigger_migration.py")
        result = subprocess.run([sys.executable, trigger_script])
        
        if result.returncode != 0:
            print("[ERROR] Failed to trigger workflow.")

        # --- STEP 4: OPEN BROWSER ---
        print("\n" + "="*60)
        print("[INFO] PHASE 4: OPENING OBSERVABILITY DASHBOARD")
        print("="*60)
        
        url = "http://localhost:8233"
        print(f"[UI] Opening {url}...")
        webbrowser.open(url)

        # --- STEP 5: KEEP ALIVE ---
        print("\n" + "="*60)
        print("[SYSTEM] STATUS: ACTIVE")
        print("="*60)
        print("   - Code Generated: ./output")
        print("   - Code Verified:  PASS")
        print("   - Worker:         RUNNING (PID: {})".format(worker_process.pid))
        print("   - Dashboard:      OPEN")
        print("\n   [PRESS CTRL+C TO STOP THE WORKER AND EXIT]")
        
        worker_process.wait()

    except KeyboardInterrupt:
        print("\n\n[INFO] User requested shutdown.")
    finally:
        if worker_process.poll() is None:
            print("[SYSTEM] Terminating worker process...")
            worker_process.terminate()
            worker_process.wait()
        print("[SYSTEM] Shutdown complete.")

if __name__ == "__main__":
    main()