from models import client
from pydantic import BaseModel


class ValidationResult(BaseModel):
    is_valid: bool
    feedback: str


response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "ValidationResult",
        "schema": ValidationResult.model_json_schema(),
        "strict": True,
    },
}


response = client.chat.completions.create(
    model="Qwen/Qwen3-32B",
    messages=[
        {
            "role": "system",
            "content": "Determine whether the provided information answers the question."
        },
        {
            "role": "user",
            "content": """
Question:
What is LangGraph?

Information:
LangGraph is a framework for building stateful,
multi-step applications with language models.
"""
        }
    ],
    response_format=response_format,
)

print(response.choices[0].message.content)