import os
import importlib

def discover_nodes():
    node_files = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith('_node.py')]
    nodes = {}
    for file in node_files:
        module_name = file[:-3]  # Remove .py
        module = importlib.import_module(f'app.nodes.{module_name}')
        node_class = getattr(module, 'Node', None)
        if node_class:
            nodes[node_class.type] = node_class
    return nodes