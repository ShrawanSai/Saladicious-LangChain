import streamlit as st
from backend.regression_model import predict_usage

st.set_page_config(page_title="Saladicious Ingredient Usage Forecaster", page_icon="🥗")
st.sidebar.header("Saladicious Ingredient Usage Forecaster")

st.title("Saladicious Ingredient Usage Forecaster")

st.header("Predit how much of each ingredient needs to be in stock for a particular date based on past usage data")
st.write("This tool will predict how much of each ingredient needs to be in stock for a particular date based on past usage data. Simply enter the date and other details and the AI will do the rest!")
number_of_serving_communities = st.number_input("Enter the number of communities you are serving:", min_value=1, max_value=100)
date = st.date_input("Enter the date for which you want to predict the ingredient usage:")
sample_given = st.checkbox("Do you intend to give out samples on this date?")

if st.button("Generate Similar Salad recipes") and number_of_serving_communities and date and sample_given:
    with st.spinner("Coming up with estimates..."):
        if sample_given:
            sample_given = 1
        else:
            sample_given = 0
        res = predict_usage(number_of_serving_communities=number_of_serving_communities, sample_given=sample_given, date=date)
        for d in res:
            if "Lettuce_Usage" in d:
                st.subheader("Lettuce Usage (in g) :")
                st.markdown(res[d])
            if "Tomato_Usage" in d:
                st.subheader("Tomato Usage (in g) :")
                st.markdown(res[d])
            if "Chicken_Usage" in d:
                st.subheader("Chicken Usage (in g) :")
                st.markdown(res[d])
            if "Cheese_Usage" in d:
                st.subheader("Cheese Usage (Packets used) :")
                st.markdown(res[d])
            if "Onion_Usage" in d:
                st.subheader("Onion Usage (in g) :")
                st.markdown(res[d])
            
      