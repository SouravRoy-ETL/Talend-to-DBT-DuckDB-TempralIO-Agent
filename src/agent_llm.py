import os
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL, AGENT_NAME
from src.knowledge_base import KnowledgeRetriever

# STRICTLY LOCKED PROMPT STRUCTURE - FULL TRANSFORMATION LOGIC PRESERVED
SYSTEM_PROMPT = """
YOU ARE THE TalendToDbtSouravAgent.
Task: Convert Talend XML components into DuckDB SQL / dbt Jinja.

CRITICAL RULES:
1. DIALECT: DuckDB.
2. LOGIC: 
   - 'tMap', 'tXMLMap': Generate a SELECT list mapping expressions to aliases.
   - 'tFilterRow', 'tFilterColumns': Generate a WHERE clause or column selection.
   - 'tAggregateRow', 'tAggregateSortedRow': Generate a GROUP BY with aggregations.
   - 'tSortRow', 'tExternalSortRow': Generate ORDER BY clauses.
   - 'tUniqRow': Generate DISTINCT or QUALIFY ROW_NUMBER() logic.
   - 'tJoin', 'tUnite': Generate JOIN or UNION logic.
   - 'tNormalize', 'tDenormalize', 'tDenormalizeSortedRow', 'tSplitRow': Generate UNNEST or STRING_AGG logic.
   - 'tReplace', 'tConvertType': Generate REGEXP_REPLACE or CAST logic.
   - 'tExtractJSONFields', 'tExtractXMLField', 'tExtractDelimitedFields', 'tExtractDynamicFields', 'tExtractPositionalFields': Generate JSON_EXTRACT, UNNEST(XPATH), or SPLIT_PART logic.
   - 'tSampleRow', 'tReplicate': Generate sampling or direct selection logic.
   - 'tRules', 'tWriteJSONField', 'tWriteXMLField', 'tWriteDynamicFields': Generate complex logic/formatting.
3. CONTEXT: Use the provided FUNCTION MAPPINGS for Java to SQL translation. NO JAVA ALLOWED. CONVERT TALEND JAVA TO DuckDB SQL FUNCTIONS.

CONTEXT:
{rag_context}

OUTPUT FORMAT (JSON):
{{
  "status": "SUCCESS",
  "sql_logic": "SELECT ... FROM ...",
  "issues": []
}}
"""

class SouravAgent:
    def __init__(self):
        # HARDWARE OPTIMIZATION: PURE SPEED (RTX 4050 Priority)
        
        # We target the 6 Performance Cores of the i7-13650HX for the data feed pipeline.
        # Avoiding the 8 Efficiency cores reduces latency jitter.
        p_cores = 6 

        self.llm = ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.0,
            format="json",
            
            # MEMORY & CONTEXT (The Speed Factor)
            # 4096 is the hard limit to keep the 7B/8B model entirely in 6GB VRAM.
            # Going higher triggers System RAM swapping, which kills speed.
            num_ctx=4096,        
            keep_alive=-1,       # Keep model loaded in VRAM between calls.
            
            # COMPUTE ACCELERATION
            num_gpu=999,         # 100% GPU Offload. No CPU Math.
            num_thread=p_cores,  # 6 P-Cores to feed the GPU pipeline.
            num_batch=1024,      # Aggressive ingestion batch size.
            
            # INFERENCE SPEED
            mirostat=0,          # Disable complex sampling algorithms.
            repeat_last_n=64     # Optimize context lookback window.
        )
        self.kb = KnowledgeRetriever()

    def convert_component(self, job_name, comp_type, xml_snippet, prev_cte, input_map):
        context = self.kb.get_context(comp_type, xml_snippet)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "COMPONENT: {comp_type}\nSOURCE: {prev_cte}\nXML:\n{xml_input}")
        ])
        
        try:
            print(f"   ... [LLM] Converting {comp_type} ...")
            chain = prompt | self.llm
            response = chain.invoke({
                "comp_type": comp_type,
                "prev_cte": prev_cte,
                "rag_context": context['rag'],
                "xml_input": xml_snippet
            })
            return json.loads(response.content)
        except Exception as e:
            return {"status": "ERROR", "issues": [str(e)]}