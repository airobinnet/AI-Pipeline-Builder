import React, { useState, useCallback, useMemo, useEffect, useRef } from 'react';
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
import { ThreeDots } from 'react-loader-spinner';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import 'reactflow/dist/style.css';
import './App.css';

const NodeTemplate = ({ data, isConnectable }) => {
  const nodeType = data.type;

  const handlePlayClick = () => {
    console.log("Play button clicked for node:", data.id);
    data.onExecuteFromNode(data.id);
  };

  const renderField = (field) => {
    switch (field.type) {
      case 'text':
      case 'number':
        return (
          <input 
            className="nodrag"
            type={field.type}
            value={data.options[field.name] || field.default || ''}
            onChange={(e) => data.updateNodeData(data.id, 'options', { [field.name]: e.target.value })}
            placeholder={field.placeholder}
            step={field.step}
            min={field.min}
            max={field.max}
          />
        );
      case 'checkbox':
        return (
          <label className="nodrag">
            <input 
              type="checkbox" 
              checked={data.options[field.name] || false}
              onChange={(e) => data.updateNodeData(data.id, 'options', { [field.name]: e.target.checked })}
            />
            {field.label}
          </label>
        );
      case 'select':
        return (
          <select 
            className="nodrag"
            value={data.options[field.name] || field.default}
            onChange={(e) => data.updateNodeData(data.id, 'options', { [field.name]: e.target.value })}
          >
            {field.options.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        );
      case 'textarea':
        return (
          <textarea 
            className="nodrag"
            value={data.options[field.name] || ''}
            onChange={(e) => data.updateNodeData(data.id, 'options', { [field.name]: e.target.value })}
            placeholder={field.placeholder}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className={`node ${nodeType.replace(/\s+/g, '-').toLowerCase()}`}>
      {nodeType !== 'Input Node' && <Handle type="target" position="top" isConnectable={isConnectable} />}
      <div className="node-header">
        {nodeType}
        <button className="play-button" onClick={handlePlayClick}>▶</button>
      </div>
      <div className="node-content">
        {data.fields.map(field => (
          <div key={field.name}>
            {field.condition ? (
              data.options[field.condition.field] === field.condition.value && renderField(field)
            ) : (
              renderField(field)
            )}
          </div>
        ))}
        {data.isLoading && (
          <div className="node-loading">
            <ThreeDots color="#00BFFF" height={50} width={50} />
          </div>
        )}
        {data.result !== undefined && !data.isLoading && (
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
  const [nodeTypes, setNodeTypes] = useState({});
  const [isInitialized, setIsInitialized] = useState(false);
  const [debugResults, setDebugResults] = useState([]);
  const [showDebug, setShowDebug] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);
  
  // Use a ref to store the latest nodes and edges
  const nodesRef = useRef(nodes);
  const edgesRef = useRef(edges);

  // Update the refs whenever nodes or edges change
  useEffect(() => {
    nodesRef.current = nodes;
    edgesRef.current = edges;
  }, [nodes, edges]);

  useEffect(() => {
    axios.get('http://localhost:5000/node-types')
      .then(response => {
        setNodeTypes(response.data);
      })
      .catch(error => {
        console.error('Error fetching node types:', error);
      });
  }, []);

  const onConnect = useCallback((params) => {
    const targetHasInput = edgesRef.current.some(edge => edge.target === params.target);
    if (!targetHasInput) {
      setEdges((eds) => addEdge({ ...params, type: 'buttonedge' }, eds));
    } else {
      alert("A node can only have one input connection.");
    }
  }, [setEdges]);

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

  const executeFromNode = useCallback((startNodeId) => {
    if (isExecuting) {
      console.log("Execution already in progress");
      return;
    }
  
    setIsExecuting(true);
    setDebugResults([]);
  
    console.log("Starting execution from node:", startNodeId);
    console.log("All nodes:", nodesRef.current);
    console.log("All edges:", edgesRef.current);
  
    // Find all nodes that need to be executed
    const nodesToExecute = new Set();
    const edgesToInclude = new Set();
    const queue = [startNodeId];
    
    // Find the input for the start node
    const incomingEdge = edgesRef.current.find(edge => edge.target === startNodeId);
    let startNodeInput = '';
    if (incomingEdge) {
      const sourceNode = nodesRef.current.find(node => node.id === incomingEdge.source);
      if (sourceNode && sourceNode.data.result !== undefined) {
        startNodeInput = sourceNode.data.result;
      }
    }
    
    while (queue.length > 0) {
      const currentNodeId = queue.shift();
      console.log("Processing node:", currentNodeId);
      if (!nodesToExecute.has(currentNodeId)) {
        nodesToExecute.add(currentNodeId);
        console.log("Added node to execute:", currentNodeId);
        
        // Find outgoing edges and add them to edgesToInclude
        edgesRef.current.forEach(edge => {
          if (edge.source === currentNodeId) {
            edgesToInclude.add(edge.id);
            queue.push(edge.target);
            console.log("Added edge:", edge.id, "and queued node:", edge.target);
          }
        });
      }
    }
  
    console.log("Nodes to execute:", Array.from(nodesToExecute));
    console.log("Edges to include:", Array.from(edgesToInclude));
  
    // Set loading state for nodes to be executed
    setNodes((nds) =>
      nds.map((node) => ({
        ...node,
        data: {
          ...node.data,
          isLoading: nodesToExecute.has(node.id),
          result: nodesToExecute.has(node.id) ? undefined : node.data.result
        }
      }))
    );
  
    // Prepare the pipeline configuration
    const pipeline = {
      nodes: nodesRef.current
        .filter(node => nodesToExecute.has(node.id))
        .map(node => ({ 
          id: node.id, 
          type: node.data.type,
          options: node.data.options,
          input: node.id === startNodeId ? startNodeInput : undefined
        })),
      edges: edgesRef.current.filter(edge => edgesToInclude.has(edge.id)),
      startNodeId: startNodeId
    };
  
    console.log('Pipeline configuration:', pipeline);
  
    // Check if there are nodes to execute
    if (pipeline.nodes.length === 0) {
      console.error('No nodes to execute');
      setIsExecuting(false);
      alert('No nodes to execute. Please check your pipeline configuration.');
      return;
    }
  
    axios.post('http://localhost:5000/start-pipeline', pipeline)
      .then(() => {
        const eventSource = new EventSource('http://localhost:5000/execute');
  
        eventSource.onopen = (event) => {
          console.log("Connection to server opened.");
        };
  
        eventSource.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.error) {
            console.error('Pipeline execution error:', data.error);
            alert(`Pipeline execution error: ${data.error}`);
            setIsExecuting(false);
            eventSource.close();
            return;
          }
          setNodes((nds) =>
            nds.map((node) => {
              if (node.id === data.id) {
                return {
                  ...node,
                  data: {
                    ...node.data,
                    isLoading: false,
                    result: data.result
                  }
                };
              }
              return node;
            })
          );
          setDebugResults((prev) => [...prev, { id: data.id, result: data.result }]);
        };
  
        eventSource.onerror = (error) => {
          console.log('EventSource ended or errored:', error);
          eventSource.close();
          setIsExecuting(false);
          setNodes((nds) =>
            nds.map((node) => ({
              ...node,
              data: {
                ...node.data,
                isLoading: false
              }
            }))
          );
        };
  
        return () => {
          eventSource.close();
        };
      })
      .catch((error) => {
        console.error('Failed to start pipeline:', error);
        setIsExecuting(false);
        setNodes((nds) =>
          nds.map((node) => ({
            ...node,
            data: {
              ...node.data,
              isLoading: false
            }
          }))
        );
        alert('Failed to start pipeline execution. Please try again.');
      });
  }, [setNodes, isExecuting]);

  const createNode = useCallback((nodeType, position) => {
    const nodeId = uuidv4();
    return {
      id: nodeId,
      type: 'default',
      position,
      data: { 
        id: nodeId,
        type: nodeType,
        updateNodeData,
        onExecuteFromNode: executeFromNode,
        options: {},
        fields: nodeTypes[nodeType].fields,
      },
    };
  }, [updateNodeData, nodeTypes, executeFromNode]);

  const addNode = useCallback((nodeType) => {
    const newNode = createNode(nodeType, {
      x: Math.random() * (window.innerWidth - 100),
      y: Math.random() * (window.innerHeight - 100) + 100,
    });
    setNodes((nds) => nds.concat(newNode));
  }, [createNode, setNodes]);

  const onExecute = useCallback(() => {
    if (nodesRef.current.length > 0) {
      executeFromNode(nodesRef.current[0].id);
    } else {
      alert("No nodes in the pipeline to execute.");
    }
  }, [executeFromNode]);

  const toggleDebug = useCallback(() => {
    setShowDebug(prev => !prev);
  }, []);

  const memoizedNodeTypes = useMemo(() => ({ default: NodeTemplate }), []);
  const memoizedEdgeTypes = useMemo(() => ({
    buttonedge: (props) => <ButtonEdge {...props} data={{ onDelete: onEdgeDelete }} />,
  }), [onEdgeDelete]);

  useEffect(() => {
    if (Object.keys(nodeTypes).length > 0 && !isInitialized) {
      const inputNode = createNode('Input Node', { x: 250, y: 125 });
      setNodes([inputNode]);
      setIsInitialized(true);
    }
  }, [nodeTypes, createNode, setNodes, isInitialized]);

  return (
    <div className="app-container">
      <div className="top-bar">
        <div className="node-buttons">
          {Object.keys(nodeTypes).map((nodeType) => (
            <button key={nodeType} onClick={() => addNode(nodeType)}>
              Add {nodeType}
            </button>
          ))}
        </div>
        <div className="control-buttons">
          <button className="execute-button" onClick={onExecute} disabled={isExecuting}>
            {isExecuting ? 'Executing...' : 'Execute Pipeline'}
          </button>
          <button className="debug-button" onClick={toggleDebug}>
            {showDebug ? 'Hide Debug' : 'Show Debug'}
          </button>
        </div>
      </div>
      <div className="react-flow-container">
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
        {showDebug && debugResults.length > 0 && (
          <div className="debug-panel">
            <h3>Debug Results:</h3>
            <pre>{JSON.stringify(debugResults, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;