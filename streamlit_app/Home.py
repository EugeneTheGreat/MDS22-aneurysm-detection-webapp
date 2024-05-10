import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.stylable_container import stylable_container as container
from streamlit_extras.card import card
from streamlit_extras.let_it_rain import rain
import utils.ui_config as uiconf
import yaml
from yaml.loader import SafeLoader

############################## Home Page Class ##############################


class HomePage:
    """
    A class that shows the home page of the web page.
    """

    def set_page_config(self):
        """
        Sets the page configuration.
        """
        st.set_page_config(
            page_title="Home",
            layout="wide",
            initial_sidebar_state=st.session_state.get("sidebar_state", "expanded"),
        )

        # change background colour of the app
        st.markdown(uiconf.pages_ui_config(), unsafe_allow_html=True)
        st.session_state.sidebar_state = "collapsed"

        # initialise the session state for determining the display of login or signup screen
        if "is_signup" not in st.session_state:
            st.session_state["is_signup"] = False

    def get_user_name(self):
        """
        Returns the name of the logged in user.
        """
        return st.session_state["name"]

    def hide_sidebar(self, sb_state):
        """
        Hides the sidebar of the page.
        """
        st.session_state.sidebar_state = sb_state
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

    def update_config(self):
        """
        Update the user details in the config.yaml file after updates.
        Includes new registration, password update and user detail updates.
        """
        with open("config.yaml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)

    def toggle_is_signup(self):
        """
        Toggle to show either the sign up screen or the login screen.
        """
        if st.session_state.is_signup:
            st.session_state.is_signup = False
        elif not st.session_state.is_signup:
            st.session_state.is_signup = True

    def page_authentication(self, authenticator):
        """
        Display either the sign up page or login page.
        """
        if st.session_state.is_signup:
            self.page_signup(authenticator)
        elif not st.session_state.is_signup:
            self.page_login(authenticator)

    def page_login(self, authenticator):
        """
        Page login logic.
        """
        name, _, _ = authenticator.login()

        placeholder = st.empty()

        if st.session_state["authentication_status"]:  # authenticated
            if name == "Guest":  # if guest login
                self.hide_sidebar("collapsed")
                placeholder.empty()
                st.title(f'Welcome *{self.get_user_name()}*!')
                self.page_content(have_detect_button=False)

                col1, col2 = st.columns([0.55, 0.45], gap="small")
                with col1:
                    guest_message = """
                                    <p style="text-align:right">Interested? Login or sign up now!</p>
                                    """
                    st.markdown(guest_message, unsafe_allow_html=True)
                with col2:
                    logout_button = authenticator.logout("Login/SignUp", "main")
            else:  # user login
                placeholder.empty()
                st.session_state.sidebar_state = "expanded"
                st.title(f'Welcome back *{self.get_user_name()}*!')
                self.page_content()

                authenticator.logout("Logout", "sidebar", "home_logout")

        elif st.session_state["authentication_status"] is False:  # cannot authenticate user
            self.hide_sidebar("collapsed")
            st.error("Username/password is incorrect! Kindly sign up if you do not have an account! 🙂")
            st.info(":green[Guest Username: guest ; Guest Password: Guest123]", icon="✅")

            with placeholder.container():
                col1, col2 = st.columns([0.55, 0.45], gap="small")

                with col1:
                    login_message = """
                                    <p style="text-align:right">Don't have an account?  Sign up now!</p>
                                    """
                    st.markdown(login_message, unsafe_allow_html=True)
                with col2:
                    st.button("Sign Up", on_click=self.toggle_is_signup)

        elif st.session_state["authentication_status"] is None:  # no authentication yet
            self.hide_sidebar("collapsed")
            st.info("Please enter your username and password", icon="ℹ️")
            st.info(":green[Guest Username: guest ; Guest Password: Guest123]", icon="✅")

            with placeholder.container():
                col1, col2 = st.columns([0.55, 0.45], gap="small")

                with col1:
                    login_message = """
                                    <p style="text-align:right">Don't have an account?  Sign up now!</p>
                                    """
                    st.markdown(login_message, unsafe_allow_html=True)
                with col2:
                    st.button("Sign Up", on_click=self.toggle_is_signup)

    def page_signup(self, authenticator):
        """
        Page sign up logic.
        """
        self.hide_sidebar("collapsed")

        try:
            email_of_registered_user, _, _ = authenticator.register_user(pre_authorization=False)

            if email_of_registered_user:
                self.update_config()
                rain(emoji="🎈", font_size=54, falling_speed=5, animation_length=3)
                st.success("User registered successfully")
        except Exception as e:
            st.error(e)

        col1, col2 = st.columns([0.55, 0.45], gap="small")

        with col1:
            login_message = """
                            <p style="text-align:right">Have an account?   Login now!</p>
                            """
            st.markdown(login_message, unsafe_allow_html=True)
        with col2:
            st.button("Login", on_click=self.toggle_is_signup)

    def page_content(self, have_detect_button=True):
        """
        Displays the main content of the homepage after logging into the application.
        """
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

                if have_detect_button:
                    get_started_button = st.button("Get Started")

                    if get_started_button:
                        st.switch_page("pages/1 Aneurysm_Detection.py")

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
                image="http://myhealth.moh.gov.my/wp-content/uploads/brain_aneurysm1.jpg",
                url="http://myhealth.moh.gov.my/en/brain-aneurysm/",
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


############################## Main Function ##############################

if __name__ == "__main__":
    home = HomePage()
    home.set_page_config()

    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["pre-authorized"],
    )

    home.page_authentication(authenticator)