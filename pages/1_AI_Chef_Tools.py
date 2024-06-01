import streamlit as st
from streamlit_chat import message
from backend.core import get_alternate_ingredients, get_best_pairings, nutritional_analysis
from backend.nutrientanalysis import get_ai_analysis, get_total_calories_and_stats

st.set_page_config(page_title="Saladicious AI Salad Chef Tools")
st.sidebar.header("Saladicious AI Salad Chef Tools")

st.title("Saladicious AI Salad Chef Tools")

st.header("Ingredient Substitution")
st.write("This tool helps you find alternative ingredients for a given ingredient. For example, if you are out of basil, you can use this tool to find alternatives for basil.")
ingredient = st.text_input("Enter the ingredient for which you want to find alternatives:")
if st.button("Find Alternatives") and ingredient:
    result = get_alternate_ingredients(ingredient)
    st.write(result)


st.header("Better Pairings")
st.write("This tool helps you find the best pairings for a given ingredient. For example, if you have broccoli, you can use this tool to find what other ingredients go well with broccoli.")
pairing_ingredient = st.text_input("Enter the ingredient/ingridents for which you want to find pairings:")
category = st.selectbox("Select the category of ingredients you want to pair with:", ("vegetable", "fruit", "protein", "dressing", "carb", "spice"))
if st.button("Find Pairings") and pairing_ingredient and category:
    result = get_best_pairings(pairing_ingredient, category)
    st.write(result)


st.header("Tool 3: Nutritional Analysis")
st.write("This tool provides a detailed nutritional analysis of a salad based on its ingredients and suggests any poetential improvements.")
salad_info = st.text_area("Enter the ingredients of the salad:")
if st.button("Analyze Salad") and salad_info:
    suggestions, total_stats, individual_ingredients_stats_df = nutritional_analysis(salad_info)
    st.write("Suggestions:", suggestions)
    st.write("Total Stats:", total_stats)
    st.write("Individual Ingredients Stats:")
    st.write(individual_ingredients_stats_df)
    
# Code for Tool 3 goes here


