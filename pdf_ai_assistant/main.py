import os
from pickle import dump, load
from typing import List

import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_extras.add_vertical_space import add_vertical_space


class NiftyBridgeAIAssistant:
    """
    An LLM-powered chatbot using Streamlit and LangChain.
    """

    def __init__(self):
        load_dotenv()
        self.vector_store = None

    def _load_or_create_embeddings(self, chunks: List[str], store_name: str) -> None:
        """
        Load embeddings from disk or create new embeddings and save to disk.

        Args:
            chunks (List[str]): List of text chunks.
            store_name (str): Name of the pickle file for storing embeddings.
        """
        if os.path.exists(store_name):
            with open(store_name, "rb") as file:
                self.vector_store = load(file)
            st.write("Embeddings Loaded from the Disk")
        else:
            embeddings = OpenAIEmbeddings()
            self.vector_store = FAISS.from_texts(chunks, embedding=embeddings)
            with open(store_name, "wb") as file:
                dump(self.vector_store, file)

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
        if len(input_text.split()) > max_tokens:
            st.write("Response is too long. Please contact support by email support@nifty-bridge.com")
            return False
        return True

    @staticmethod
    def _process_pdf(pdf: UploadedFile) -> List[str]:
        """
        Process a PDF file to extract text and split it into chunks.

        Args:
            pdf (bytes): The PDF file content.

        Returns:
            List[str]: List of text chunks.
        """
        pdf_reader = PdfReader(pdf)
        text = ''.join([page.extract_text() for page in pdf_reader.pages])

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        return text_splitter.split_text(text=text)

    @staticmethod
    def _display_sidebar():
        """
        Display the sidebar content with app information and PDF upload.
        """
        with st.sidebar:
            st.title("NiftyBridge AI assistant")
            st.markdown("""
            ## About
            This app is an LLM-powered chatbot built using:
            - [Streamlit](http://streamlit.io/)
            - [LangChain](http://python.langchain.com/)
            - [OpenAI](http://platform.openai.com/docs/models) LLM model

            """)
            add_vertical_space(5)
            st.write("Made with love by Dmytro Vons")

        st.header("Chat with PDF")
        pdf = st.file_uploader("Upload your PDF", type="pdf")
        print(pdf)
        return pdf

    def run(self) -> None:
        """
        Run the NiftyBridge AI assistant.
        """
        pdf = self._display_sidebar()

        if pdf:
            chunks = self._process_pdf(pdf)
            store_name = f"{pdf.name.replace('.pdf', '')}.pkl"
            self._load_or_create_embeddings(chunks, store_name)

            query = st.text_input("Ask questions about your PDF file:")
            if self._validate_query(query):
                docs = self.vector_store.similarity_search(query=query, k=3)
                turbo_llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
                prompt = f"User: {query}\nNiftyBridge AI assistant:"
                chain = load_qa_chain(llm=turbo_llm, chain_type="stuff")
                response = chain.run(input_documents=docs, question=prompt)
                if "I don't" in response:
                    response = "I don't know, please contact support by email support@nifty-bridge.com"
                st.write(response)


if __name__ == '__main__':
    assistant = NiftyBridgeAIAssistant()
    assistant.run()
