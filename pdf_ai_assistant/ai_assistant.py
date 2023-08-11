import os
import pickle
from typing import List

from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

DEFAULT_PDF_FILE_PATH = 'files/my_file.pdf'

# Load environment variables from .env file
load_dotenv()


class NiftyBridgeAIAssistant:
    """
    An LLM-powered chatbot using FastAPI, LangChain, and Streamlit.
    """

    def __init__(self):
        self.vector_store = None

    def _load_or_create_embeddings(self, chunks: List[str], store_file_path: str) -> None:
        """
        Load embeddings from disk or create new embeddings and save to disk.

        Args:
            chunks (List[str]): List of text chunks.
            store_file_path (str): The store file path.
        """
        if os.path.exists(store_file_path):
            with open(store_file_path, "rb") as file:
                self.vector_store = pickle.load(file)
        else:
            embeddings = OpenAIEmbeddings()
            self.vector_store = FAISS.from_texts(chunks, embedding=embeddings)
            with open(store_file_path, "wb") as file:
                pickle.dump(self.vector_store, file)

    @staticmethod
    def _validate_query(input_text: str) -> bool:
        """
        Validate the input text length to ensure it doesn't exceed the maximum token limit.

        Args:
            input_text (str): The user input text.

        Returns:
            bool: True if the query is valid, False otherwise.
        """
        max_tokens = 4096
        return len(input_text.split()) <= max_tokens

    @staticmethod
    def _process_pdf(pdf_path: str) -> List[str]:
        """
        Process a PDF file to extract text and split it into chunks.

        Args:
            pdf_path (bytes): The PDF file path.

        Returns:
            List[str]: List of text chunks.
        """
        pdf_path = DEFAULT_PDF_FILE_PATH if not pdf_path else pdf_path
        pdf_reader = PdfReader(pdf_path)
        text = ''.join([page.extract_text() for page in pdf_reader.pages])

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        return text_splitter.split_text(text=text)

    def run(self, query: str, pdf_path: str = None) -> str:
        """
        Run the NiftyBridge AI assistant.

        Args:
            query (str): The user's query.
            pdf_path (str): The PDF file path.
        Returns:
            str: The response from the AI assistant.
        """
        chunks = self._process_pdf(pdf_path)
        store_file_path = os.path.join("files", "temp.pkl")
        self._load_or_create_embeddings(chunks, store_file_path)

        if self._validate_query(query):
            docs = self.vector_store.similarity_search(query=query, k=3)
            turbo_llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
            prompt = f"User: {query}\nNiftyBridge AI assistant:"
            chain = load_qa_chain(llm=turbo_llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=prompt)
            if "I don't" in response:
                response = "I don't know, please contact support by email support@nifty-bridge.com"
            return response
