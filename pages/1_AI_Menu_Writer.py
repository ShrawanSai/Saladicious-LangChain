import streamlit as st
from streamlit_chat import message
from backend.description_creator import get_name_and_description

st.set_page_config(page_title="Saladicious AI Menu Helper", page_icon="🥗")
st.sidebar.header("Saladicious AI Salad Chef Tools")

st.title("Saladicious AI Menu Helper")

st.header("Menu and Description Creator")
st.write("This tool will create a creative name and description for your salad menu item. Just enter a brief description of the salad and the AI will do the rest!")

description = st.text_area("Enter a brief description of your salad here:")
if st.button("Create Name and Description"):
    with st.spinner("Creating Name and Description..."):
        title, description = get_name_and_description(description)
        st.subheader(title)
        st.markdown(description)