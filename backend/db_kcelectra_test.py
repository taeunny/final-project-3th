from models.kcelectra_model import Kcelectra
from schemas.db_handler import DBhandler

db_handler = DBhandler()
kcelectra = Kcelectra()

dialog_log = db_handler.select_dialog_log()
label = kcelectra.analyze_sentiment(pd.DataFrame(dialog_log))
db_handler.update_dialog_emotion(label)

if db_handler.select_dialog_log():
    print("인풋 성공함!")
else:
    print("인풋 실패!")