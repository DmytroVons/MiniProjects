from os import path
from typing import List

from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()

DEFAULT_PDF_FILE_PATH = path.join('files', 'news.pdf')


class NewsAIAssistant:

    def _create_embeddings(self, chunks: List[str]) -> None:
        """Creates new embeddings.

        Args:
            chunks (List[str]): List of text chunks.
        """
        embeddings = OpenAIEmbeddings()
        self.vector_store = FAISS.from_texts(chunks, embedding=embeddings)

    @staticmethod
    def _process_pdf() -> List[str]:
        """
        Process a PDF file to extract text and split it into chunks.
        Returns:
            List[str]: List of text chunks.
        """
        pdf_reader = PdfReader(DEFAULT_PDF_FILE_PATH)
        text = ''.join([page.extract_text() for page in pdf_reader.pages])

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=400,
            length_function=len
        )
        return text_splitter.split_text(text=text)

    def run(self) -> str:
        """Runs the News AI assistant.

        Returns:
            str: The response from the AI assistant.
        """
        chunks = self._process_pdf()
        self._create_embeddings(chunks)
        docs = self.vector_store.similarity_search(query="Please summarize these news articles")
        turbo_llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
        prompt = (f"User: Please summarize these news articles\n"
                  f"News AI assistant:")
        chain = load_qa_chain(llm=turbo_llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=prompt)
        return response

    def customer_questions(self, query: str) -> str:
        docs = self.vector_store.similarity_search(query=query)
        turbo_llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
        prompt = f"User: {query}\nNews AI assistant:"
        chain = load_qa_chain(llm=turbo_llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=prompt)
        return response
