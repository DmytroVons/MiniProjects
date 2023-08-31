from typing import List

from dotenv import load_dotenv
from langchain import FAISS
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()


class NewsAIAssistant:

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
            chunk_size=10000,
            chunk_overlap=500,
            length_function=len
        )
        return text_splitter.split_text(text=text)

    def run(self, news_text: str) -> str:
        """Runs the News AI assistant.

        Returns:
            str: The response from the AI assistant.
        """
        chunks = self._process_text(news_text)
        self._create_embeddings(chunks)
        docs = self.vector_store.similarity_search(
            query="Please summarize these news articles")
        turbo_llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        prompt = (f"User: Please summarize these news\n"
                  f"News AI assistant:")
        chain = load_summarize_chain(llm=turbo_llm, chain_type="map_reduce")
        response = chain.run(input_documents=docs, question=prompt)
        return response
