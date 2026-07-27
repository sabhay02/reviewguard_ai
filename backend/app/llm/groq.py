from groq import Groq

from app.utils.configs import settings


class LLMClient:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.1-8b-instant"

    def generate(self, prompt: str, json_mode: bool = False) -> str:

        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert Senior Software Engineer and "
                        "Application Security Engineer."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.2,
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content.strip()
        except Exception as e:
            if hasattr(e, "body") and isinstance(e.body, dict):
                error_info = e.body.get("error", {})
                if error_info.get("code") == "json_validate_failed":
                    return error_info.get("failed_generation", "{}").strip()
            
            print(f"LLM Generation Error: {e}")
            return "{}" if json_mode else ""
            
    def chat(self, messages: list[dict]) -> str:
        """
        Sends a multi-turn conversation to the LLM.
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.4,
        }
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Chat Error: {e}")
            return "I'm sorry, I encountered an error while trying to respond to that."