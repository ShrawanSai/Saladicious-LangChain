import streamlit as st
from streamlit_chat import message


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.header("Hello! Welcome to the Saladicious Admin Page")
st.subheader("Here you can manage your salad menu, chat with the AI Chef, and more!")

st.subheader("Here are the links for weekly menu management:")
st.markdown("[Menu Website](https://shrawansai.github.io/saladicious.github.io/)")
st.markdown("[Google Sheet](https://docs.google.com/spreadsheets/d/1Sh-0lCLnAWM2wCgGur7G6-9K-Ew7M8GtceMSsvmS5xg/edit?usp=sharing)")


        