def process(input_data, options):
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

def get_ui_config():
    return {
        "type": "Sentiment Analysis",
        "fields": []
    }