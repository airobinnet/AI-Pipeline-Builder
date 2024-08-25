from .base_node import BaseNode

class Node(BaseNode):
    type = "Text Analysis"

    def process(self, input_data, options):
        word_count = len(input_data.split())
        char_count = len(input_data)
        return f"Word count: {word_count}, Character count: {char_count}"

    @classmethod
    def get_frontend_config(cls):
        return {
            "type": cls.type,
            "options": []
        }