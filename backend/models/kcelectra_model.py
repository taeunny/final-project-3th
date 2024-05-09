# !pip install transformers

from transformers import ElectraTokenizer, ElectraForSequenceClassification, pipeline
import torch


class Kcelectra:
    device = 0 if torch.cuda.is_available() else -1
    model_name = "nlp04/korean_sentiment_analysis_kcelectra"
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model=model_name,
        tokenizer=model_name,
        device=device
    )

    @staticmethod
    def analyze_sentiment(message):
        if not message:  # Handle None or empty string
            return None
        try:
            print(f"kcelectra.message: {message}")
            result = Kcelectra.sentiment_analyzer(message)[0]
            print(f"result: {result}")
            return result["label"]
        except Exception as e:
            print(f"Error processing text: {e}")
            return None

    def check_device(self):
        print("Using GPU." if self.device == 0 else "Using CPU.")