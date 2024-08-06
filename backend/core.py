from dotenv import load_dotenv
import os
from backend import nutrientanalysis
import requests
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeLangChain
INDEX_NAME = "saladicious-docs-dataset"
from typing import Any, List, Dict
import pandas as pd

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def run_llm(query:str) ->Any:
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeLangChain.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)

    chat = ChatOpenAI(verbose=True, temperature=0)

    qa = RetrievalQA.from_chain_type(llm = chat, chain_type = "stuff", retriever = docsearch.as_retriever(), return_source_documents = True)
    print(qa({"query":query}))

    return qa({"query":query})

def run_llm_for_chat(query:str, chat_history:List[Dict[str,Any]] = []) ->Any:
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeLangChain.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)

    chat = ChatOpenAI(verbose=True, temperature=0)

    qa = ConversationalRetrievalChain.from_llm(llm = chat, retriever = docsearch.as_retriever(), return_source_documents = False)

    return qa({"question":query, "chat_history":chat_history})

def get_alternate_ingredients(ingredient:str) -> Any:

    query = f"Suggest alternatives for {ingredient}. Give me the answer in a list. Give me only a numbered list of not more than 5 items. No other information is needed. Just the list."

    return run_llm(query)['result']

def get_best_pairings(ingredient:str, category:str) -> Any:

    query = f"Suggest what ingredients go best with these ingridents. The ingrident(s) are: {ingredient}. The ingredients you suggest must be a {category} Give me only a numbered list of not more than 7 ingredients."

    return run_llm(query)['result']


def nutritional_analysis(ingridients:str) -> Any:

    clean_ingridients,quantities = nutrientanalysis.clean_salad_ingredients_list(ingridients)

    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    response = requests.get(api_url + clean_ingridients,
                             headers=
                             {'X-Api-Key': os.getenv("CALORIE_NINJA_API_KEY")
                               })
    if response.status_code == requests.codes.ok:
        json_obj = []
        for item in response.json()['items']:
            if item['name'] in clean_ingridients:
                json_obj.append(item)
        calorie_summary, total_stats, individual_ingredients_stats = nutrientanalysis.get_total_calories_and_stats(response.json()['items'],quantities)
        suggestions = nutrientanalysis.get_ai_analysis(calorie_summary)
        return suggestions, total_stats, individual_ingredients_stats, clean_ingridients
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":

    query1 = "Suggest vegtables that go well with Brocolli. Give me only a numbered set of 5 vegtables."
    query2 = "Suggest alternatives for basil. Give me the answer in a list."
    query3 = "What dressings are low fat? Give me a list of dressings."
    query4 = "Give me a list of high protien ingridents I can add with potatoes. Give me a numbered list of ingridents."

    #print(nutritional_analysis("beetroot carrot apple banana"))
    
    # print(nutrientanalysis.get_ai_analysis("""1. total_calories: 221.6
    #     2. total_fat: 0.9000000000000001
    #     3. total_protein: 3.9
    #     4. total_carbs: 55.599999999999994
    #     5. total_sugar: 34.0
    #     6. total_sodium: 135.0
    #     7. total_fat_saturated: 0.1
    #     8. total_cholesterol: 0.0
    #     9. total_fiber: 10.0
    #     10. toal_pottasium: 101.0"""))
    #         #result = run_llm(query4)['result']

    #print(result)
    



