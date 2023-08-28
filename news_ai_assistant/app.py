import streamlit as st
from dotenv import load_dotenv

from news_ai_assistant import NewsAIAssistant

# Load environment variables from .env file
load_dotenv()


def main():
    st.header("News AI Assistant")
    news_ai_assistant = NewsAIAssistant()
    news_ai_assistant_response = news_ai_assistant.run()
    st.write(news_ai_assistant_response)


if __name__ == '__main__':
    main()
