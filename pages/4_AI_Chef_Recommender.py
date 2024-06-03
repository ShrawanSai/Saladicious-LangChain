import streamlit as st
from backend.alternate_suggestor import user_also_liked

st.set_page_config(page_title="Saladicious AI Recommeder", page_icon="🥗")
st.sidebar.header("Saladicious AI Recommeder")

st.title("Saladicious AI Recommeder")

st.header("Recommendation System for customers who liked a particular salad")
st.write("This system will recommed other salads that are similar to the one the customer liked. Simply type in the name of the salad and a brief description of it and we will provide you with a name and description for the salad.")

description = st.text_area("Enter the name and a brief description of your salad here:")
if st.button("Generate Similar Salad recipes") and description:
    with st.spinner("Coming up with recommendations..."):
        salads = user_also_liked(description)
        for salad in salads:
            st.markdown(salad)
      
        