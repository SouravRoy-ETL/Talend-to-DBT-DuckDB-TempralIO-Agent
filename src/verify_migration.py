import os
import glob
import re
import duckdb
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

# MATCHING YOUR HARDWARE OPTIMIZATION (i7-13650HX)
MAX_WORKERS = 8

class MigrationTester:
    def __init__(self, dbt_project_dir):
        self.dbt_dir = dbt_project_dir
        self.models_dir = os.path.join(dbt_project_dir, "models")
        self.issues = []
        self.existing_models = set()

    def run_checks(self):
        print(f"[TEST] Starting Parallel QA Checks on {self.dbt_dir}...")
        
        if not os.path.exists(self.models_dir):
            self._log_error("Missing 'models' directory.")
            return False

        # 1. PRE-LOAD: Fast scan of all model names for linking checks
        print(f"[TEST] Indexing models...")
        self.existing_models = {
            os.path.basename(f).replace(".sql", "") 
            for f in glob.glob(os.path.join(self.models_dir, "*.sql"))
        }
        
        all_files = glob.glob(os.path.join(self.models_dir, "*.sql"))
        print(f"[TEST] Found {len(all_files)} models. Analyzing with {MAX_WORKERS} threads...")

        # 2. PARALLEL EXECUTION: Run Syntax + Link checks in parallel
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all files to the pool
            future_to_file = {
                executor.submit(self._verify_single_file, filepath): filepath 
                for filepath in all_files
            }
            
            # Gather results as they finish
            for future in as_completed(future_to_file):
                filepath = future_to_file[future]
                try:
                    file_issues = future.result()
                    if file_issues:
                        self.issues.extend(file_issues)
                except Exception as e:
                    self._log_error(f"System Error checking {os.path.basename(filepath)}: {e}")

        # 3. REPORTING
        if self.issues:
            print(Fore.RED + f"\n[FAIL] Verification Failed with {len(self.issues)} issues:" + Style.RESET_ALL)
            # Limit output to first 20 errors to avoid spamming terminal
            for issue in self.issues[:20]:
                print(f" - {issue}")
            if len(self.issues) > 20:
                print(f" ... and {len(self.issues) - 20} more.")
            return False
        else:
            print(Fore.GREEN + "\n[PASS] All checks passed. Code is clean." + Style.RESET_ALL)
            return True

    def _verify_single_file(self, filepath):
        """
        Worker function: Checks ONE file for both Syntax and Links.
        Returns a list of error strings.
        """
        filename = os.path.basename(filepath)
        local_issues = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_sql = f.read()

            # --- CHECK A: Jinja References ---
            refs = re.findall(r"ref\(['\"](.*?)['\"]\)", raw_sql)
            for ref in refs:
                if ref not in self.existing_models:
                    local_issues.append(f"[LINK] {filename} -> missing model '{ref}'")

            # --- CHECK B: SQL Syntax (DuckDB) ---
            # Mock Jinja to make it valid SQL
            clean_sql = re.sub(r"\{\{.*?\}\}", "dummy_table", raw_sql)
            clean_sql = re.sub(r"\{%.*?%\}", "", clean_sql)
            
            # Use a fresh connection per thread (safe & fast)
            con = duckdb.connect(database=':memory:')
            
            # HARDWARE ACCEL: Force DuckDB to use 4 threads for parsing if complex
            con.execute("PRAGMA threads=4")
            
            con.execute(f"CREATE OR REPLACE TEMPORARY VIEW test_view AS {clean_sql} LIMIT 0")
            con.close()

        except Exception as e:
            # Filter actual syntax errors
            err_msg = str(e)
            if "dummy_table" not in err_msg:
                local_issues.append(f"[SYNTAX] {filename}: {err_msg}")
        
        return local_issues

    def _log_error(self, msg):
        self.issues.append(msg)
        print(Fore.RED + f"   [x] {msg}" + Style.RESET_ALL)

if __name__ == "__main__":
    tester = MigrationTester("./output/dbt_project")
    tester.run_checks()