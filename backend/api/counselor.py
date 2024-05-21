from fastapi import APIRouter
from schemas.request import Text
# from schemas.db_handler import DBhandler
from transformers import TextStreamer
from models.mentos import (tokenizer,
                           model,
                           retriever_memory,
                           buffer_memory,
                           )
from models.mentos_dpo import model_dpo
from models.kcelectra_model import sentiment_analyzer
from models.bart_speech_style_converter import speech_style_converter

router = APIRouter()
# db_handler = DBhandler()


def speech_style_convert(input, style):
    text = f"{style} 형식으로 변환:{input}"
    out = speech_style_converter(text, max_length=250)[0]['generated_text']    
    return out


def predict(message, tone):  # message: 사용자 입력, tone: 말투
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    buffer_history = buffer_memory.load_memory_variables({})["history"]

    previous_conversation =''  # 직전 1개의 대화
    similar_conversation=''  # 직전 1개의 대화를 제외한, 사용자 입력과 유사한 2개의 과거 대화
    converted_response = ''  # 말투가 변경된 멘토스 답변
    
    cnt = 0
    if buffer_history:
      for buffer in buffer_history.split('\n'):
        if cnt:
          previous_conversation += buffer[4:] + '\n'
          ans = buffer[4:]

        else:
          previous_conversation += buffer[7:] + '\n'
          q = buffer[7:]

        cnt += 1

      similar_history = retriever_memory.load_memory_variables({"query": message})["history"].split('\n')
      similar_history =  similar_history[2:] + similar_history[:2]

      for text in similar_history:
        similar_conversation += text[4:] +'\n'

      retriever_memory.save_context(
            {"질문": q},
            {"답변": ans},
        )
      
      context = similar_conversation + previous_conversation + message

    else:
      context = message

    conversation = [{'role': 'user', 'content': context}]
    inputs = tokenizer.apply_chat_template(
        conversation,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors='pt').to("cuda")
    
    if tone == "전문적인 상담사":
       model_dpo.eval()

       _ = model_dpo.generate(inputs,
                      streamer=streamer,
                      max_new_tokens=512,
                      use_cache=True,
                      repetition_penalty=1.2)
       response = tokenizer.decode(_[0][len(inputs[0]):], skip_special_tokens=True)  # 멘토스_dpo 답변

    else: 
      model.eval()
      
      _ = model.generate(inputs,
                        streamer=streamer,
                        max_new_tokens=512,
                        use_cache=True,
                        repetition_penalty=1.2)
      response = tokenizer.decode(_[0][len(inputs[0]):], skip_special_tokens=True)  # 멘토스 답변

    message_sentiment = sentiment_analyzer(message)[0]['label']  # 사용자 입력 감성
     
    buffer_memory.save_context(
            {"질문": message.strip('\n')},
            {"답변": response.strip('\n')},
        )

    print("과거 대화:", similar_conversation + previous_conversation, '\n')
    print("사용자 입력:", message, '\n')
    print("사용자 입력 감성 분석:", message_sentiment, '\n')
    print("멘토스 답변:", response, '\n')

    if tone != ("멘토스" or "전문적인 상담사"):
      converted_response = speech_style_convert(response, tone)
      print("말투가 변경된 멘토스 답변:", converted_response, '\n')
    
    # 사용자 입력(u_message), 멘토스 답변(ai_message), 사용자 입력 감성(dialog_emotion), 과거 대화(past_dialog), 사용자가 선택한 말투로 변환된 답변(change_dialog) data INSERT
    # db_handler.create_dialog_message(u_message=message,
    #                                  ai_message=response,
    #                                  dialog_emotion=message_sentiment,
    #                                  past_dialog=similar_conversation + previous_conversation,
    #                                  change_dialog=converted_response,
    #                                  )    
    
    # 사용자가 선택한 말투로 변환된 답변
    if converted_response:
       response = converted_response

    answer = response + '\n* 당신은 현재 ' + message_sentiment + ' 감정을 느끼고 있어요'
    return answer


@router.post("/counselor")
def eeve(request: Text):
    message = request.msg
    tone = request.tone
    result = predict(message.strip(), tone) 
    return {"result": result}
