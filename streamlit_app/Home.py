import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.stylable_container import stylable_container as container
from streamlit_extras.add_vertical_space import add_vertical_space
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
    def __init__(self):
        """
        Sets the page configuration.
        """
        st.set_page_config(
            page_title="Home",
            layout="wide",
            initial_sidebar_state=st.session_state.get("sidebar_state", "expanded")
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
        with open("streamlit_app/config.yaml", "w") as file:
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
        name, _, _, _ = authenticator.login()

        placeholder = st.empty() # an empty container to hold some UI components 

        if st.session_state["authentication_status"]:  # authenticated
            if name == "Guest":  # if guest login
                self.hide_sidebar("collapsed")
                placeholder.empty()
                st.title(f'Welcome *{self.get_user_name()}*!')
                self.page_content(have_detect_button=False)

                with container(
                    key="guest_container",
                    css_styles=[
                        """
                        {
                            border-radius: 25px;
                            padding-top: 30px;
                            padding-bottom: 30px;
                            padding-left: 120px;
                            background-color: #C2D7EA;
                            margin-top: 80px;
                            margin-bottom: 40px
                        }
                        """,
                        """
                        button {
                            height: 55px;
                            border-radius: 15px;
                        }
                        """,
                    ],
                ):
                    col1, col2 = st.columns([0.50, 0.50], gap="small")

                    with col1:
                        subheader_txt = """
                                        <h1 style="color:black">Interested?</h1>
                                        """
                        body_txt = """
                                <h4 style="color:black">Login or sign up now</h4>
                                """
                        body_txt2 = """
                                    <p style="color:black">And start detecting!</p>
                                    """
                        add_vertical_space(4)
                        st.markdown(subheader_txt, unsafe_allow_html=True)
                        st.markdown(body_txt, unsafe_allow_html=True)
                        st.markdown(body_txt2, unsafe_allow_html=True)
                        add_vertical_space(5)
                    with col2:
                        add_vertical_space(7)
                        # go back to the authentication page 
                        guest_logout = authenticator.logout("Login or SignUp Now!", "main")

            else:  # registered user login
                placeholder.empty()
                st.session_state.sidebar_state = "expanded"
                st.title(f'Welcome back *{self.get_user_name()}*!')
                self.page_content()

                # app tips
                add_vertical_space(1)
                st.subheader("Some Great Tips!")
                add_vertical_space(1)
                with st.expander("Show Tips"):
                    self.page_tips_container("1. Remember to log out everytime before closing the app for extra security.")
                    self.page_tips_container("2. Mix uppercase, lowercase, numbers, and symbols in a memorable passphrase for robust password security.")
                    self.page_tips_container("3. Why did the password go to therapy? Because it couldn't find a safe place to save itself! Do save yours safely!")
                    self.page_tips_container("4. Ensure to clear detection results in My Profile page after each session.")

        elif st.session_state["authentication_status"] is False:  # cannot authenticate user
            self.hide_sidebar("collapsed")
            st.error("Username/password is incorrect! Kindly sign up if you do not have an account! 🙂")

            with placeholder.container():
                col1, col2, col3, col4 = st.columns([0.5, 0.1, 0.02, 0.38], gap="small")

                with col1:
                    login_message = """
                                    <p style="text-align:right">Don't have an account?  Sign up now!</p>
                                    """
                    st.markdown(login_message, unsafe_allow_html=True)
                with col2:
                    st.button("Sign Up", on_click=self.toggle_is_signup)

                with col3:
                    or_text = """
                                    <p style="text-align:center">or</p>
                                    """
                    st.markdown(or_text, unsafe_allow_html=True)

                with col4:
                    guest_login_button = st.button("Guest Login")

                    if guest_login_button:
                        username = "guest"
                        pw = "Guest123"
                        if authenticator.authentication_handler.check_credentials(username,
                                                                                    pw,
                                                                                    None,
                                                                                    None):
                            authenticator.authentication_handler.execute_login(username=username)
                            authenticator.cookie_handler.set_cookie()

        elif st.session_state["authentication_status"] is None:  # no authentication yet
            self.hide_sidebar("collapsed")
            st.info("Please enter your username and password", icon="ℹ️")

            with placeholder.container():
                col1, col2, col3, col4 = st.columns([0.5, 0.1, 0.02, 0.38], gap="small")

                with col1:
                    login_message = """
                                    <p style="text-align:right">Don't have an account?  Sign up now!</p>
                                    """
                    st.markdown(login_message, unsafe_allow_html=True)
                with col2:
                    st.button("Sign Up", on_click=self.toggle_is_signup)

                with col3:
                    or_text = """
                                    <p style="text-align:center">or</p>
                                    """
                    st.markdown(or_text, unsafe_allow_html=True)

                with col4:
                    guest_login_button = st.button("Guest Login")

                    if guest_login_button:
                        username = "guest"
                        pw = "Guest123"
                        if authenticator.authentication_handler.check_credentials(username,
                                                                                    pw,
                                                                                    None,
                                                                                    None):
                            authenticator.authentication_handler.execute_login(username=username)
                            authenticator.cookie_handler.set_cookie()

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
                st.image("streamlit_app/resources/brain.png")
                st.write(
                    "Image source: [Source 1](https://www.hopkinsmedicine.org/health/conditions-and-diseases/cerebral-aneurysm), [Source 2](https://www.barrowneuro.org/condition/brain-aneurysm/), [Source 3](https://www.froedtert.com/brain-aneurysm)"
                )

        # the links to papers for aneurysm
        add_vertical_space(4)
        st.subheader("See Also")
        col3, col4, col5 = st.columns(3, gap="small")

        with col3:
            card(
                title="What Is Brain Aneurysm?",
                text="",
                image="https://i0.wp.com/www.bafound.org/wp-content/uploads/2019/01/180091.jpg?w=400&ssl=1",
                url="https://www.bafound.org/about-brain-aneurysms/brain-aneurysm-basics/",
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

    def page_tips_container(self, tips):
        """
        Container to show tips for the app.
        """
        with container(
                    key="tips_container",
                    css_styles=[
                        """
                        {
                            border-radius: 15px;
                            padding-top: 20px;
                            padding-bottom: 20px;
                            padding-left: 50px;
                            background-color: #C2D7EA;
                            margin-top: 15px;
                            margin-bottom: 15px
                        }
                        """
                    ],
                ):
            txt = f"""
                        <h5 style="color:black">{tips}</h5>
                        """
            st.markdown(txt, unsafe_allow_html=True)

############################## Main Function ##############################

if __name__ == "__main__":
    home = HomePage()

    with open("streamlit_app/config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["pre-authorized"],
    )

    home.page_authentication(authenticator)

    uiconf.page_footer()