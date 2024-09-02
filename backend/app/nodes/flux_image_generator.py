# backend/app/nodes/flux_image_generator.py

import torch
from diffusers import FluxPipeline
import io
import base64
from PIL import Image
import os
import asyncio

# Load the FLUX pipeline
pipe = FluxPipeline.from_pretrained(
    "C:\\Projects\\flux1\\",  # Update this path to your local FLUX model
    torch_dtype=torch.bfloat16,
)
pipe.enable_sequential_cpu_offload()

def process(input_data, options):
    # This function is required but not used
    return "FLUX Image Generator does not support synchronous processing"

async def async_process(input_data, options):
    prompt = options.get("prompt", input_data)
    guidance_scale = float(options.get("guidance_scale", 4.0))
    num_inference_steps = int(options.get("num_inference_steps", 6))
    height = int(options.get("height", 1024))
    width = int(options.get("width", 1024))
    seed = options.get("seed")

    if seed is not None and seed != "random":
        generator = torch.Generator("cpu").manual_seed(int(seed))
    else:
        generator = torch.Generator("cpu").manual_seed(torch.randint(0, 1000000, (1,)).item())

    try:
        # Run the pipeline
        result = pipe(
            prompt,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator,
            output_type="pil",
        )

        # Final image
        final_image = result.images[0]
        buffered = io.BytesIO()
        final_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        yield {
            "image": f"data:image/png;base64,{img_str}",
            "is_final": True
        }

    except Exception as e:
        print(f"Error in FLUX generator: {str(e)}")
        yield {"error": str(e)}

def get_ui_config():
    return {
        "type": "FLUX Image Generator",
        "description": "Generates images using the FLUX model",
        "fields": [
            {
                "name": "prompt",
                "type": "textarea",
                "label": "Image Prompt",
                "placeholder": "{input}",
                "default": ""
            },
            {
                "name": "guidance_scale",
                "type": "number",
                "label": "Guidance Scale",
                "default": 4.0,
                "min": 0,
                "max": 20,
                "step": 0.1
            },
            {
                "name": "num_inference_steps",
                "type": "number",
                "label": "Inference Steps",
                "default": 6,
                "min": 1,
                "max": 100,
                "step": 1
            },
            {
                "name": "height",
                "type": "number",
                "label": "Height",
                "default": 1024,
                "min": 256,
                "max": 1024,
                "step": 64
            },
            {
                "name": "width",
                "type": "number",
                "label": "Width",
                "default": 1024,
                "min": 256,
                "max": 1024,
                "step": 64
            },
            {
                "name": "seed",
                "type": "text",
                "label": "Seed",
                "placeholder": "random",
                "default": "random"
            }
        ]
    }