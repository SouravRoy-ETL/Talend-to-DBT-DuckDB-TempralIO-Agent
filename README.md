# 🚀 Talend-to-dbt Migration Agent (`talendtodbtsouravagent`)

**Enterprise-Grade Logic Refactoring & Orchestration Engine**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![dbt](https://img.shields.io/badge/dbt-Core-orange)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-yellow)
![Temporal](https://img.shields.io/badge/Temporal.io-Orchestration-black)
![Hardware](https://img.shields.io/badge/RTX%205070%20Ti%20Super-Optimized-green)

An AI-augmented migration framework designed to refactor legacy **Talend XML (.item)** metadata into modular **dbt SQL** models and high-durability **Temporal.io** Python workflows. This agent bridges the gap between imperative legacy ETL and declarative modern data stacks.

---

## 📖 Table of Contents
- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Hardware Optimization (The Squeeze)](#-hardware-optimization-the-squeeze)
- [Temporal.io Orchestration](#-temporalio-orchestration)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)

---

## 🧐 Overview

The **Talend-to-dbt Migration Agent** is not just a code translator; it is a **logic refactoring engine**. It parses the deep semantic structure of Talend jobs to ensure 1:1 behavioral parity while modernizing the codebase.

**Key Capabilities:**
* **Semantic Parsing:** Extracts logic from `tMap`, `tFilterRow`, and `tAggregateRow` using `lxml`.
* **Topological Sorting:** Solves the DAG to ensure SQL Common Table Expressions (CTEs) are ordered correctly.
* **Java-to-SQL Bridge:** Converts proprietary Java routines (e.g., `TalendDate.getCurrentDate()`) into native DuckDB SQL.
* **Workflow Modernization:** Replaces `tRunJob` and `tLoop` with fault-tolerant Temporal workflows.

---

## 🏗 System Architecture

The agent operates on a decoupled, four-tier pipeline:

1.  **Ingestion Tier (`lxml`):** Namespace-agnostic parsing of `.item` and `.properties` files.
2.  **Semantic Tier (`NetworkX`):** Mathematical resolution of component dependencies (DAG Solver).
3.  **Intelligence Tier (`Ollama`):** Local LLM inference (Llama3) grounded by a deterministic Knowledge Base.
4.  **Materialization Tier:** Generation of `.sql` models, Jinja macros, and `.py` Temporal activities.

![Uploading image.png…]()


---

## ⚡ Hardware Optimization (The Squeeze)

This project is specifically tuned to saturate high-end consumer hardware. Default configurations are locked for the **NVIDIA RTX 5070 Ti Super** and **Intel i7-14700K**.

| Component | Setting | Technical Rationale |
| :--- | :--- | :--- |
| **GPU VRAM** | `num_ctx = 4096` | Prevents System RAM swapping by keeping the context window entirely in the 16GB VRAM. |
| **CUDA Cores** | `num_gpu = 999` | Forces 100% of model layers to offload to the GPU. |
| **CPU Threads** | `MAX_WORKERS = 8` | Targets the 8 Performance-Cores (P-Cores) of the i7-14700K for parallel parsing. |

---

## ⏳ Temporal.io Orchestration

We treat ETL migration as a distributed system problem. This agent generates **Temporal Workflows** to replace legacy Talend job schedulers.

* **File Sensors:** Replaces `tWaitForFile`. The generated Python worker polls directories and triggers workflows upon file arrival.
* **Retries & Heartbeats:** Replaces `tLogCatcher`. Temporal automatically handles retries for transient failures without custom error-handling logic.
* **Child Workflows:** Replaces `tRunJob`. Complex job chains are modeled as parent-child workflow executions.

---

## 🛠 Installation

### 1. Prerequisites
* **Python 3.10+** installed.
* **Ollama** installed and running (`ollama serve`).
* **Temporal CLI** installed for local development.

### 2. Clone the Repository
```bash
git clone [https://github.com/sourav/talendtodbtsouravagent.git](https://github.com/sourav/talendtodbtsouravagent.git)
cd talendtodbtsouravagent
3. Install Dependencies
We use a targeted requirements.txt to minimize bloat.

Bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install Core Engine & Parsing Tools
pip install lxml networkx pandas

# Install AI & LangChain Integration
pip install langchain-ollama langchain-core

# Install Target Adapters (dbt & DuckDB)
pip install dbt-core dbt-duckdb duckdb

# Install Orchestration SDK
pip install temporalio
🚀 Quick Start
Step 1: Initialize Local Services
Start your local LLM server and Temporal backend.

Bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Temporal Dev Server
temporal server start-dev
Step 2: Ingest Data
Export your Talend Jobs as items (do not export as scripts). Place the .item and .properties files into the input_data/ folder.

Step 3: Configure Hardware
Open src/config.py and ensure the hardware profile matches your rig:

Python
# src/config.py
LLM_CONFIG = {
    "model": "llama3",
    "num_ctx": 4096,  # RTX 5070 Ti Super VRAM Lock
    "num_gpu": 999
}

PARALLEL_CONFIG = {
    "max_workers": 8  # i7-14700K P-Core Count
}
Step 4: Execute Migration
Run the master orchestrator to begin the conversion.

Bash
python run_migration.py
Step 5: Start Orchestration Worker
Once migration is complete, start the Temporal worker to begin processing file triggers.

Bash
python src/temporal_worker.py
📂 Project Structure
Plaintext
talendtodbtsouravagent/
├── input_data/               # Drop your Talend .item files here
├── output/
│   ├── models/               # Generated dbt SQL models (CTEs)
│   ├── macros/               # Generated dbt Macros (Joblets)
│   └── temporal/             # Generated Temporal Workflow Definitions
├── src/
│   ├── main_engine.py        # Master Parallel Orchestrator
│   ├── agent_llm.py          # LLM Logic & Prompt Engineering
│   ├── graph_builder.py      # NetworkX DAG Solver
│   ├── knowledge_base.py     # Deterministic Component Map
│   └── temporal_worker.py    # Temporal.io Worker Entrypoint
├── run_migration.py          # Main Execution Script
├── requirements.txt          # Python Dependencies
└── README.md                 # Documentation
🔧 Troubleshooting
Issue: CUDA Out of Memory error during inference.

Fix: Reduce num_ctx in src/config.py to 2048 or close other GPU-intensive applications.

Issue: dbt models show "Circular Dependency".

Fix: Check the NetworkX logs in migration.log. The topological sort may have failed due to a loop in the original Talend job (e.g., tLoop connected back to start).

Lead Architect: Sourav License: MIT
