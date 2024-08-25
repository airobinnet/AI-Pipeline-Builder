from abc import ABC, abstractmethod

class BaseNode(ABC):
    type = "base"

    @abstractmethod
    def process(self, input_data, options):
        pass

    @classmethod
    def get_frontend_config(cls):
        return {
            "type": cls.type,
            "options": []
        }