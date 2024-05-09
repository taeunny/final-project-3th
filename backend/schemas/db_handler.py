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

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


class DBhandler:
    def __init__(self):
        self.db = pymysql.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, charset="utf8"
        )
        self.cursor = self.db.cursor()
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
        finally:
            # self.db.commit()
            self.cursor.close()
            self.db.close()

    def create_dialog_message(
        self, u_message, ai_message
    ):  # dialog Table INSERT DATA(user_message(인풋), ai_message(아웃풋))
        try:
            self.cursor.execute(
                f"INSERT INTO mentos.dialog (dt_dialog, u_message, ai_message) VALUES ({u_message}, {ai_message}, NOW();)"
            )
            return True
        except:
            print(traceback.format_exc())
            return False
        finally:
            # self.db.commit()
            self.cursor.close()
            self.db.close()

    def update_dialog_emotion(
        self, kcelectra_data
    ):  # dialog_table UPDATE dialog_emotion (감정분석 후 감정분석 데이터 update)
        try:
            for dialog_id, model_data in enumerate(kcelectra_data, start=1):
                self.cursor.execure(
                    f"UPDATE dialog SET dialog_emotion = {model_data} WHERE dialog_id = {dialog_id}"
                )
            self.db.commit()
            return True
        except:
            print(traceback.format_exc())
            return False
        finally:
            self.cursor.close()
            self.db.close()

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
        finally:
            # self.db.commit()
            self.cursor.close()
            self.db.close()

    def select_dialog_log(self):  # dialog Table u_message 조회
        try:
            self.cursor.execute("SELECT u_message FROM dialog;")
            result = self.cursor.fetchall()
            return result

        except:
            print(traceback.extract_exc())
            return False
        finally:
            # self.db.commit()
            self.cursor.close()
            self.db.close()


if __name__ == "__main__":
    from kcelectra_model import Kcelectra

    db_handler = DBhandler()
    kcelectra = Kcelectra()

    dialog_log = db_handler.select_dialog_log()
    label = kcelectra.analyze_sentiment(pd.DataFrame(dialog_log))
    db_handler.update_dialog_emotion(label)

    if db_handler.select_dialog_log():
        print("인풋 성공함!")
    else:
        print("인풋 실패!")
