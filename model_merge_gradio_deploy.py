# -*- coding: utf-8 -*-
"""model_merge_gradio_deploy(발표).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n1dHQXNBcglgakXhbHCLY87cT6knw76O
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install -q accelerate==0.26.1 peft==0.8.2 bitsandbytes==0.42.0 transformers==4.37.2 gradio==3.45.0 --use-deprecated=legacy-resolver typing_extensions --upgrade

import torch
import time
import gradio as gr
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TextStreamer
    )

base_model = "nlpai-lab/KULLM3"

compute_dtype = getattr(torch, 'float16')

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=quant_config,
    device_map={"": 0}
)
model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 어댑터 추가
model_to_merge = PeftModel.from_pretrained(model, "/content/drive/MyDrive/Colab Notebooks/model/finetuned_model")

streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

def res(message: str, history: list) -> str:

    SYSTEM_PROMPT = """
    <s>[INST] <<SYS>>You are a counselor like friend who empathizes, encourages, and helps person who is anxious or depressed. You must complete your answer in three sentences. Be sure not to repeat the same answer.<</SYS>>
    """

    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    conversation = [{'role': 'user', 'content': SYSTEM_PROMPT + f"{message} [/INST]"}]
    inputs = tokenizer.apply_chat_template(
    conversation,
    tokenize=True,
    add_generation_prompt=False,
    return_tensors='pt'
    ).to("cuda")
    _ = model_to_merge.generate(inputs, streamer=streamer, max_new_tokens=300, repetition_penalty=1.2)
    response = tokenizer.decode(_[0][len(inputs[0]):])

    print("사용자 입력:", message)
    print("멘토스 답변:", response)

    for i in range(len(response)):
        time.sleep(0.03)
        yield response[:i+1]

gr.ChatInterface(
        fn=res,
        textbox=gr.Textbox(placeholder="고민을 얘기해주세요🙌", container=False, scale=1),
        title="멘토스(Mental Mate Talk on Support)",
        description="멘토스는 당신의 고민을 들어주며 격려해주는 상담친구에요😊",
        theme="soft",
        examples=[["나 우울해"], ["너무 짜증나"], ["사는게 쉽지않아"]],
        retry_btn="다시보내기 ↩",
        undo_btn="이전챗 삭제 ❌",
        clear_btn="전챗 삭제 💫"
).queue().launch(debug=True, share=True)

