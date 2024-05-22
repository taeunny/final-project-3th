import torch
from peft import AutoPeftModelForCausalLM
from transformers import (
    AutoTokenizer,
    BitsAndBytesConfig,
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

MODEL_DIR = "hskhyl/EEVE-finetuned-05-13_1"
model = AutoPeftModelForCausalLM.from_pretrained(MODEL_DIR,
                                                      quantization_config=quant_config,
                                                      device_map="auto")

tokenizer = AutoTokenizer.from_pretrained("hskhyl/EEVE-finetuned-05-13_1")

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
retriever_memory = VectorStoreRetrieverMemory(retriever=retriever, return_docs=False)
buffer_memory = ConversationBufferWindowMemory(k=1, return_messages=False)
