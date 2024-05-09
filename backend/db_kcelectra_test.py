from models.kcelectra_model import Kcelectra
from schemas.db_handler import DBhandler
import pandas as pd

db_handler = DBhandler()
dialog_log = db_handler.select_dialog_log()
print(dialog_log)
dialog_texts = [(item[0], item[1]) for item in dialog_log] if dialog_log else []
df = pd.DataFrame(dialog_texts, columns=['dialog_id', 'messages'])

print('DataFrame content:', df)

# Apply sentiment analysis
df['label'] = df['messages'].apply(Kcelectra.analyze_sentiment)
print(df)
# label = kcelectra.analyze_sentiment(df)
# print(f"label: {label}")
# db_handler.update_dialog_emotion(label)
if db_handler.update_dialog_emotion(df):
    print("Emotion update successful!")
else:
    print("Failed to update emotions.")

if db_handler.select_dialog_log():
    print("인풋 성공함!")
else:
    print("인풋 실패!")