from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from typing import Any, List, Dict
import pandas as pd
import os

load_dotenv()


def get_total_calories_and_stats(ingridients:List) -> Any:

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

    ingridient_stats_list = []
    
    for ingridient in ingridients:
        total_calories += float(ingridient['calories'])
        total_fat += float(ingridient['fat_total_g'])
        total_protein += float(ingridient['protein_g'])
        total_carbs += float(ingridient['carbohydrates_total_g'])
        total_sugar += float(ingridient['sugar_g'])
        total_sodium += float(ingridient['sodium_mg'])
        total_fat_saturated += float(ingridient['fat_saturated_g'])
        total_cholesterol += float(ingridient['cholesterol_mg'])
        total_fiber += float(ingridient['fiber_g'])
        toal_pottasium += float(ingridient['potassium_mg'])
        ingridient_stats_list.append(ingridient)
    
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


    ingridient_stats_df = pd.DataFrame(ingridient_stats_list)
    calorie_summary = "\n".join([f"{index+1}. {key}: {value}" for index, (key, value) in enumerate(total_stats.items())])
    
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

    question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

    return llm_chain.invoke(question)
