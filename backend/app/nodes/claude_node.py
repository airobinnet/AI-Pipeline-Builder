import os
import asyncio
from anthropic import Anthropic, AsyncAnthropic

sync_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
async_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_text(content):
    if isinstance(content, list):
        return ' '.join([extract_text(item) for item in content])
    elif isinstance(content, dict):
        return content.get('text', '')
    elif hasattr(content, 'type') and hasattr(content, 'text'):
        return content.text
    else:
        return str(content)

async def async_claude_function(input_data, options):
    try:
        if options.get('use_custom_input', False):
            custom_input = options.get('custom_input', '')
            input_data = custom_input.replace('{input}', input_data)
        max_tokens = int(options.get('max_tokens', 1024))
        model = options.get('model', 'claude-3-opus-20240229')
        system_message = options.get('system_message', "You are a helpful assistant.")

        response = await async_client.messages.create(
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": input_data
                }
            ],
            model=model,
            system=system_message
        )
        return extract_text(response.content)
    except Exception as e:
        return f"Error: {str(e)}"

def sync_claude_function(input_data, options):
    try:
        max_tokens = int(options.get('max_tokens', 1024))
        model = options.get('model', 'claude-3-opus-20240229')
        system_message = options.get('system_message', "You are a helpful assistant.")

        response = sync_client.messages.create(
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": input_data
                }
            ],
            model=model,
            system=system_message
        )
        return extract_text(response.content)
    except Exception as e:
        return f"Error: {str(e)}"

def process(input_data, options):
    return sync_claude_function(input_data, options)

async def async_process(input_data, options):
    result = await async_claude_function(input_data, options)
    yield result

def get_ui_config():
    return {
        "type": "Claude Node",
        "fields": [
            {
                "name": "model",
                "type": "select",
                "label": "Model",
                "options": [
                    {"value": "claude-3-5-sonnet-20240620", "label": "Claude 3.5 Sonnet"},
                    {"value": "claude-3-opus-20240229", "label": "Claude 3 Opus"},
                    {"value": "claude-3-sonnet-20240229", "label": "Claude 3 Sonnet"},
                    {"value": "claude-3-haiku-20240307", "label": "Claude 3 Haiku"},
                    {"value": "claude-2.1", "label": "Claude 2.1"}
                ]
            },
            {
                "name": "max_tokens",
                "type": "number",
                "label": "Max Tokens",
                "default": 1024
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