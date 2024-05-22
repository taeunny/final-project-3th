"""
MySql DB 연결 및 쿼리 실행 모듈
"""

# import pymysql
# import traceback


# class DBhandler:
#     def __init__(self):
#         self.connection = pymysql.connect(
#             host='', 
#             user='', 
#             password='', 
#             charset=""
#         )
#         self.cursor = self.connection.cursor()
#         self.cursor.execute("USE mentos;")  # mentos 스키마 접근

#     def create_dialog_message(
#         self, u_message, ai_message, dialog_emotion, past_dialog, change_dialog
#     ):  # dialog Table INSERT DATA(user_message(인풋), ai_message(아웃풋), dialog_emotion(인풋 감성 분석), 과거 대화(past_dialog), 사용자가 선택한 말투로 변환된 답변(change_dialog))
#         try:
#             self.cursor.execute(
#                 "INSERT INTO mentos.dialog (dt_dialog,u_message, ai_message, dialog_emotion, past_dialog, change_dialog) VALUES (NOW(), %s, %s, %s, %s, %s);", (u_message, ai_message, dialog_emotion, past_dialog, change_dialog)
#             )
#             self.connection.commit()
 
#             return True
#         except:
#             print(traceback.format_exc())
#             return False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
