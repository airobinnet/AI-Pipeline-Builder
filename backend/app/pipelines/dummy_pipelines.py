# backend\app\pipelines\dummy_pipelines.py

import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def gpt_function(input_data, options):
    try:
        if options.get('use_custom_input', False):
            custom_input = options.get('custom_input', '')
            input_data = custom_input.replace('{input}', input_data)

        chat_completion = await client.chat.completions.create(
            model=options.get('model', 'gpt-4'),
            messages=[
                {"role": "system", "content": options.get('system_message', "You are a helpful assistant.")},
                {"role": "user", "content": input_data}
            ],
            max_tokens=int(options.get('max_tokens', 150)),
            temperature=float(options.get('temperature', 0.7))
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def text_transformation(input_data, options):
    if options.get('to_uppercase', False):
        input_data = input_data.upper()
    if options.get('reverse', False):
        input_data = input_data[::-1]
    return input_data

def text_analysis(input_data, options):
    word_count = len(input_data.split())
    char_count = len(input_data)
    return f"Word count: {word_count}, Character count: {char_count}"

def sentiment_analysis(input_data, options):
    # This is a very basic sentiment analysis. In a real-world scenario, you'd use a proper NLP library.
    positive_words = set(['good', 'great', 'excellent', 'happy', 'positive'])
    negative_words = set(['bad', 'awful', 'terrible', 'sad', 'negative'])
    
    words = input_data.lower().split()
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"

def sync_gpt_function(input_data, options):
    return asyncio.run(gpt_function(input_data, options))

pipeline_functions = {
    'Input Node': lambda x, _: x,
    'Text Transformation': text_transformation,
    'Text Analysis': text_analysis,
    'Sentiment Analysis': sentiment_analysis,
    'GPT Node': sync_gpt_function,
}

def execute_pipeline(config):
    nodes = {node['id']: node for node in config['nodes']}
    edges = config['edges']
    
    # Create a graph representation
    graph = {node: [] for node in nodes}
    incoming_edges = {node: [] for node in nodes}
    for edge in edges:
        graph[edge['source']].append(edge['target'])
        incoming_edges[edge['target']].append(edge['source'])
    
    # Find the Input Node
    input_node = next((node for node in nodes.values() if node['type'] == 'Input Node'), None)
    if not input_node:
        raise ValueError("No Input Node found in the pipeline")

    # Execute pipeline
    results = {}
    processed = set()
    execution_order = []

    def process_node(node_id):
        if node_id in processed:
            return results.get(node_id)
        
        node = nodes[node_id]
        function = pipeline_functions.get(node['type'], lambda x, _: f"Unknown function: {node['type']}")
        
        if node['type'] == 'Input Node':
            input_data = node.get('value', '')
        else:
            parents = incoming_edges[node_id]
            if not parents:
                return None  # Skip disconnected nodes
            input_data = [process_node(parent) for parent in parents]
            input_data = [data for data in input_data if data is not None]
            if not input_data:
                return None  # Skip if all parents were skipped
            input_data = input_data[0] if len(input_data) == 1 else ' '.join(input_data)
        
        result = function(input_data, node.get('options', {}))
        
        results[node_id] = result
        processed.add(node_id)
        execution_order.append(node_id)
        return result

    # Start processing from the Input Node
    process_node(input_node['id'])

    # Process any remaining nodes
    for node_id in nodes:
        process_node(node_id)

    # Return results in execution order
    return {node_id: results[node_id] for node_id in execution_order if node_id in results}