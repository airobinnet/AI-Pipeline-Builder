from quart import jsonify, request, Response
from app import app
from app.pipelines.dynamic_pipeline import execute_pipeline, get_node_types
import json
import asyncio

pipeline_config = None

@app.route('/start-pipeline', methods=['POST'])
async def start_pipeline():
    global pipeline_config
    pipeline_config = await request.get_json()
    return jsonify({"status": "Pipeline configuration received"}), 200

@app.route('/execute', methods=['GET'])
async def execute():
    global pipeline_config

    if pipeline_config is None:
        return jsonify({"error": "No pipeline configuration received"}), 400

    start_node_id = pipeline_config.get('startNodeId')
    print('Received pipeline configuration:', pipeline_config)

    async def generate():
        try:
            async for node_id, result in execute_pipeline(pipeline_config, start_node_id):
                yield f"data: {json.dumps({'id': node_id, 'result': result})}\n\n"
        except ValueError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/node-types', methods=['GET'])
async def node_types():
    return jsonify(get_node_types())