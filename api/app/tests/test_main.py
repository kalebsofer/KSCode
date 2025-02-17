import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from main import ChatRequest, ChatMessage
from model_loader import OpenAIAssistant


def main():
    client = OpenAIAssistant()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        request = ChatRequest(messages=[ChatMessage(role="user", content=user_input)])

        response = client.generate_chat(
            request.messages, max_tokens=512, temperature=0.6
        )

        print(f"Assistant: {response}")


if __name__ == "__main__":
    main()
