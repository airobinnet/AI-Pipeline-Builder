// frontend\src\App.js

import React, { useState, useCallback, useMemo } from 'react';
import ReactFlow, { 
  addEdge, 
  Background, 
  Controls, 
  MiniMap,
  useNodesState,
  useEdgesState,
  Handle,
  getBezierPath,
  getMarkerEnd,
} from 'reactflow';
import 'reactflow/dist/style.css';
import axios from 'axios';
import './App.css';

const NODE_TYPES = {
  'Input Node': 'Input Node',
  'Text Transformation': 'Text Transformation',
  'Text Analysis': 'Text Analysis',
  'Sentiment Analysis': 'Sentiment Analysis',
  'GPT Node': 'GPT Node',
};

const NodeTemplate = ({ data, isConnectable }) => {
  const nodeType = data.label;

  return (
    <div className={`node ${nodeType.replace(/\s+/g, '-').toLowerCase()}`}>
      {nodeType !== 'Input Node' && <Handle type="target" position="top" isConnectable={isConnectable} />}
      <div className="node-header">{nodeType}</div>
      <div className="node-content">
        {nodeType === 'Input Node' && (
          <input 
            className="nodrag"
            type="text" 
            value={data.value || ''}
            onChange={(e) => data.updateNodeData(data.id, 'value', e.target.value)}
            placeholder="Enter input"
          />
        )}
        {nodeType === 'Text Transformation' && (
          <>
            <label className="nodrag">
              <input 
                type="checkbox" 
                checked={data.options.to_uppercase || false}
                onChange={(e) => data.updateNodeData(data.id, 'options', { to_uppercase: e.target.checked })}
              />
              To Uppercase
            </label>
            <label className="nodrag">
              <input 
                type="checkbox" 
                checked={data.options.reverse || false}
                onChange={(e) => data.updateNodeData(data.id, 'options', { reverse: e.target.checked })}
              />
              Reverse Text
            </label>
          </>
        )}
        {nodeType === 'GPT Node' && (
          <>
            <select 
              className="nodrag"
              value={data.options.model || 'gpt-4'}
              onChange={(e) => data.updateNodeData(data.id, 'options', { model: e.target.value })}
            >
              <option value="gpt-4o">GPT-4o</option>
              <option value="gpt-4o-mini">GPT-4o-mini</option>
              <option value="gpt-4-turbo">GPT-4-turbo</option>
            </select>
            <input 
              className="nodrag"
              type="number" 
              value={data.options.max_tokens || 150}
              onChange={(e) => data.updateNodeData(data.id, 'options', { max_tokens: e.target.value })}
              placeholder="Max Tokens"
            />
            <input 
              className="nodrag"
              type="number" 
              value={data.options.temperature || 0.7}
              onChange={(e) => data.updateNodeData(data.id, 'options', { temperature: e.target.value })}
              placeholder="Temperature"
              step="0.1"
              min="0"
              max="1"
            />
            <textarea 
              className="nodrag"
              value={data.options.system_message || ''}
              onChange={(e) => data.updateNodeData(data.id, 'options', { system_message: e.target.value })}
              placeholder="System Message"
            />
            <label className="nodrag">
              <input 
                type="checkbox" 
                checked={data.options.use_custom_input || false}
                onChange={(e) => data.updateNodeData(data.id, 'options', { use_custom_input: e.target.checked })}
              />
              Use Custom Input
            </label>
            {data.options.use_custom_input && (
              <textarea 
                className="nodrag"
                value={data.options.custom_input || ''}
                onChange={(e) => data.updateNodeData(data.id, 'options', { custom_input: e.target.value })}
                placeholder="Custom input (use {input} for previous node's output)"
              />
            )}
          </>
        )}
        {data.result && (
          <div className="node-result">
            <strong>Result:</strong>
            <pre>{JSON.stringify(data.result, null, 2)}</pre>
          </div>
        )}
      </div>
      <Handle type="source" position="bottom" isConnectable={isConnectable} />
    </div>
  );
};

const foreignObjectSize = 40;

const ButtonEdge = ({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, style = {}, data }) => {
  const edgePathParams = {
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  };

  const [edgePath] = getBezierPath(edgePathParams);
  const [edgeCenterX, edgeCenterY] = [
    (sourceX + targetX) / 2,
    (sourceY + targetY) / 2
  ];

  const onEdgeClick = (evt) => {
    evt.stopPropagation();
    data.onDelete(id);
  };

  return (
    <>
      <path
        id={id}
        style={style}
        className="react-flow__edge-path"
        d={edgePath}
        markerEnd={getMarkerEnd()}
      />
      <foreignObject
        width={foreignObjectSize}
        height={foreignObjectSize}
        x={edgeCenterX - foreignObjectSize / 2}
        y={edgeCenterY - foreignObjectSize / 2}
        className="edgebutton-foreignobject"
        requiredExtensions="http://www.w3.org/1999/xhtml"
      >
        <button
          className="edgebutton"
          onClick={onEdgeClick}
        >
          ×
        </button>
      </foreignObject>
    </>
  );
};

