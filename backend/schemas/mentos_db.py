"""
MySql DB 연결 및 쿼리 실행 모듈
"""

import pymysql
from datetime import datetime
import traceback
import time    
db = pymysql.connect(host='database-2.cb020s4qamql.ap-northeast-2.rds.amazonaws.com', user='admin', password='saltlux123!', charset='utf8')
cursor = db.cursor()

cursor.execute('USE mentos;')


class DBhandler :
    def __init__(self):
        self.cursor = db.cursor()
        
    def create_dialog_log(self, u_message, ai_message): #dialog_table INSERT DATA
        try:
            cursor.execute(f"INSERT INTO mentos.dialog (dt_dialog, u_message, ai_message) VALUES (%s, %s, %s)",
                           ({u_message}, {ai_message}, {time.strftime("%Y-%m-%d %H:%M:%S")}))
            db.commit()
            db.close()
            return True
        except:
            print(traceback.format_exc())
            return False
        
    def create_emotion_log(self, input_message):
        try:
            cursor.execute(f"INSERT INTO mentos.emotion_log (counsel_emotion, dt_emotion_log) VALUES (%s, %s)", 
                           ({input_message}, {time.strftime("%Y-%m-%d %H:%M:%S")}))
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
        