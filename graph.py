from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from states import ResearchState,ValidationResult
from tools import web_search, scrape_page
from models import model,validation_model

def search_node(state: ResearchState):

    attempts = state.get("attempts", 0) + 1

    results = web_search(state["question"])

    return {
        "search_results": results,
        "attempts": attempts
    }

def scrape_node(state: ResearchState):
    results = state["search_results"]

    scraped_content = []

    for result in results:
        url = result["link"]

        try:
            content = scrape_page(url)

            scraped_content.append({
                "url": url,
                "content": content
            })

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    return {
        "scraped_content": scraped_content
    }


def extract_node(state: ResearchState):

    question = state["question"]
    pages = state["scraped_content"]

    context = ""

    for page in pages:
        context += f"""
SOURCE: {page['url']}

CONTENT:
{page['content']}

--------------------------------
"""

    prompt = f"""
You are a web research assistant.

User's question:
{question}

Below is information collected from webpages:

{context}

Extract only the information that is relevant to the user's question.

Give a clear and concise answer based only on the provided sources.
"""

    response = model.invoke(prompt)

    return {
        "extracted_information": response.content
    }



def validate_node(state: ResearchState):
    parser = PydanticOutputParser(
        pydantic_object=ValidationResult
    )
    template = PromptTemplate(
        template="""
You are validating a web research result.

Question:
{question}

Extracted information:
{information}

Determine whether the extracted information adequately
answers the user's question.

{format_instructions}
""",
        input_variables=["question", "information"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    chain = template | model | parser

    result = chain.invoke({
        "question": state["question"],
        "information": state["extracted_information"]
    })

    return {
        "is_valid": result.is_valid,
        "validation_feedback": result.feedback
    }


def validation_router(state: ResearchState):

    if state["is_valid"]:
        return "report"

    if state["attempts"] >= 3:
        return "report"

    return "search"

def report_node(state: ResearchState):

    question = state["question"]
    information = state["extracted_information"]

    prompt = f"""
You are a research report writer.

User's question:
{question}

Validated research information:
{information}

Create a clear and concise final research report.

Requirements:
- Directly answer the user's question
- Organize the information logically
- Do not add information that is not present in the research
- Keep the answer easy to understand
"""

    response = model.invoke(prompt)

    return {
        "extracted_information": response.content
    }


graph = StateGraph(ResearchState)

graph.add_node("search", search_node)
graph.add_node("scrape", scrape_node)
graph.add_node("extract", extract_node)
graph.add_node("validate", validate_node)
graph.add_node("report", report_node)

graph.add_edge(START, "search")
graph.add_edge("search", "scrape")
graph.add_edge("scrape", "extract")
graph.add_edge("extract", "validate")

graph.add_conditional_edges(
    "validate",
    validation_router,
    {
        "search": "search",
        "report": "report"
    }
)

graph.add_edge("report", END)

research_graph = graph.compile()