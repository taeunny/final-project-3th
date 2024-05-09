"""
MySql DB 연결 및 쿼리 실행 모듈
"""

import pymysql
from datetime import datetime
import time
from pytz import timezone
import traceback
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd

## .env ##
load_dotenv(find_dotenv())  # 환경변수 로드

class DBhandler:
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST"), 
            user=os.getenv("DB_USER"), 
            password=os.getenv("DB_PASSWORD"), 
            charset="utf8"
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("USE mentos;")  # mentos 스키마 접근

    def create_user(self, user_id):
        try:
            self.cursor.execute(
                f"INSERT INTO mentos.user (user_id) VALUES ({user_id});"
            )
            return True
        except:
            print(traceback.format_exc())
            return False


    def create_dialog_message(
        self, u_message, ai_message
    ):  # dialog Table INSERT DATA(user_message(인풋), ai_message(아웃풋))
        try:
            self.cursor.execute(
                "INSERT INTO mentos.dialog (dt_dialog, u_message, ai_message) VALUES (%s, %s, NOW();)", (u_message, ai_message)
            )
            return True
        except:
            print(traceback.format_exc())
            return False


    def update_dialog_emotion(self, df):
        try:
            for index, row in df.iterrows():
                dialog_id = row['dialog_id']
                emotion = row['label']
                self.cursor.execute(
                    "UPDATE dialog SET dialog_emotion = %s WHERE dialog_id = %s",
                    (emotion, dialog_id)
                )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating dialog emotion: {e}")
            self.connection.rollback()
            return False

    def create_emotion_log(self, input_message):  # emotion_log Table
        try:
            self.cursor.execute(
                f"INSERT INTO mentos.emotion_log (counsel_emotion, dt_emotion_log) VALUES ({input_message}, NOW();)"
            )
            #    ({input_message}, {time.strftime("%Y-%m-%d %H:%M:%S")})
            self.db.commit()
            self.db.close()
            return True
        except:
            print(traceback.format_exc())
            return False


    def select_dialog_log(self):  # dialog Table u_message 조회
        try:
            self.cursor.execute("SELECT dialog_id, u_message FROM dialog;")
            result = self.cursor.fetchall()
            return result

        except:
            print(traceback.extract_exc())
            return False

    def close_connection(self):
        self.connection.close()


# if __name__ == "__main__":
#     from kcelectra_model import Kcelectra

#     db_handler = DBhandler()
#     kcelectra = Kcelectra()

#     dialog_log = db_handler.select_dialog_log()
#     label = kcelectra.analyze_sentiment(pd.DataFrame(dialog_log))
#     db_handler.update_dialog_emotion(label)

#     if db_handler.select_dialog_log():
#         print("인풋 성공함!")
#     else:
#         print("인풋 실패!")
