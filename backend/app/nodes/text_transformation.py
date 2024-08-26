def process(input_data, options):
    if options.get('to_uppercase', False):
        input_data = input_data.upper()
    if options.get('reverse', False):
        input_data = input_data[::-1]
    return input_data

def get_ui_config():
    return {
        "type": "Text Transformation",
        "fields": [
            {
                "name": "to_uppercase",
                "type": "checkbox",
                "label": "To Uppercase"
            },
            {
                "name": "reverse",
                "type": "checkbox",
                "label": "Reverse Text"
            }
        ]
    }