import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from main import app, get_model_loader, ChatRequest, ChatMessage


def main():
    # Load the model
    model_loader = get_model_loader()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Create a chat request
        request = ChatRequest(messages=[ChatMessage(role="user", content=user_input)])

        # Simulate the API call
        response = model_loader.generate_chat(
            request.messages, max_tokens=512, temperature=0.6
        )

        print(f"Assistant: {response}")


if __name__ == "__main__":
    main()
