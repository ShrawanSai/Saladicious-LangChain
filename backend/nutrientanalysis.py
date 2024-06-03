from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from typing import Any, List, Dict
import pandas as pd
import os

load_dotenv()


def get_total_calories_and_stats(ingridients:List, quantities:List) -> Any:


    ingridient_stats_df = pd.DataFrame(ingridients)
    if len(ingridient_stats_df) != len(quantities):
        if len(quantities) > len(ingridient_stats_df):
            quantities = quantities[:len(ingridient_stats_df)]
        else:
            quantities = quantities + [0] * (len(ingridient_stats_df) - len(quantities))
    

    for column in ingridient_stats_df.columns:
            if column.lower() == 'name':
                continue
            ingridient_stats_df[column] = ingridient_stats_df[column] / ingridient_stats_df['serving_size_g']

    ingridient_names_df = ingridient_stats_df['name']
    ingredient_quantities_df = ingridient_stats_df.drop(columns=['name']).multiply(quantities, axis=0)
    
    ingridient_stats_df = pd.concat([ingridient_names_df, ingredient_quantities_df], axis=1)


    total_calories = 0
    total_fat = 0
    total_protein = 0
    total_carbs = 0
    total_sugar = 0
    total_sodium = 0
    total_fat_saturated = 0
    total_cholesterol = 0
    total_fiber = 0
    toal_pottasium = 0

    for index, ingridient in ingridient_stats_df.iterrows():
        total_calories += int(ingridient['calories'])
        total_fat += float(ingridient['fat_total_g'])
        total_protein += float(ingridient['protein_g'])
        total_carbs += float(ingridient['carbohydrates_total_g'])
        total_sugar += float(ingridient['sugar_g'])
        total_sodium += float(ingridient['sodium_mg'])
        total_fat_saturated += float(ingridient['fat_saturated_g'])
        total_cholesterol += float(ingridient['cholesterol_mg'])
        total_fiber += float(ingridient['fiber_g'])
        toal_pottasium += float(ingridient['potassium_mg'])
    
    
    total_stats = {
        "total_calories": total_calories,
        "total_fat": total_fat,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_sugar": total_sugar,
        "total_sodium": total_sodium,
        "total_fat_saturated": total_fat_saturated,
        "total_cholesterol": total_cholesterol,
        "total_fiber": total_fiber,
        "toal_pottasium": toal_pottasium
    }

    calorie_summary = "\n".join([f"{index+1}. {key.replace('_', ' ').capitalize()}: {value}" for index, (key, value) in enumerate(total_stats.items())])

    return calorie_summary,total_stats, ingridient_stats_df



def get_ai_analysis(salad_info:str) -> Any:

    template = """A balanced salad: To create a healthy, balanced salad, aim for the following nutrient proportions:

Total Calories: Ensure the salad is satisfying by targeting a moderate calorie range.
Total Fat: Include a moderate amount of healthy fats for nutrient absorption and satiety.
Total Protein: Add a generous portion of protein to help maintain muscle mass and keep you full.
Total Carbohydrates: Incorporate a balance of starchy and non-starchy vegetables, grains, and fruits.
Total Sugar: Focus on natural sugars from fruits, keeping added sugars low.
Total Sodium: Limit sodium to maintain healthy blood pressure.
Total Saturated Fat: Keep saturated fat low to support heart health.
Total Cholesterol: Monitor cholesterol intake, especially if concerned about heart health.
Total Fiber: Ensure a high fiber content for digestion and satiety.
Total Potassium: Include potassium-rich foods to balance sodium levels and support muscle function.
Proportions:
Carbohydrates: 1/3 of the salad
Protein: 1/4 of the salad
Healthy Fats: 1/5 of the salad
Vegetables/Fruits: The majority of the salad, ensuring a mix of non-starchy and starchy types.
Extras (like dressings and toppings): Use sparingly for added flavor and texture.
    
    Information and Total calories for this salad: {salad_info}
    
    Given this information, find what nutrients are in excess or are lacking in the salad.
    Write 1 sentence that summarizes the overall healthiness of the salad based on the nutrient proportions and targets.
    Suggest ingredients that can be added to make up for the lact of any nutrient. If any nutrient is in excess, 
    suggest removing ingredient types that contribute to that nutrient.
    Give a numbered list of not more than 3 suggestions.
    NO OTHER INFORMATION IS NEEDED. Just the give the one sentence summary and the numbered list of suggestions.
    Answer:"""

    prompt = PromptTemplate.from_template(template)

    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

    llm_chain = prompt | llm

    return llm_chain.invoke(salad_info)

def clean_salad_ingredients_list(salad_info:str) -> Any:

    template = """Reading through the salad ingredients list, identify all the ingredients and their quantities.
    Then create a numbered list of the ingredients and their quantities in the following format:
    1. Ingredient 1 serving size : Quantity 1 (in grams)
    2. Ingredient 2 serving size: Quantity 2 (in grams)
    
    The salad ingredients list is: 
    {salad_info}
    NO OTHER INFORMATION IS NEEDED. Just the give the numbered list of ingredients and quantities.
    Answer:"""

    template2 = """
    Create a single line which is a comma separated list with all of the quantities in grams for each item. If the 
    quantity is not available in grams, add a 0 for that item.
    The list should be in the following format:
    Quantity1, Quantity2, Quantity3, Quantity4, Quantity5

    The length of the list should be equal to the number of ingredients in the salad. {length} in this case.

    The salad ingredients list is:
    {text}

    Give only the comma separated list of {length} quantities in grams and nothing else.
    """

    prompt = PromptTemplate.from_template(template)

    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

    llm_chain = prompt | llm

    text = llm_chain.invoke(salad_info)
    length = text.count("\n")

    prompt2 = PromptTemplate.from_template(template2)
    llm_chain = prompt2 | llm
    quantities = llm_chain.invoke(
        {
            "text": text, 
            "length": length
        }
    )
    quantities = quantities.split(",")
    quantities = [float(x.strip()) for x in quantities]
    #quantities = [x.split(":")[-2].strip() for x in text.split("\n")]
    print(quantities)
    

    return text,quantities
