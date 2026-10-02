from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Flash-0731",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.2
)

validation_model = ChatHuggingFace(llm=llm)

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.2
)

model = ChatHuggingFace(llm=llm)