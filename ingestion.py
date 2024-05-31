from dotenv import load_dotenv
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from pinecone import Pinecone
from consts import INDEX_NAME
load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def ingest_pdf() -> None:

    # Load PDF files
    loader = PyPDFLoader("salads-database/E-Book-Salads-That-Satisfy.pdf")
    another_loader = PyPDFLoader("salads-database/salads-for-every-season-earthbound-farm-cookbook.pdf")
    last_loader = PyPDFLoader("salads-database/recipebook.pdf")
    
    # Load and split pages
    pages1 = loader.load_and_split()
    pages2 = another_loader.load_and_split()
    pages3 = last_loader.load_and_split()

    # Combine pages
    pages = pages1 + pages2 + pages3
    print(len(pages))
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50, separators=["\n\n","\n", " ", ""])
    documents = text_splitter.split_documents(documents=pages)
    print(len(documents))

    # Load embeddings and push to Pinecone
    embeddings = OpenAIEmbeddings()
    PineconeLangChain.from_documents(documents, embeddings, index_name = INDEX_NAME)
    print("All documents have been ingested into Pinecone!")





if __name__ == "__main__":
    
    ingest_pdf()
