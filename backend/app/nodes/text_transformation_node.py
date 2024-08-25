from .base_node import BaseNode

class Node(BaseNode):
    type = "Text Transformation"

    def process(self, input_data, options):
        if options.get('to_uppercase', False):
            input_data = input_data.upper()
        if options.get('reverse', False):
            input_data = input_data[::-1]
        return input_data

    @classmethod
    def get_frontend_config(cls):
        return {
            "type": cls.type,
            "options": [
                {"name": "to_uppercase", "type": "checkbox", "label": "To Uppercase"},
                {"name": "reverse", "type": "checkbox", "label": "Reverse Text"}
            ]
        }