from fastapi import APIRouter
from schemas.request import text
from schemas.mentos_db import DBhandler

router = APIRouter()

import torch
import gradio as gr
from peft import AutoPeftModelForCausalLM
from transformers import (
    AutoTokenizer,
    BitsAndBytesConfig,
    TextStreamer
    )
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS
import faiss


compute_dtype = getattr(torch, 'float16')

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)

MODEL_DIR = "uine/single-practice-fine-tuning-eeve-adapter"
model = AutoPeftModelForCausalLM.from_pretrained(MODEL_DIR,
                                                      quantization_config=quant_config,
                                                      device_map="auto")

tok = AutoTokenizer.from_pretrained("uine/single-practice-fine-tuning-eeve-adapter")

model_name = "jhgan/ko-sbert-nli"
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs
)

embedding_size = 768
index = faiss.IndexFlatL2(embedding_size)
embedding_fn = hf.embed_query
vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})
retriever = vectorstore.as_retriever(search_kwargs=dict(k=2))
memory = VectorStoreRetrieverMemory(retriever=retriever, return_docs=False)


ConversationBufferWindowMemory()
buffer_memory = ConversationBufferWindowMemory(k=1, return_messages=False)
db_handler = DBhandler()

# def res(message: str, history: list) -> str:  # @ message > 사용자 현재 질문
def predict(message):
    streamer = TextStreamer(tok, skip_prompt=True, skip_special_tokens=True)

    buffer_history = buffer_memory.load_memory_variables({})["history"]

    sss =''
    ss=''
    # s = '요가에 대해서도 알려줘'
    cnt = 0
    if buffer_history:
      for buffer in buffer_history.split('\n'):
        if cnt:
          sss += buffer[4:] + '\n'
          ans = buffer[4:]

        else:
          sss += buffer[7:] + '\n'
          q = buffer[7:]

        cnt += 1

      similar_history = memory.load_memory_variables({"query": message})["history"]

      for texts in similar_history.split('\n'):
        ss += texts[4:] +'\n'

      memory.save_context(
            {"질문": q},
            {"답변": ans},
        )

      context = ss + sss + message  # @ ss + sss > 과거 대화들(현재 질문과 유사한 과거 대화 2개랑(ss), 직전 대화 1개(sss))

    else:
      context = message

    conversation = [{'role': 'user', 'content': context}]
    inputs = tok.apply_chat_template(
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
    response = tok.decode(_[0][len(inputs[0]):], skip_special_tokens=True)  # @ response > 답변

    buffer_memory.save_context(
            {"질문": message.strip('\n')},
            {"답변": response.strip('\n')},
        )

    print("과거 대화:", ss+sss, '\n')
    print("사용자 입력:", message, '\n')
    print("멘토스 답변:", response, '\n')
    
    db_handler.create_dialog_log(u_message=message, ai_message=response) # u_message와 ai_message data INSERT

    return response

@router.post("/counselor")
def eeve(request: text):
    message = request.msg
    result = predict(message.strip())
    return {"result": result}
