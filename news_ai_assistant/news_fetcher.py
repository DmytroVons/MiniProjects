import time
from datetime import datetime, date
from os import getenv
from typing import List

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

NEWS_API_KEY = getenv("NEWS_API_KEY")


def get_news_articles(category="world", language="en", country="us", sort="top", page=1, limit=20) -> List:
    """Gets news articles from the NewsAPI.
    Args:
        category (str, optional): The category of news articles to retrieve. Defaults to "world".
        language (str, optional): The language of the news articles to retrieve. Defaults to "en".
        country (str, optional): The country of the news articles to retrieve. Defaults to "us".
        sort (str, optional): The sort order of the news articles. Defaults to "top".
        page (int, optional): The page number of the results. Defaults to 1.
        limit (int, optional): The number of results per page. Defaults to 20.
    Returns:
        list: A list of news articles.
    """
    url = "https://newsi-api.p.rapidapi.com/api/category"

    headers = {
        "X-RapidAPI-Key": NEWS_API_KEY,
        "X-RapidAPI-Host": "newsi-api.p.rapidapi.com"
    }

    querystring = {
        "category": category,
        "language": language,
        "country": country,
        "sort": sort,
        "page": f"{page}",
        "limit": f"{limit}"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        articles = response.json()
        return articles


def form_news_articles() -> str:
    """Forms the news articles
    Returns:
        str: A string of news articles.
    """
    articles_list = []
    pages = 1
    for page in range(pages):
        articles = get_news_articles(page=page)

        for article in articles:
            published_timestamp = datetime.utcfromtimestamp(article.get("publishedTimestamp"))
            if published_timestamp.date() == date.today() and article.get('body'):
                articles_list.append(article.get('body'))
        time.sleep(1)

    return ''.join(articles_list)
