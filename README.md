# AI Pipeline Builder

[![GitHub license](https://img.shields.io/github/license/airobinnet/AI-Pipeline-Builder.svg)](https://github.com/airobinnet/AI-Pipeline-Builder/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/airobinnet/AI-Pipeline-Builder.svg)](https://github.com/airobinnet/AI-Pipeline-Builder/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/airobinnet/AI-Pipeline-Builder.svg)](https://github.com/airobinnet/AI-Pipeline-Builder/issues)

AI Pipeline Builder is a flexible and extensible platform for creating and executing AI pipelines. It allows users to visually construct workflows by connecting various AI nodes, including text processing, image generation, and language models.

## Features

- Visual pipeline builder with drag-and-drop interface
- Support for various AI nodes (GPT, DALL-E, FLUX, Claude, etc.)
- Real-time pipeline execution
- Asynchronous processing for improved performance
- Extensible architecture for adding custom nodes
- Debug panel for monitoring pipeline execution

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/airobinnet/ai-pipeline-builder.git
   cd ai-pipeline-builder
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Create a `.env` file in the `backend` directory and add your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python run.py
   ```

2. In a new terminal, start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000` to use the AI Pipeline Builder.

## Usage

1. Use the buttons in the top bar to add nodes to your pipeline.
2. Connect nodes by dragging from one node's output handle to another node's input handle.
3. Configure node options in the node panels.
4. Click the "Execute Pipeline" button to run the entire pipeline, or use the play button on individual nodes to execute from that point.
5. View results in the node panels and the debug panel (if enabled).

## Creating Custom Nodes

The AI Pipeline Builder supports custom nodes, allowing you to extend its functionality. To create a new node:

1. Create a new Python file in the `backend/app/nodes/` directory.
2. Implement the required functions: `process`, `async_process` (optional), and `get_ui_config`.
3. The new node will be automatically detected and included in the application.

For detailed instructions on creating custom nodes, please refer to our [Node Creator Guide](docs/node-tutorial.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [React Flow](https://reactflow.dev/) for the visual graph editor
- [OpenAI](https://openai.com/) for GPT and DALL-E APIs
- [Anthropic](https://www.anthropic.com/) for Claude API