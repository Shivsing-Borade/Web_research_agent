from typing import TypedDict


class TopicState(TypedDict):
    google_trends: list
    reddit_topics: list
    youtube_topics: list
    news_topics: list
    x_topics: list
    all_topics: list
    common_topics: list