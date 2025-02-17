# AI-Powered IDE

A personal AI-powered IDE built on top of VSCode, leveraging the DeepSeek model for features like autocomplete, code explanations, and refactoring suggestions. The system is containerized, with separate containers for the API and IDE application.

## Features
- **AI Autocomplete**: Real-time code suggestions powered by OpenAI's Assistant API.
- **Code Explanations**: Get detailed explanations for complex code snippets.
- **Refactoring Suggestions**: AI-driven recommendations for code improvements.
- **Chat Interface**: Interact with the AI for coding assistance.

## Architecture
The system consists of two main components:
1. **API Container**: Hosts the DeepSeek model and provides REST/WebSocket endpoints for AI functionalities.
2. **IDE Container**: A customized VSCode instance with AI integration.

## Getting Started
### Prerequisites
- Docker
- Python 3.8+
- Node.js (for IDE development)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-ide.git
   cd ai-ide
   ```

2. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

3. Access the IDE at `http://localhost:8080`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

### Deployment Instructions

1. **Set Environment Variables**:
   ```bash
   echo "OPENAI_API_KEY=your-api-key" > api/app/.env
   ```

2. **Build and Run**:
   ```bash
   docker build -t kscode .
   docker run -p 8000:8000 kscode
   ```

3. **Access the API**:
   The API will be available at `http://localhost:8000`.

4. **Health Check**:
   Verify the API is running by visiting:
   ```bash
   curl http://localhost:8000/health
   ```

5. **Chat Endpoint**:
   Use the `/chat` endpoint to interact with the model:
   ```bash
   curl -X POST "http://localhost:8000/chat" \
   -H "Content-Type: application/json" \
   -d '{"messages": [{"role": "user", "content": "Hello!"}]}'
   ```