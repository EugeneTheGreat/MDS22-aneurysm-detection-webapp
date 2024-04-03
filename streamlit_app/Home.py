import streamlit as st
import utils.ui_config as uiconf
from streamlit_extras.stylable_container import stylable_container as container 
from streamlit_extras.switch_page_button import switch_page as nav_to_page

############################## Page Configuration ##############################

# set the page configuration
st.set_page_config(page_title="Home", layout="wide", initial_sidebar_state="expanded")

# change background colour of the app
st.markdown(uiconf.pages_ui_config(), unsafe_allow_html=True)

st.sidebar.title("Home")

############################## Page Content ##############################

# the main columns in the home page
col1, col2 = st.columns(2, gap="large")

with col1:
    with container(
        key="app_name_container",
        css_styles=[
            """
            {
                border-radius: 25px;
                padding-top: 30px;
                padding-bottom: 30px;
                padding-left: 20px;
                background-color: #C2D7EA;
                margin-top: 200px;
            }
            """,
            """
            button {
                background-color: #67A750;
                border-radius: 15px;
                border-color: #67A750;
                color: black;
            }
            """]):
        title_txt = """
                    <h1 style="color:black">The Best Aneurysm Detector In The World</h1>
                    """
        subheader_txt = """
                        <h3 style="color:black">Powered By XAI</h3>
                        """
        body_txt = """
                   <p style="color:black">Application created by Team MDS22 from Monash University Malaysia. 
                                    <br>Project supervised by Dr Ting Fung Fung. <br><br></p>
                   """
        st.markdown(title_txt, unsafe_allow_html=True)
        st.markdown(subheader_txt, unsafe_allow_html=True)
        st.markdown(body_txt, unsafe_allow_html=True)
        get_started_button = st.button("Get Started")

        if get_started_button:
            nav_to_page("Aneurysm Detection")

with col2:
    with container(
        key="images_container",
        css_styles="""
            {
                padding: 10px;
                text-align: center;
            }
            """):
        st.image("resources/brain.png")
        st.write("Image source: [Source 1](https://www.hopkinsmedicine.org/health/conditions-and-diseases/cerebral-aneurysm), [Source 2](https://www.barrowneuro.org/condition/brain-aneurysm/), [Source 3](https://www.froedtert.com/brain-aneurysm)")
