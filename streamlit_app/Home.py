import streamlit as st
import utils.ui_config as uiconf
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils.home_content import page_content as content

############################## Page Configuration ##############################

# set the page configuration
st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state=st.session_state.get("sidebar_state", "collapsed"),
)

# change background colour of the app
st.markdown(uiconf.pages_ui_config(), unsafe_allow_html=True)

st.sidebar.title("Home")

st.session_state.sidebar_state = "collapsed"

############################## Authentication ##############################

# authentication
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["pre-authorized"],
)

authenticator.login()

if st.session_state["authentication_status"]:
    logout_button = authenticator.logout("Logout", "sidebar")
    st.session_state.sidebar_state = "expanded"
    if logout_button:
        st.markdown(
            """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
        </style>
        """,
            unsafe_allow_html=True,
        )
    content()
elif st.session_state["authentication_status"] is False:
    st.session_state.sidebar_state = 'collapsed'
    st.error("Username/password is incorrect")
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
elif st.session_state["authentication_status"] is None:
    st.session_state.sidebar_state = 'collapsed'
    st.warning("Please enter your username and password")
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
