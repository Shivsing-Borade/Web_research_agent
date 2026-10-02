import requests
import xml.etree.ElementTree as ET
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_google_trends():

    url = "https://trends.google.com/trending/rss?geo=IN"

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    topics = []

    for item in root.findall(".//item"):
        title = item.find("title")

        if title is not None and title.text:
            topics.append({
                "topic": title.text.strip(),
                "source": "google_trends"
            })

    return topics


def get_reddit_topics():

    url = "https://www.reddit.com/r/popular/hot.json"

    params = {
        "limit": 100
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
        headers={
            "User-Agent": "TopicDiscoveryAgent/1.0"
        }
    )

    response.raise_for_status()

    data = response.json()

    topics = []

    for post in data["data"]["children"]:
        post_data = post["data"]

        title = post_data.get("title")

        if title:
            topics.append(title)

    return topics



def get_youtube_topics():

    api_key = os.getenv("YOUTUBE_API_KEY")

    url = "https://www.googleapis.com/youtube/v3/search"

    queries = [
        "trending news India",
        "latest technology",
        "latest AI",
        "latest science",
        "latest business",
        "trending India",
        "latest world news",
    ]

    topics = []

    for query in queries:

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "regionCode": "IN",
            "maxResults": 50,
            "order": "relevance",
            "key": api_key
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        for video in data.get("items", []):

            title = video["snippet"].get("title")

            if title:
                topics.append({
                    "topic": title,
                    "source": "youtube"
                })

    return topics

def get_news_topics():

    queries = [
        "latest news India",
        "latest technology news",
        "latest AI news",
        "latest science news",
        "latest business news",
        "latest world news",
        "trending news",
    ]

    topics = []

    for query in queries:

        try:

            url = "https://news.google.com/rss/search"

            params = {
                "q": query,
                "hl": "en-IN",
                "gl": "IN",
                "ceid": "IN:en"
            }

            response = requests.get(
                url,
                params=params,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            response.raise_for_status()

            root = ET.fromstring(response.content)

            for item in root.findall(".//item"):

                title = item.find("title")

                if title is not None and title.text:
                    topics.append({
                        "topic": title.text.strip(),
                        "source": "google_news"
                    })

        except requests.exceptions.RequestException as e:

            print(f"News request failed for '{query}': {e}")
            continue

    return topics

