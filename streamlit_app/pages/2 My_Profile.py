import streamlit as st
import utils.ui_config as uiconf
from streamlit_extras.stylable_container import stylable_container as container
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

############################## Profile Class ##############################
class ProfilePage:
    """
    A class that shows the home page of the web page.
    """

    def config_page(self):
        """
        Configures the page when created. 
        """
        # set the page configuration
        st.set_page_config(
            page_title="My Profile",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # change background colour of the app
        st.markdown(uiconf.pages_ui_config(), unsafe_allow_html=True)

        st.title("My Profile")

    def update_config(self):
        """
        Update the user details in the config.yaml file after updates.
        Includes new registration, password update and user detail updates.
        """
        with open("config.yaml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)

    def page_content(self, authenticator):
        """
        The content of the profile page. 
        """
        with container(
                key="profile_container",
                css_styles=[
                    """
                    {
                        border-radius: 25px;
                        padding-top: 20px;
                        padding-bottom: 30px;
                        padding-left: 40px;
                        background-color: #C2D7EA;
                        margin-top: 10px;
                        margin-bottom: 50px
                    }
                    """,
                ],
            ):
                username_title = """
                                <h4 style="color:black; text-align:right">Username: </h4>
                                """
                username = f"""
                            <h4 style="color:black; text-align:left">{st.session_state["name"]}</h4>
                            """
                
                col1, col2 = st.columns([0.12, 0.88], gap="small")

                with col1:
                    st.markdown(username_title, unsafe_allow_html=True)
                with col2:
                    st.markdown(username, unsafe_allow_html=True)

        # set the style of the tabs 
        st.markdown("""
                    <style>
                        .stTabs [data-baseweb="tab-list"] {
                            gap: 12px;
                        }

                        .stTabs [data-baseweb="tab"] {
                            height: 40px;
                            white-space: pre-wrap;
                            border-radius: 10px 10px 10px 10px;
                            gap: 5px;
                            padding-top: 10px;
                            padding-bottom: 10px;
                            padding-left: 10px;
                            padding-right: 10px;
                            margin-bottom: 10px;
                        }

                        .stTabs [aria-selected="true"] {
                            background-color: #C2D7EA;
                        }

                    </style>""", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Reset Password", "Update Details"])

        with tab1:
             if st.session_state["authentication_status"]:
                try:
                    if authenticator.reset_password(st.session_state["username"]):
                        self.update_config()
                        st.success('Password modified successfully')
                except Exception as e:
                    st.error(e)

        with tab2:
            if st.session_state["authentication_status"]:
                try:
                    if authenticator.update_user_details(st.session_state["username"]):
                        self.update_config()
                        st.success('Entries updated successfully')
                except Exception as e:
                    st.error(e)
             

############################## Main Function ##############################

if __name__ == "__main__":
    profile = ProfilePage()
    profile.config_page()

    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["pre-authorized"],
    )

    profile.page_content(authenticator)
