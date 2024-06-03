from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from typing import Any, List, Dict
import pandas as pd
import os

load_dotenv()



def get_name_and_description(salad_info:str) -> Any:

    template = """
    Given the descrption of the salad abd its ingredients below, provide a one paragraph description of the salad to add to a daily menu.
    The description must be engaging and informative. The description must include only the main ingredients of the salad.
    Also make sure to include a brief note on the nutritional value of the salad (e.g. low-calorie, high-protein, vegan-friendly, etc.)
    The description must be no more than 250 words.

    Keep in mind the following guidelines:
    When crafting captivating salad descriptions for a weekly subscription service, it's crucial to evoke imagery, highlight freshness,
    and appeal to the senses. Begin by introducing the salad's star ingredients, emphasizing their quality and origin to evoke a 
    sense of freshness and sustainability. Use descriptive language to evoke the salad's texture, flavor profile, and visual appeal, 
    painting a vivid picture for subscribers. Incorporate sensory details such as vibrant colors, crisp textures, and enticing 
    aromas to stimulate the reader's imagination. Consider incorporating storytelling elements to connect the salad to a narrative 
    or theme, adding depth and intrigue to the description. Lastly, provide dietary information, flavor pairings, and serving 
    suggestions to empower subscribers in their culinary exploration and encourage experimentation with flavors and ingredients. 
    Remember, the goal is to entice subscribers with mouthwatering descriptions that not only showcase the salads' ingredients but 
    also ignite their curiosity and excitement for each weekly offering.

    Salad Description: {salad_info}

    Give just description of the salad. Nothing else is needed.
    Answer:"""

    title_template = """ Given the description of the salad below, provide a creative name for the salad that is engaging and appealing.
    The name should be descriptive and evoke the essence of the salad's main ingredients and flavors. It should be catchy, memorable,
    and reflect the salad's unique character. The name should be no more than 5 words.

    Salad Description: {description}
    """

    prompt = PromptTemplate.from_template(template)

    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

    llm_chain = prompt | llm

    description = llm_chain.invoke(salad_info)

    title_prompt = PromptTemplate.from_template(title_template)
    llm_chain = title_prompt | llm
    title = llm_chain.invoke({"description":description})
    

    return title, description

if __name__ == "__main__":
    print(get_name_and_description("A greek salad consisting of fresh vegetables like tomatoes, cucumbers, onions, and bell peppers, typically topped with Kalamata olives and feta cheese. It's seasoned with extra virgin olive oil, oregano, salt, and sometimes vinegar for a refreshing and flavorful combination that embodies the essence of Greek cuisine."))