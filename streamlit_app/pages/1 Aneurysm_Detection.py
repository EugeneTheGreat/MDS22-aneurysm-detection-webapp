import streamlit as st
import utils.ui_config as uiconf

############################## Page Configuration ##############################

# set the page configuration
st.set_page_config(
    page_title="Aneurysm Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

# change background colour of the app
st.markdown(uiconf.pages_ui_config(), unsafe_allow_html=True)

st.sidebar.title("Aneurysm Detection")

st.title("Aneurysm Detection")

############################## Page Content ##############################
