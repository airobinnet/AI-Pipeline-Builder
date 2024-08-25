# backend\app\routes.py

from flask import request, jsonify
from app import app
from app.pipelines.dummy_pipelines import execute_pipeline

@app.route('/execute', methods=['POST'])
def execute():
    pipeline_config = request.json
    try:
        result = execute_pipeline(pipeline_config)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500