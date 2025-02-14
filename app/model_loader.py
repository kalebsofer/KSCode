import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from threading import Lock
from typing import List


class ModelLoader:
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.lock = Lock()  # Add a lock for thread safety

    def load_model(self):
        if self.model is None:
            print(f"Loading model from {self.model_path}...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                use_safetensors=True,
            )
            print("Model loaded successfully!")

    def generate_chat(self, messages: List[dict], max_tokens=512, temperature=0.7):
        if self.model is None:
            self.load_model()

        with self.lock:
            # Format the conversation history
            formatted_conversation = self._format_conversation(messages)

            inputs = self.tokenizer(formatted_conversation, return_tensors="pt").to(
                self.device
            )
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _format_conversation(self, messages: List[dict]) -> str:
        """Format conversation history into a single string"""
        formatted = []
        for msg in messages:
            if msg["role"] == "user":
                formatted.append(f"User: {msg['content']}")
            elif msg["role"] == "assistant":
                formatted.append(f"Assistant: {msg['content']}")
        return "\n".join(formatted)
