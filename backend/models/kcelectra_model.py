from transformers import pipeline
import torch

device = 0 if torch.cuda.is_available() else -1
model_name = "nlp04/korean_sentiment_analysis_kcelectra"
sentiment_analyzer = pipeline('sentiment-analysis', model=model_name, tokenizer=model_name, device=device)
