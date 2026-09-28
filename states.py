from typing import TypedDict
from pydantic import BaseModel, Field
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class ResearchState(TypedDict):
    question: str
    search_results: list
    scraped_content: list
    extracted_information: str
    is_valid: bool
    validation_feedback: str
    attempts: int

class ValidationResult(BaseModel):

    is_valid: bool = Field(
        description="Whether the extracted information adequately answers the question"
    )

    feedback: str = Field(
        description="Explain why the information is valid or what is missing"
    )


