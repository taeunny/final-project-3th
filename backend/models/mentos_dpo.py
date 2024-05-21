import torch
from peft import AutoPeftModelForCausalLM
from transformers import BitsAndBytesConfig

compute_dtype = getattr(torch, 'float16')

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)

MODEL_DIR = "hskhyl/05-13_1-dpo"
model_dpo = AutoPeftModelForCausalLM.from_pretrained(MODEL_DIR,
                                                      quantization_config=quant_config,
                                                      device_map="auto")
