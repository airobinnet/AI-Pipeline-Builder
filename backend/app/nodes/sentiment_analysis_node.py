from .base_node import BaseNode

class Node(BaseNode):
    type = "Sentiment Analysis"

    def process(self, input_data, options):
        positive_words = set(['good', 'great', 'excellent', 'happy', 'positive'])
        negative_words = set(['bad', 'awful', 'terrible', 'sad', 'negative'])
        
        words = input_data.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Negative"
        else:
            return "Neutral"

    @classmethod
    def get_frontend_config(cls):
        return {
            "type": cls.type,
            "options": []
        }