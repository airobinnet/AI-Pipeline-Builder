import os
from openai import OpenAI, AsyncOpenAI
import asyncio

sync_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def async_gpt_function(input_data, options):
    try:
        if options.get('use_custom_input', False):
            custom_input = options.get('custom_input', '')
            input_data = custom_input.replace('{input}', input_data)

        chat_completion = await async_client.chat.completions.create(
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

def sync_gpt_function(input_data, options):
    try:
        if options.get('use_custom_input', False):
            custom_input = options.get('custom_input', '')
            input_data = custom_input.replace('{input}', input_data)

        chat_completion = sync_client.chat.completions.create(
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

def process(input_data, options):
    return sync_gpt_function(input_data, options)

async def async_process(input_data, options):
    return await async_gpt_function(input_data, options)

def get_ui_config():
    return {
        "type": "GPT Node",
        "fields": [
            {
                "name": "model",
                "type": "select",
                "label": "Model",
                "options": [
                    {"value": "gpt-4o", "label": "GPT-4o"},
                    {"value": "gpt-4o-mini", "label": "GPT-4o-mini"},
                    {"value": "gpt-4-turbo", "label": "GPT-4-turbo"},
                    {"value": "gpt-3.5-turbo", "label": "GPT-3.5-turbo"},
                ]
            },
            {
                "name": "max_tokens",
                "type": "number",
                "label": "Max Tokens",
                "default": 150
            },
            {
                "name": "temperature",
                "type": "number",
                "label": "Temperature",
                "default": 0.7,
                "step": 0.1,
                "min": 0,
                "max": 1
            },
            {
                "name": "system_message",
                "type": "textarea",
                "label": "System Message",
                "placeholder": "You are a helpful assistant."
            },
            {
                "name": "use_custom_input",
                "type": "checkbox",
                "label": "Use Custom Input"
            },
            {
                "name": "custom_input",
                "type": "textarea",
                "label": "Custom Input",
                "placeholder": "Custom input (use {input} for previous node's output)",
                "condition": {"field": "use_custom_input", "value": True}
            }
        ]
    }