function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [result, setResult] = useState(null);

  const onConnect = useCallback((params) => {
    const targetHasInput = edges.some(edge => edge.target === params.target);
    if (!targetHasInput) {
      setEdges((eds) => addEdge({ ...params, type: 'buttonedge' }, eds));
    } else {
      alert("A node can only have one input connection.");
    }
  }, [edges, setEdges]);

  const onEdgeDelete = useCallback((edgeId) => {
    setEdges((eds) => eds.filter((edge) => edge.id !== edgeId));
  }, [setEdges]);

  const updateNodeData = useCallback((nodeId, key, value) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === nodeId) {
          if (key === 'options') {
            return {
              ...node,
              data: {
                ...node.data,
                options: {
                  ...node.data.options,
                  ...value
                }
              }
            };
          } else {
            return {
              ...node,
              data: {
                ...node.data,
                [key]: value
              }
            };
          }
        }
        return node;
      })
    );
  }, [setNodes]);

  const createNode = useCallback((label, position) => ({
    id: (nodes.length + 1).toString(),
    type: 'default',
    position,
    data: { 
      id: (nodes.length + 1).toString(),
      label,
      updateNodeData,
      value: '',
      options: {
        dropdown: 'option1',
        input: '',
        toggle: false,
        system_message: '',
        use_custom_input: false,
        custom_input: '',
      }
    },
  }), [nodes.length, updateNodeData]);

  const addNode = useCallback((nodeType) => {
    const newNode = createNode(nodeType, {
      x: Math.random() * (window.innerWidth - 100),
      y: Math.random() * (window.innerHeight - 100) + 100,
    });
    setNodes((nds) => nds.concat(newNode));
  }, [createNode, setNodes]);

  const onExecute = useCallback(() => {
    const pipeline = {
      nodes: nodes.map(node => ({ 
        id: node.id, 
        type: node.data.label,
        value: node.data.value,
        options: node.data.options
      })),
      edges: edges.map(edge => ({ source: edge.source, target: edge.target }))
    };

    axios.post('http://localhost:5000/execute', pipeline)
      .then(response => {
        setResult(response.data);
        setNodes((nds) =>
          nds.map((node) => ({
            ...node,
            data: {
              ...node.data,
              result: response.data[node.id]
            }
          }))
        );
      })
      .catch(error => {
        console.error('Error executing pipeline:', error);
        if (error.response && error.response.data && error.response.data.error) {
          setResult({ error: error.response.data.error });
        } else if (error.request) {
          setResult({ error: "No response received from the server. Please check your connection." });
        } else {
          setResult({ error: "An error occurred while setting up the request: " + error.message });
        }
      });
  }, [nodes, edges, setNodes]);

  const memoizedNodeTypes = useMemo(() => ({ default: NodeTemplate }), []);
  const memoizedEdgeTypes = useMemo(() => ({
    buttonedge: (props) => <ButtonEdge {...props} data={{ onDelete: onEdgeDelete }} />,
  }), [onEdgeDelete]);

  useState(() => {
    const inputNode = createNode('Input Node', { x: 250, y: 125 });
    setNodes([inputNode]);
  }, []);

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <div className="top-bar">
        <div className="node-buttons">
          {Object.keys(NODE_TYPES).map((nodeType) => (
            <button key={nodeType} onClick={() => addNode(nodeType)}>
              Add {nodeType}
            </button>
          ))}
        </div>
        <button className="execute-button" onClick={onExecute}>Execute Pipeline</button>
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={memoizedNodeTypes}
        edgeTypes={memoizedEdgeTypes}
        defaultEdgeOptions={{ type: 'buttonedge' }}
      >
        <Controls />
        <Background color="#aaa" gap={16} />
        <MiniMap />
      </ReactFlow>
      {result && (
        <div className="result-panel">
          <h3>Result:</h3>
          {result.error ? (
            <div style={{ color: 'red' }}>Error: {result.error}</div>
          ) : (
            <pre>{JSON.stringify(result, null, 2)}</pre>
          )}
        </div>
      )}
    </div>
  );
}

export default App;