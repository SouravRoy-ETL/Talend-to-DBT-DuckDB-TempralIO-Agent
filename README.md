# Talend-to-DBT-DuckDB-TempralIO-Agent
🚀 Talend-to-dbt Migration Agent
An enterprise-grade, AI-augmented migration framework designed to refactor legacy Talend XML (.item) metadata into modular dbt SQL and Temporal.io Python workflows.

📖 Table of Contents
Overview

System Architecture

Hardware Optimization

Temporal.io Orchestration

Installation

Quick Start

Project Structure

🧐 Overview
The Talend-to-dbt Migration Agent automates the transition from imperative, Java-heavy Talend jobs to declarative, cloud-native dbt models. It utilizes local LLMs (via Ollama) to translate complex Java logic into high-performance DuckDB SQL while maintaining absolute logical parity through topological sorting.

🏗 System Architecture
The agent operates through a decoupled, four-tier pipeline:

Ingestion Tier: Parses Talend .item files using lxml to extract metadata and predicates.

Semantic Tier: Uses NetworkX to build a Directed Acyclic Graph (DAG) for component topological sorting.

Intelligence Tier: Interfaces with local LLMs (Llama3/Mistral) to refactor Java routines into SQL.

Materialization Tier: Generates finalized dbt models (.sql), macros, and Temporal SDK workflows.

⚡ Hardware Optimization
This agent is specifically tuned to "squeeze" maximum performance from high-end consumer hardware:

GPU (NVIDIA RTX 5070 Ti Super): Utilizes num_gpu=999 to lock the model entirely in VRAM (16GB), preventing PCIe bus saturation.

CPU (Intel i7-14700K): Targets the 8 high-performance P-Cores for parallel metadata parsing and graph resolution.

Concurrency: Configured with MAX_WORKERS=8 for simultaneous batch processing.

⏳ Temporal.io Orchestration
Unlike basic converters, this agent treats ETL as a distributed workflow. It generates Temporal.io Python SDK code to manage:

File-Based Triggers: Sensing and reacting to file arrivals in the landing zone.

State Management: Tracking job status and handling retries across complex multi-job chains.

Orchestration: Replacing legacy Talend tRunJob and tLoop components with fault-tolerant Python activities.

🛠 Installation
1. Prerequisites
Python: 3.10 or higher

Ollama: Running locally (ollama serve)

Temporal: Local server or Cloud access (temporal server start-dev)

2. Clone and Setup
Bash
git clone https://github.com/your-username/talendtodbtsouravagent.git
cd talendtodbtsouravagent
3. Pip Commands
Install core dependencies using the optimized stack:

Bash
# Update pip
python -m pip install --upgrade pip

# Install core migration engine components
pip install lxml networkx langchain_ollama pandas

# Install dbt and target adapter
pip install dbt-core dbt-duckdb

# Install Temporal SDK
pip install temporalio
🚀 Quick Start
1. Prepare Metadata
Place your exported Talend .item XML files into the input_data/ directory.

2. Configure Environment
Update src/config.py with your hardware-specific parameters:

Python
# Hardware Squeeze Profile
NUM_CTX = 4096
NUM_GPU = 999  # RTX 5070 Ti Super Optimized
MAX_WORKERS = 8 # i7-14700K P-Core Affinity
3. Run Migration
Bash
# Initialize Ollama
ollama run llama3

# Execute the master migration script
python run_migration.py
4. Run Temporal Worker
Bash
# Start the worker to handle generated file-based workflows
python src/temporal_worker.py
📂 Project Structure
Plaintext
talendtodbtsouravagent/
├── input_data/               # Source Talend XML files (.item)
├── output/                   # Resultant migration artifacts
│   ├── models/               # Generated dbt SQL CTEs
│   ├── macros/               # Reusable dbt macros
│   └── temporal/             # Temporal.io Python workflows
├── src/
│   ├── main_engine.py        # Master parallel orchestrator
│   ├── agent_llm.py          # AI logic & prompt engine
│   └── knowledge_base.py     # Deterministic mapping (800+ rules)
└── run_migration.py          # Unified entry point
