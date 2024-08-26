def process(input_data, options):
    word_count = len(input_data.split())
    char_count = len(input_data)
    return f"Word count: {word_count}, Character count: {char_count}"

def get_ui_config():
    return {
        "type": "Text Analysis",
        "fields": []
    }