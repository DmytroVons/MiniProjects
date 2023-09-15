import streamlit as st
from dotenv import load_dotenv

from news_ai_assistant import NewsAIAssistant
from news_fetcher import NewsFetcher

# Load environment variables from .env file
load_dotenv()


def main():
    news_fetcher = NewsFetcher()
    news_fetcher.form_articles()
    st.header("News AI Assistant")
    news_ai_assistant = NewsAIAssistant()
    ai_response = news_ai_assistant.run()
    st.write(ai_response)

    query = st.text_input("Please ask question about the recent news described above:")

    if query:
        question_response = news_ai_assistant.customer_questions(query)
        st.write(question_response)


if __name__ == '__main__':
    main()
