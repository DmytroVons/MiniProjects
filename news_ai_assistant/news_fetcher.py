import json
from datetime import datetime, date
from os import getenv, path
from re import search
from typing import List, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

EXCLUDE_WORDS_PATTERN = r"\b(cookies|javascript|ad blocker)\b"


class NewsAPI:
    """Interacts with the NewsAPI to fetch news articles."""

    def __init__(self):
        self.url = "https://newsi-api.p.rapidapi.com/api/category"
        self.headers = {
            "X-RapidAPI-Key": getenv("NEWS_API_KEY"),
            "X-RapidAPI-Host": "newsi-api.p.rapidapi.com"
        }

    def get_articles(self,
                     config={},
                     category="world",
                     language="en",
                     country="us",
                     sort="top",
                     page=1,
                     limit=10
                     ) -> List[Dict]:
        """Fetches news articles from the NewsAPI.

        Args:
            config (dict, optional): Configurations. Defaults to an empty dictionary.
            category (str, optional): The category of news articles to retrieve. Defaults to "world".
            language (str, optional): The language of the news articles to retrieve. Defaults to "en".
            country (str, optional): The country of the news articles to retrieve. Defaults to "us".
            sort (str, optional): The sort order of the news articles. Defaults to "top".
            page (int, optional): The page number of the results. Defaults to 1.
            limit (int, optional): The number of results per page. Defaults to 20.

        Returns:
            List[Dict]: A list of news articles.
        """
        query_params = {
            "category": config.get("category", category),
            "language": config.get("language", language),
            "country": config.get("country", country),
            "sort": config.get("sort", sort),
            "page": config.get("page", page),
            "limit": config.get("limit", limit)
        }
        response = requests.get(self.url, headers=self.headers, params=query_params)
        if response.status_code == 200:
            articles = response.json()
            return articles


class NewsFetcher:
    """Fetches and processes news articles."""

    def __init__(self):
        self.news_api = NewsAPI()

    def form_articles(self) -> List[str]:
        """Forms a list of news articles.

        Returns:
            List[str]: List of formatted news articles.
        """
        articles_list = []
        config = self.read_config_file()
        articles = self.news_api.get_articles(config=config)
        if articles:
            for article in articles:
                published_timestamp = datetime.utcfromtimestamp(article.get("publishedTimestamp"))
                if published_timestamp.date() == date.today():
                    if not article.get('hasBody') or search(EXCLUDE_WORDS_PATTERN, article.get('body').lower()):
                        articles_list.append(article.get('title').replace('\n', ''))
                    else:
                        articles_list.append(article.get('body').replace('\n', ''))
        return articles_list

    @staticmethod
    def read_config_file(filename: str = "config.json", filepath: str = ".") -> Dict:
        """Reads the configuration file.

        Args:
            filename (str, optional): Name of the config file. Defaults to "config.json".
            filepath (str, optional): Path to the config file. Defaults to ".".

        Returns:
            Dict: Configuration settings as a dictionary.
        """
        with open(path.join(filepath, filename)) as file:
            return json.load(file)
