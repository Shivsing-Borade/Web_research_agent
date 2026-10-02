from langgraph.graph import StateGraph, START, END

from state import TopicState
from tools import *

from models import model


# --------------------------------------------------
# SOURCE NODES
# --------------------------------------------------

def google_trends_node(state: TopicState):

    topics = get_google_trends()

    return {
        "google_trends": topics
    }


def youtube_node(state: TopicState):

    topics = get_youtube_topics()

    return {
        "youtube_topics": topics
    }


def news_node(state: TopicState):

    topics = get_news_topics()

    return {
        "news_topics": topics
    }


# --------------------------------------------------
# COMBINE ALL SOURCES
# --------------------------------------------------

def combine_topics_node(state: TopicState):

    google_trends = state.get("google_trends", [])
    youtube_topics = state.get("youtube_topics", [])
    news_topics = state.get("news_topics", [])

    all_topics = (
            google_trends[:20]
            + youtube_topics[:100]
            + news_topics[:100]
    )

    return {
        "all_topics": all_topics
    }


# --------------------------------------------------
# EXTRACT / NORMALIZE TOPICS
# --------------------------------------------------

def extract_topics_node(state: TopicState):

    raw_topics = state["all_topics"]

    text = "\n".join(
        f"- {item['topic']}"
        for item in raw_topics
    )

    prompt = f"""
You are a topic extraction system.

Below are current search queries, news headlines,
and YouTube video titles collected from different sources.

Your task is to identify the major real-world topics
being discussed.

Rules:
- Combine items referring to the same topic.
- Do not return individual headlines.
- Return short, clear topic names.
- Remove duplicate topics.
- Focus on actual subjects, events, people, products,
  technologies, sports, entertainment, etc.
- Return up to 30 topics.
- Return ONLY a numbered list.

Data:

{text}
"""
    print(prompt)
    print('sending to LLM')
    response = model.invoke(prompt)
    print('response recieved ')
    extracted_topics = response.content

    return {
        "common_topics": extracted_topics
    }


# --------------------------------------------------
# GRAPH
# --------------------------------------------------

graph = StateGraph(TopicState)


# Source nodes
graph.add_node("google_trends", google_trends_node)
graph.add_node("youtube", youtube_node)
graph.add_node("news", news_node)

# Processing nodes
graph.add_node("combine_topics", combine_topics_node)
graph.add_node("extract_topics", extract_topics_node)


# --------------------------------------------------
# PARALLEL SOURCE COLLECTION
# --------------------------------------------------

graph.add_edge(START, "google_trends")
graph.add_edge(START, "youtube")
graph.add_edge(START, "news")


# All three must finish before combining
graph.add_edge("google_trends", "combine_topics")
graph.add_edge("youtube", "combine_topics")
graph.add_edge("news", "combine_topics")


# Extract topics after combining
graph.add_edge("combine_topics", "extract_topics")


# Finish
graph.add_edge("extract_topics", END)


topic_graph = graph.compile()

if __name__ == "__main__":

    result = topic_graph.invoke({
        "google_trends": [],
        "reddit_topics": [],
        "youtube_topics": [],
        "news_topics": [],
        "x_topics": [],
        "all_topics": [],
        "common_topics": []
    })

    print("\n===== EXTRACTED TOPICS =====\n")
    print(result["common_topics"])