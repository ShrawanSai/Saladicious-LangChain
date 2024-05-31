from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain.chains import RetrievalQA

from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeLangChain
INDEX_NAME = "saladicious-docs-dataset"
from typing import Any

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def run_llm(query:str) ->Any:
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeLangChain.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)

    chat = ChatOpenAI(verbose=True, temperature=0)

    qa = RetrievalQA.from_chain_type(llm = chat, chain_type = "stuff", retriever = docsearch.as_retriever(), return_source_documents = True)

    return qa({"query":query})

if __name__ == "__main__":

    query = "Suggest salad dressings that use olive oil as a base and are easy to prepare at home."

    result = run_llm(query)['result']

    print(result)
    



