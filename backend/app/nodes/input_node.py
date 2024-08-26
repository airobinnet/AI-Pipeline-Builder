def process(input_data, options):
    return options.get('value', '')

def get_ui_config():
    return {
        "type": "Input Node",
        "fields": [
            {
                "name": "value",
                "type": "text",
                "label": "Input",
                "placeholder": "Enter input"
            }
        ]
    }