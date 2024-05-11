from transformers import pipeline
import torch

device = 0 if torch.cuda.is_available() else -1
model = "KoJLabs/bart-speech-style-converter"
speech_style_converter = pipeline('text2text-generation', model=model, tokenizer=model, device=device)   
