from fastapi import APIRouter
from schemas.request import text
from schemas.db_handler import DBhandler
from transformers import TextStreamer
from models.mentos import (tokenizer,
                           model,
                           retriever_memory,
                           buffer_memory,
                           )
from models.kcelectra_model import sentiment_analyzer

router = APIRouter()
db_handler = DBhandler()


def predict(message):  # message > 사용자 입력
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    buffer_history = buffer_memory.load_memory_variables({})["history"]

    previous_conversation =''  # 직전 1개의 대화
    similar_conversation=''  # 직전 1개의 대화를 제외한, 사용자 입력과 유사한 2개의 과거 대화
    
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

      similar_history = retriever_memory.load_memory_variables({"query": message})["history"]

      for texts in similar_history.split('\n'):
        similar_conversation += texts[4:] +'\n'

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
    
    model.eval()
    
    _ = model.generate(inputs,
                      streamer=streamer,
                      max_new_tokens=1024,
                      use_cache=True,
                      repetition_penalty=1.2)
    response = tokenizer.decode(_[0][len(inputs[0]):], skip_special_tokens=True)  # 멘토스 답변

    message_sentiment = sentiment_analyzer(message)[0]['label']  # 사용자 입력 감성

    buffer_memory.save_context(
            {"질문": message.strip('\n')},
            {"답변": response.strip('\n')},
        )

    print("과거 대화:", similar_conversation+previous_conversation, '\n')
    print("사용자 입력:", message, '\n')
    print("사용자 입력 감성 분석:", message_sentiment, '\n')
    print("멘토스 답변:", response, '\n')
    
    # 사용자 입력(u_message), 멘토스 답변(ai_message), 사용자 입력 감성(dialog_emotion) data INSERT
    db_handler.create_dialog_message(u_message=message,
                                     ai_message=response,
                                     dialog_emotion=message_sentiment)

    answer = response + '\n* 당신은 현재 ' + message_sentiment + ' 감정을 느끼고 있어요'
    return answer


@router.post("/counselor")
def eeve(request: text):
    message = request.msg
    result = predict(message.strip())
    return {"result": result}
