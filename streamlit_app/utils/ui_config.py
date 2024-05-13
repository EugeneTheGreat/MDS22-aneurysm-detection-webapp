import streamlit as st

def pages_ui_config():
    bg_config_colour = """
                        <style>
                        [data-testid="stAppViewContainer"] {
                            background-color: #485270;
                        }

                        [data-testid="stHeader"] {
                            background-color: #94ABC2;
                            color: #000000;
                        }

                        [data-testid="stSidebar"] {
                            background-color: #1f2433;
                        }

                        #MainMenu {
                                visibility: hidden;
                        }
                        </style>
                        """

    return bg_config_colour

def page_footer():
    """
    Page footer.
    """
    footer = """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #485270;
            color: white;
            text-align: center;
            padding-top: 12px;
        }
        </style>

        <div class='footer'>
            <p>Monash University FIT3164 Team MDS22 © 2024</p>
        </div>
        """
    st.markdown(footer, unsafe_allow_html=True)