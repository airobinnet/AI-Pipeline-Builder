# Pipeline Node Creator Guide

This guide explains how to create custom nodes for the pipeline application. By following these steps, you can extend the functionality of the application with your own custom nodes.

## Table of Contents

1. [Node Structure](#node-structure)
2. [Creating a New Node](#creating-a-new-node)
3. [Node Functions](#node-functions)
4. [UI Configuration](#ui-configuration)
5. [Adding the Node to the Application](#adding-the-node-to-the-application)
6. [Example Node](#example-node)

## Node Structure

Each node is defined in a separate Python file located in the `backend/app/nodes/` directory. The file should contain the following key components:

- A `process` function that handles the node's main logic
- An `async_process` function for asynchronous processing (optional)
- A `get_ui_config` function that defines the node's UI elements

## Creating a New Node

1. Create a new Python file in the `backend/app/nodes/` directory. Name it according to your node's functionality (e.g., `text_analyzer.py`).

2. In this file, define the required functions as described in the [Node Functions](#node-functions) section.

## Node Functions

### `process` Function

This function handles the main logic of your node. It should take two parameters:

- `input_data`: The input data from the previous node(s)
- `options`: A dictionary containing the node's configuration options

Example:

```python
def process(input_data, options):
    # Your node logic here
    result = do_something(input_data, options)
    return result
```

### `async_process` Function (Optional)

If your node requires asynchronous processing, define this function. It should be similar to the `process` function but async:

```python
async def async_process(input_data, options):
    # Your async node logic here
    result = await do_something_async(input_data, options)
    return result
```

### `get_ui_config` Function

This function defines the UI configuration for your node. It should return a dictionary with the following structure:

```python
def get_ui_config():
    return {
        "type": "Your Node Type",
        "fields": [
            {
                "name": "field_name",
                "type": "field_type",
                "label": "Field Label",
                "default": "default_value",
                "options": [...],  # For select fields
                "placeholder": "Placeholder text",
                "condition": {...}  # For conditional fields
            },
            # More fields...
        ]
    }
```

## UI Configuration

The `fields` list in the UI configuration supports the following field types:

- `"text"`: A single-line text input
- `"number"`: A number input
- `"checkbox"`: A checkbox input
- `"select"`: A dropdown select input
- `"textarea"`: A multi-line text input

Each field can have the following properties:

- `name`: The internal name of the field (required)
- `type`: The type of the field (required)
- `label`: The display label for the field (required)
- `default`: The default value for the field (optional)
- `options`: A list of options for select fields (required for select fields)
- `placeholder`: Placeholder text for text and textarea fields (optional)
- `condition`: A condition object for conditional fields (optional)

## Adding the Node to the Application

Once you've created your node file, the application will automatically detect and include it. No additional steps are required to integrate the node into the system.

## Example Node

Here's an example of a simple text analysis node:

```python
# backend/app/nodes/text_analyzer.py

def process(input_data, options):
    word_count = len(input_data.split())
    char_count = len(input_data)
    
    if options.get('include_spaces', False):
        space_count = input_data.count(' ')
        return f"Word count: {word_count}, Character count: {char_count}, Space count: {space_count}"
    else:
        return f"Word count: {word_count}, Character count: {char_count}"

def get_ui_config():
    return {
        "type": "Text Analyzer",
        "fields": [
            {
                "name": "include_spaces",
                "type": "checkbox",
                "label": "Include space count",
                "default": False
            }
        ]
    }
```

This node analyzes input text and returns word and character counts. It also has an option to include space count in the analysis.

---

By following this guide, you can create custom nodes that seamlessly integrate with the pipeline application, extending its functionality to suit your specific needs.