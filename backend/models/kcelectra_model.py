# !pip install transformers

from transformers import ElectraTokenizer, ElectraForSequenceClassification, pipeline
import torch


class Kcelectra:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.model_name = "nlp04/korean_sentiment_analysis_kcelectra"
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model=self.model_name,
            tokenizer=self.model_name,
            device=self.device,
        )

        self.kcelectra = Kcelectra()

    def analyze_sentiment(self, message):
        try:
            result = self.sentiment_analyzer(message)[0]
            return result["label"]  # [, , , , ,]
        except Exception as e:
            print(f"Error processing text: {e}")
            return None

    # def apply_analyze_sentiment(self, result_kcelectra):
    #     try:
    #         self.db_handler.select_dialog_log().apply(
    #             self.kcelectra.analyze_sentiment
    #         )  # 꺄아아아악!!!!!!!
    #     except Exception as e:
    #         print(f"Error processing text: {e}")
    #         return None

    def check_device(self):
        # CUDA 사용 가능 여부 확인
        print("Using GPU." if self.device == 0 else "Using CPU.")
