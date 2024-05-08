"""
MySql DB 연결 및 쿼리 실행 모듈
"""

import pymysql
from datetime import datetime
from pytz import timezone
import traceback
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")

    
db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, charset='utf8')
cursor = db.cursor()

cursor.execute('USE mentos;') # mentos 스키마 접근


class DBhandler :
    def __init__(self):
        self.cursor = db.cursor()
        
    def create_user(self, user_cookie): # user Table
        try:
            cursor.execute("INSERT INTO mentos.user (user_id) VALUES (%s)",
                           ({user_cookie}))
            db.commit()
            db.close()
            return True
        except:
            print(traceback.format_exc())
            return False
        
    def create_dialog_log(self, u_message, ai_message): # dialog Table
        try:
            time = datetime.now(timezone('Asia/Seoul'))
            cursor.execute(f"INSERT INTO mentos.dialog (dt_dialog, u_message, ai_message) VALUES (%s, %s, %s)",
                           ({time}, {u_message}, {ai_message}))
            db.commit()
            db.close()
            return True
        except:
            print(traceback.format_exc())
            return False
        
    def create_emotion_log(self, input_message): # emotion_log Table
        try:
            time = datetime.now(timezone('Asia/Seoul'))
            cursor.execute(f"INSERT INTO mentos.emotion_log (counsel_emotion, dt_emotion_log) VALUES (%s, %s)", 
                           ({input_message}, {time}))
            db.commit()
            db.close()
            return True
        except:
            print(traceback.format_exc())
            return False
        
        
        



if __name__ == '__main__':
    db_handler = DBhandler()
    
    if db_handler.create_emotion_log("temp_message"):
        print("인풋 성공함!")
    else:
        print("인풋 실패!")
        