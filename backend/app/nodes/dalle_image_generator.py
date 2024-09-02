# backend/app/nodes/dalle_image_generator.py

import os
from openai import OpenAI

def process(input_data, options):
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print(f"DALL-E received input_data: {input_data}")
    print(f"DALL-E received options: {options}")
    # Prepare the request parameters
    params = {
        "model": "dall-e-3",
        "prompt": options.get("prompt", input_data),
        "n": 1,
        "size": options.get("size", "1024x1024"),
        "quality": options.get("quality", "standard"),
        "style": options.get("style", "vivid"),
    }

    # if prompt contains {input}, replace it with the actual input data
    if "{input}" in params["prompt"]:
        params["prompt"] = params["prompt"].replace("{input}", input_data)

    # Generate the image
    try:
        response = client.images.generate(**params)
        # Return the URL of the generated image
        return response.data[0].url
    except Exception as e:
        return f"Error generating image: {str(e)}"

def get_ui_config():
    return {
        "type": "DALL-E Image Generator",
        "fields": [
            {
                "name": "prompt",
                "type": "textarea",
                "label": "Image Prompt",
                "placeholder": "{input}",
                "default": ""
            },
            {
                "name": "size",
                "type": "select",
                "label": "Image Size",
                "options": ["1024x1024", "1792x1024", "1024x1792"],
                "default": "1024x1024"
            },
            {
                "name": "quality",
                "type": "select",
                "label": "Image Quality",
                "options": ["standard", "hd"],
                "default": "standard"
            },
            {
                "name": "style",
                "type": "select",
                "label": "Image Style",
                "options": ["vivid", "natural"],
                "default": "vivid"
            }
        ]
    }