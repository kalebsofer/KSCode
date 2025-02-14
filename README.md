# AI-Powered IDE (Cursor AI Clone)

This project is a custom AI-powered IDE built on top of VSCode, leveraging the DeepSeek model for AI-driven features like autocomplete, code explanations, and refactoring suggestions. The system is containerized, with separate containers for the API and IDE application.

## Features
- **AI Autocomplete**: Real-time code suggestions powered by DeepSeek.
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