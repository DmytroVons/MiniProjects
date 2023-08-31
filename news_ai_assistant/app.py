import streamlit as st
from dotenv import load_dotenv

from news_ai_assistant import NewsAIAssistant
from news_fetcher import NewsFetcher

# Load environment variables from .env file
load_dotenv()


def main():
    ai_response_result = ""
    news_fetcher = NewsFetcher()
    articles = news_fetcher.form_articles()
    st.header("News AI Assistant")
    news_ai_assistant = NewsAIAssistant()
    for news in articles:
        ai_response = news_ai_assistant.run(news)
        ai_response_result += f"{ai_response}\n\n"
    st.write(ai_response_result)


if __name__ == '__main__':
    main()
