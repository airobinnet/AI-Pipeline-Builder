import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
from .base_node import BaseNode

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Node(BaseNode):
    type = "GPT Node"

    async def async_process(self, input_data, options):
        try:
            if options.get('use_custom_input', False):
                custom_input = options.get('custom_input', '')
                input_data = custom_input.replace('{input}', input_data)

            chat_completion = await client.chat.completions.create(
                model=options.get('model', 'gpt-4'),
                messages=[
                    {"role": "system", "content": options.get('system_message', "You are a helpful assistant.")},
                    {"role": "user", "content": input_data}
                ],
                max_tokens=int(options.get('max_tokens', 150)),
                temperature=float(options.get('temperature', 0.7))
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def process(self, input_data, options):
        return asyncio.run(self.async_process(input_data, options))

    @classmethod
    def get_frontend_config(cls):
        return {
            "type": cls.type,
            "options": [
                {"name": "model", "type": "select", "label": "Model", "choices": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"], "default": "gpt-4"},
                {"name": "max_tokens", "type": "number", "label": "Max Tokens", "default": 150, "min": 1, "max": 4096},
                {"name": "temperature", "type": "number", "label": "Temperature", "default": 0.7, "min": 0, "max": 1, "step": 0.1},
                {"name": "system_message", "type": "textarea", "label": "System Message"},
                {"name": "use_custom_input", "type": "checkbox", "label": "Use Custom Input"},
                {"name": "custom_input", "type": "textarea", "label": "Custom Input"}
            ]
        }