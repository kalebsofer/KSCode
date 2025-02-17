import os
import logging
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from schemas import ChatMessage

load_dotenv()

logger = logging.getLogger(__name__)


class OpenAIAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant_id = self._create_or_get_assistant()
        self.thread_id = self.client.beta.threads.create().id
        logger.info("OpenAI Assistant initialized")

    def _create_or_get_assistant(self):
        assistants = self.client.beta.assistants.list()
        for assistant in assistants.data:
            if assistant.name == "Code Editor Assistant":
                return assistant.id

        instructions = (
            "You are a code editor assistant. Help users with code completion, "
            "explanations, and refactoring."
        )
        assistant = self.client.beta.assistants.create(
            name="Code Editor Assistant",
            instructions=instructions,
            model="gpt-4-0125-preview",
            tools=[{"type": "code_interpreter"}],
        )
        return assistant.id

    def generate_chat(
        self, messages: List[ChatMessage], max_tokens=512, temperature=0.7
    ):
        try:
            for msg in messages:
                self.client.beta.threads.messages.create(
                    thread_id=self.thread_id, role=msg.role, content=msg.content
                )

            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
            )

            while run.status != "completed":
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id, run_id=run.id
                )

            messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            return messages.data[0].content[0].text.value
        except Exception as e:
            logger.error(f"OpenAI Assistant error: {str(e)}")
            raise
