import streamlit as st
import utils.ui_config as uiconf
from streamlit_extras.stylable_container import stylable_container as container
from streamlit_extras.switch_page_button import switch_page as nav_to_page
from streamlit_extras.card import card
from streamlit_extras.grid import grid

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
                margin-bottom: 100px
            }
            """,
            """
            button {
                background-color: #67A750;
                border-radius: 15px;
                border-color: #67A750;
                color: black;
            }
            """,
        ],
    ):
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
            """,
    ):
        st.image("resources/brain.png")
        st.write(
            "Image source: [Source 1](https://www.hopkinsmedicine.org/health/conditions-and-diseases/cerebral-aneurysm), [Source 2](https://www.barrowneuro.org/condition/brain-aneurysm/), [Source 3](https://www.froedtert.com/brain-aneurysm)"
        )


# the links to papers for aneurysm
col3, col4, col5 = st.columns(3, gap="small")

with col3:
    card(
        title="What Is Brain Aneurysm?",
        text="",
        image="https://www.mayoclinic.org/-/media/kcms/gbs/patient-consumer/images/2013/08/26/10/36/ds00582_im02314_r7_brainaneurysmthu_jpg.jpg",
        url="https://www.mayoclinic.org/diseases-conditions/brain-aneurysm/symptoms-causes/syc-20361483",
        styles={
            "card": {
                "width": "320px",
                "height": "320px",
                "border-radius": "50px",
                "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                "display": "block",
            },
            "div": {
                "background-color": "#485270",
                "padding-left": "15px",
                "margin-left": "auto",
                "margin-right": "auto",
            },
            "title": {
                "margin-top": "100px",
                "color": "black",
                "text-shadow": "-1px 0 white, 0 1px white, 1px 0 white, 0 -1px white",
                "background-color": "rgba(0, 0, 0, 0.4)",
            },
            "filter": {"background-color": "rgba(0, 0, 0, 0.2)"},
        },
    )

with col4:
    card(
        title="About Brain Aneurysms",
        text="",
        image="https://www.dradamrennie.com/wp-content/uploads/2018/01/aneurysm-2.jpg",
        url="https://www.dradamrennie.com/portfolio/brain-aneurysms/",
        styles={
            "card": {
                "width": "320px",
                "height": "320px",
                "border-radius": "50px",
                "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                "display": "block",
            },
            "div": {
                "background-color": "#485270",
                "padding-left": "15px",
                "margin-left": "auto",
                "margin-right": "auto",
            },
            "title": {
                "margin-top": "100px",
                "color": "black",
                "text-shadow": "-1px 0 white, 0 1px white, 1px 0 white, 0 -1px white",
                "background-color": "rgba(0, 0, 0, 0.4)",
            },
            "filter": {"background-color": "rgba(0, 0, 0, 0.2)"},
        },
    )

with col5:
    card(
        title="How Common Are Brain Aneurysms?",
        text="",
        image="https://post.medicalnewstoday.com/wp-content/uploads/sites/3/2023/02/brain_aneurysms_Stocksy_txp9b618f0bw0e300_Medium_1087981_Header-1024x575.jpg",
        url="https://www.medicalnewstoday.com/articles/how-common-are-brain-aneurysms",
        styles={
            "card": {
                "width": "320px",
                "height": "320px",
                "border-radius": "50px",
                "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                "display": "block",
            },
            "div": {
                "background-color": "#485270",
                "padding-left": "15px",
                "margin-left": "auto",
                "margin-right": "auto",
            },
            "title": {
                "margin-top": "100px",
                "color": "black",
                "text-shadow": "-1px 0 white, 0 1px white, 1px 0 white, 0 -1px white",
                "background-color": "rgba(0, 0, 0, 0.4)",
            },
            "filter": {"background-color": "rgba(0, 0, 0, 0.2)"},
        },
    )
