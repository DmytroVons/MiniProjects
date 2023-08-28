from typing import List

from dotenv import load_dotenv
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from news_fetcher import form_news_articles

# Load environment variables from .env file
load_dotenv()


class NewsAIAssistant:

    def __init__(self):
        self.news_text = form_news_articles()

    def _create_embeddings(self, chunks: List[str]) -> None:
        """Creates new embeddings.

        Args:
            chunks (List[str]): List of text chunks.
        """
        embeddings = OpenAIEmbeddings()
        self.vector_store = FAISS.from_texts(chunks, embedding=embeddings)

    @staticmethod
    def _process_text(text: str) -> List[str]:
        """Splits text into chunks.
        Args:
            text (str): the input text

        Returns:
            List[str]: List of text chunks.
        """

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        return text_splitter.split_text(text=text)

    def run(self) -> str:
        """Runs the News AI assistant.

        Returns:
            str: The response from the AI assistant.
        """
        chunks = self._process_text(self.news_text)
        self._create_embeddings(chunks)

        docs = self.vector_store.similarity_search(
            query="Please summarize these news articles")
        turbo_llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        prompt = (f"User: Please summarize these news articles\n"
                  f"News AI assistant:")
        chain = load_qa_chain(llm=turbo_llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=prompt)
        return response
