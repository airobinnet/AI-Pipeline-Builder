# backend/app/pipelines/dynamic_pipeline.py

import os
import importlib.util
import asyncio
from collections import deque
from dotenv import load_dotenv

load_dotenv()

def load_node_modules():
    node_modules = {}
    nodes_dir = os.path.join(os.path.dirname(__file__), '..', 'nodes')
    print(f"Loading nodes from: {nodes_dir}")
    for filename in os.listdir(nodes_dir):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            module_path = os.path.join(nodes_dir, filename)
            print(f"Loading module: {module_name} from {module_path}")
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'process') and hasattr(module, 'get_ui_config'):
                node_type = module.get_ui_config()['type']
                print(f"Added node type: {node_type}")
                node_modules[node_type] = module
            else:
                print(f"Module {module_name} does not have required attributes")
    return node_modules

NODE_MODULES = load_node_modules()

async def execute_pipeline(config, start_node_id=None):
    nodes = {node['id']: node for node in config['nodes']}
    edges = config['edges']
    
    if not nodes:
        raise ValueError("No nodes in the pipeline configuration")

    # Create a graph representation
    graph = {node: [] for node in nodes}
    incoming_edges = {node: [] for node in nodes}
    for edge in edges:
        graph[edge['source']].append(edge['target'])
        incoming_edges[edge['target']].append(edge['source'])
    
    # Topological sort
    def topological_sort():
        in_degree = {node: len(incoming) for node, incoming in incoming_edges.items()}
        queue = deque([node for node, degree in in_degree.items() if degree == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(nodes):
            raise ValueError("Graph has a cycle")
        
        return result

    execution_order = topological_sort()

    # Determine the execution order based on the start_node_id
    if start_node_id:
        if start_node_id not in nodes:
            raise ValueError(f"Start node {start_node_id} not found in the pipeline configuration")
        start_index = execution_order.index(start_node_id)
        execution_order = execution_order[start_index:]

    # Execute pipeline
    results = {}
    processed = set()

    async def process_node(node_id):
        if node_id in processed:
            yield node_id, results.get(node_id)
            return

        node = nodes[node_id]
        module = NODE_MODULES.get(node['type'])
        if not module:
            result = f"Unknown node type: {node['type']}"
            results[node_id] = result
            processed.add(node_id)
            yield node_id, result
            return

        if node['type'] == 'Input Node':
            input_data = node.get('input') or node.get('options', {}).get('value', '')
        else:
            if node.get('input') is not None:
                input_data = node['input']
            else:
                parents = incoming_edges.get(node_id, [])
                if not parents:
                    input_data = ''  # Use empty string for nodes without inputs
                else:
                    input_data = []
                    for parent in parents:
                        parent_result = results.get(parent)
                        if parent_result is not None:
                            input_data.append(parent_result)
                    if not input_data:
                        input_data = ''  # Use empty string if all parents were skipped
                    else:
                        input_data = input_data[0] if len(input_data) == 1 else ' '.join(input_data)

        if hasattr(module, 'async_process'):
            async for result in module.async_process(input_data, node.get('options', {})):
                if isinstance(result, dict) and "error" in result:
                    yield node_id, {"error": result["error"]}
                    break
                yield node_id, {"result": result}
                if isinstance(result, dict) and result.get("is_final"):
                    results[node_id] = result.get("image") or result
        else:
            result = module.process(input_data, node.get('options', {}))
            results[node_id] = result
            yield node_id, {"result": result}

        processed.add(node_id)

    # Process nodes in topological order
    for node_id in execution_order:
        async for intermediate_node_id, intermediate_result in process_node(node_id):
            yield intermediate_node_id, intermediate_result

def get_node_types():
    return {node_type: module.get_ui_config() for node_type, module in NODE_MODULES.items()}