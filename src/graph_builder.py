import os
import glob
import networkx as nx
from lxml import etree

class ProjectGraph:
    def __init__(self, root_dir):
        self.root = root_dir
        self.graph = nx.DiGraph()

    def build(self):
        print(f"[INFO] Scanning {self.root} for Jobs & Joblets...")
        files = glob.glob(os.path.join(self.root, "**", "*.item"), recursive=True)
        
        for filepath in files:
            self._analyze_file(filepath)
            
        print(f"[SUCCESS] Graph Built: {self.graph.number_of_nodes()} Nodes found.")
        return self.graph

    def _analyze_file(self, filepath):
        job_name = os.path.basename(filepath).replace("_0.1.item", "")
        is_joblet = "joblets" in filepath.lower()
        
        node_type = "joblet" if is_joblet else "standard"
        
        try:
            tree = etree.parse(filepath)
            ns = tree.getroot().nsmap
            if None in ns: ns['t'] = ns.pop(None)
            
            # Check for Loops (Orchestration)
            if tree.xpath("//node[contains(@componentName, 'Loop') or contains(@componentName, 'FileList')]", namespaces=ns):
                node_type = "orchestration"
                
            self.graph.add_node(job_name, filepath=filepath, type=node_type)
            
            # Find Dependencies
            # 1. tRunJob
            for node in tree.xpath("//node[@componentName='tRunJob']", namespaces=ns):
                param = node.find("elementParameter[@name='PROCESS:PROCESS_TYPE_PROCESS']", namespaces=ns)
                if param is not None:
                    self.graph.add_edge(job_name, param.get("value"))
                    
        except Exception as e:
            print(f"[WARN] Failed to parse {job_name}: {e}")