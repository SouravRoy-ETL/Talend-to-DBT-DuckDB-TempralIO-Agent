import os
import json
import networkx as nx
from concurrent.futures import ThreadPoolExecutor, as_completed
from lxml import etree
from src.config import INPUT_DIR, DBT_OUTPUT_DIR, TEMPORAL_OUTPUT_DIR
from src.graph_builder import ProjectGraph
from src.agent_llm import SouravAgent
from src.temporal_generator import TemporalGenerator

# --- HARDWARE OPTIMIZATION ---
MAX_WORKERS = 8  

class MigrationEngine:
    def __init__(self):
        self.graph_builder = ProjectGraph(INPUT_DIR)
        self.agent = SouravAgent()

    def run(self):
        print(f"[INFO] STARTING TALEND-TO-DBT-SOURAV-AGENT (Parallel Threads: {MAX_WORKERS})...")
        graph = self.graph_builder.build()
        TemporalGenerator(graph, TEMPORAL_OUTPUT_DIR).generate()
        self._generate_dbt_assets_parallel(graph)

    def _generate_dbt_assets_parallel(self, graph):
        os.makedirs(os.path.join(DBT_OUTPUT_DIR, "models"), exist_ok=True)
        os.makedirs(os.path.join(DBT_OUTPUT_DIR, "macros"), exist_ok=True)
        
        tasks = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for job in graph.nodes:
                node_data = graph.nodes[job]
                
                if node_data.get('type') == 'orchestration': 
                    continue
                
                if node_data.get('type') == 'joblet':
                    future = executor.submit(self._convert_joblet, job, node_data['filepath'])
                else:
                    future = executor.submit(self._convert_job_chain, job, node_data['filepath'])
                
                tasks.append(future)

            total = len(tasks)
            completed = 0
            print(f"[INFO] Processing {total} conversion tasks with {MAX_WORKERS} threads...")
            
            for future in as_completed(tasks):
                completed += 1
                try:
                    result = future.result()
                    print(f"   [{completed}/{total}] {result}")
                except Exception as e:
                    print(f"   [ERROR] Task failed: {e}")

    def _convert_joblet(self, name, filepath):
        sql = self._process_xml_chain(name, filepath)
        if sql:
            path = os.path.join(DBT_OUTPUT_DIR, "macros", f"{name}.sql")
            with open(path, "w", encoding='utf-8') as f:
                f.write(f"{{% macro {name}() %}}\n{sql}\n{{% endmacro %}}")
            return f"Converted Joblet: {name}"
        return f"Skipped Joblet: {name}"

    def _convert_job_chain(self, name, filepath):
        sql = self._process_xml_chain(name, filepath)
        if sql:
            path = os.path.join(DBT_OUTPUT_DIR, "models", f"{name}.sql")
            with open(path, "w", encoding='utf-8') as f:
                f.write(f"-- Migrated Job: {name}\n")
                f.write("WITH \n")
                f.write(sql)
                f.write(f"\n\nSELECT * FROM final_cte")
            return f"Converted Job: {name}"
        return f"Skipped Job: {name}"

    def _process_xml_chain(self, job_name, filepath):
        try:
            tree = etree.parse(filepath)
            
            # NAMESPACE-AGNOSTIC GRAPH BUILDING
            internal_graph = nx.DiGraph()
            connections = tree.xpath("//*[local-name()='connection']")
            for conn in connections:
                src, tgt = conn.get("source"), conn.get("target")
                if src and tgt:
                    internal_graph.add_edge(src, tgt)
            
            try:
                comps = list(nx.topological_sort(internal_graph))
            except:
                # Fallback: Get all UNIQUE_NAME values directly if graph fails
                comps = tree.xpath("//*[local-name()='elementParameter' and @name='UNIQUE_NAME']/@value")
                
            cte_list = []
            prev_cte = "dual"
            
            # FETCH ALL NODES
            all_nodes = tree.xpath("//*[local-name()='node']")
            
            for comp_id in comps:
                # SEARCH FOR NODE
                node = None
                for candidate in all_nodes:
                    u_name = candidate.xpath(".//*[local-name()='elementParameter' and @name='UNIQUE_NAME']/@value")
                    if u_name and u_name[0] == comp_id:
                        node = candidate
                        break
                
                if node is None: continue
                
                comp_type = node.get("componentName")
                xml_str = etree.tostring(node).decode('utf-8')
                
                # 1. Handle Inputs
                if "Input" in comp_type:
                    params = node.xpath(".//*[local-name()='elementParameter']")
                    raw_val = None
                    for p in params:
                        if p.get("name") in ["TABLE", "FILENAME"]:
                            raw_val = p.get("value")
                            break
                    
                    if raw_val:
                        if "context." in raw_val or "globalMap.get" in raw_val:
                            var_name = raw_val.split('.')[-1].replace('"', '').replace(')', '')
                            source_ref = f"{{{{ var('{var_name}', 'default_{comp_id}') }}}}"
                        else:
                            clean_val = raw_val.replace('"', '').replace('\\', '/')
                            tbl_name = os.path.splitext(os.path.basename(clean_val))[0] if '/' in clean_val else clean_val
                            source_ref = f"{{{{ source('raw', '{tbl_name}') }}}}"
                    else:
                        source_ref = f"{{{{ source('raw', 'src_{comp_id}') }}}}"

                    cte_list.append(f"{comp_id} AS ( SELECT * FROM {source_ref} )")
                    prev_cte = comp_id
                    continue
                
                if "Output" in comp_type:
                    continue

                # 3. Handle Transformations
                input_map = { "prev_cte": prev_cte }
                result = self.agent.convert_component(job_name, comp_type, xml_str, prev_cte, json.dumps(input_map))
                
                if result.get('status') == 'SUCCESS':
                    clean_sql = result['sql_logic'].strip().rstrip(';')
                    cte_list.append(f"{comp_id} AS (\n {clean_sql} \n)")
                    prev_cte = comp_id
            
            # --- CRITICAL PATCH: NO LEADING/DANGLING COMMAS ---
            if not cte_list:
                return None
                
            return ",\n".join(cte_list) + f",\nfinal_cte AS ( SELECT * FROM {prev_cte} )"
            
        except Exception as e:
            print(f"[WARN] Error processing XML chain for {job_name}: {e}")
            return None