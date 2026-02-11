import os

# --- AGENT CONFIGURATION ---
AGENT_NAME = "TalendToDbtSouravAgent"
OLLAMA_MODEL = "deepseek-coder-v2" 
OLLAMA_BASE_URL = "http://localhost:11434"

# --- TARGET DIALECT ---
TARGET_DB = "DuckDB" 

# --- PATHS ---
# Base directory is one level up from 'src'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input/Output paths
INPUT_DIR = os.path.join(BASE_DIR, "input_data", "TALEND_PROJECT")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DBT_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "dbt_project")
TEMPORAL_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "temporal_workflows")