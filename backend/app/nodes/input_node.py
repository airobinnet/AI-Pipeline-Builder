from .base_node import BaseNode

class Node(BaseNode):
    type = "Input Node"

    def process(self, input_data, options):
        return input_data

    @classmethod
    def get_frontend_config(cls):
        return {
            "type": cls.type,
            "options": []
        }