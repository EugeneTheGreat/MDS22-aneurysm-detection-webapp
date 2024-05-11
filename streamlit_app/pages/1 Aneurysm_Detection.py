import fnmatch
import streamlit as st
import utils.ui_config as uiconf
import glob
from pathlib import Path
import shutil
from matplotlib import pyplot as plt
import streamlit as st
import requests
import tempfile
import nibabel as nib
import os
import json
import subprocess
from zipfile import ZipFile
from PIL import Image

PROJECT_PATH = '.'
STREAMLIT_PATH = './streamlit_app'
############################## Page Configuration ##############################

def setup_page():
    """ Sets up the UI configuration of the page.
    """
    # set the page configuration
    st.set_page_config(
        page_title="Aneurysm Detection",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # change background colour of the app
    st.markdown(uiconf.pages_ui_config(), unsafe_allow_html=True)


############################## Page Content ##############################

# Function to perform prediction
def predict(file_path):
    with open(os.path.join(PROJECT_PATH, 'inference/config_inference.json'), 'r') as file:
        data = json.load(file)

    # Modify the value of a particular key
    data['demo_dir'] = file_path
    data['inference_outputs_path'] = os.path.join(STREAMLIT_PATH, 'outputs')

    # Write the modified JSON back to the file
    with open(os.path.join(PROJECT_PATH, 'inference/config_inference_streamlit.json'), 'w') as file:
        json.dump(data, file, indent=4)
    process = subprocess.run(["python",
                              os.path.join(PROJECT_PATH, "inference/patient_wise_sliding_window.py"),
                              "--config",
                              os.path.join(PROJECT_PATH, "inference/config_inference_streamlit.json")],
                              check=True, capture_output=True, text=True)
    
    return file_path  

def main():
    st.title('Intracranial Aneurysm Detection and Segmentation')

    st.subheader('Upload TOF-MRA Image (.zip)')
    st.warning('File types accepted is only .zip. Please upload only a single .zip file!', icon="⚠️")
    uploaded_file = st.file_uploader("Upload input zip file (.zip)...", type="zip")

    os.makedirs(os.path.join(STREAMLIT_PATH, 'upload'), exist_ok=True)
    input_folder = os.path.join(STREAMLIT_PATH, 'upload')
    os.makedirs(os.path.join(STREAMLIT_PATH, 'outputs'), exist_ok=True)
    output_folder = os.path.join(STREAMLIT_PATH, 'outputs')

    if uploaded_file is not None:
        with ZipFile(uploaded_file, 'r') as zObject:
            with st.spinner("Processing files..."):
                zObject.extractall(path=input_folder)
        if 'last_uploaded_file' in st.session_state and st.session_state.last_uploaded_file != uploaded_file:
            st.session_state.button_clicked = False
            st.session_state.prediction_done = False
        st.session_state.last_uploaded_file = uploaded_file


        # Display the uploaded image
        st.subheader('Uploaded TOF-MRA Image')   

        if st.button('Detect and Segment Aneurysms') or st.session_state.get('button_clicked', False):
            st.session_state.button_clicked = True
            if not st.session_state.get('prediction_done', False):
                with st.spinner("Model running..."):
                    predict(os.path.join(input_folder, uploaded_file.name.split('.')[0]))
                st.session_state.prediction_done = True

            # Display segmented image
            st.subheader('Segmented Image with Detected Aneurysms')

            run_path = os.path.join(output_folder, sorted(os.listdir(output_folder))[-1])

            original_to_display = []
            segmentation_to_display = []
            explanation_to_display = []

            for sub in os.listdir(run_path):
                if sub.startswith('sub'):
                    for ses in os.listdir(os.path.join(run_path, sub)):
                        if ses.startswith('ses'):
                            for root, dirs, files in os.walk(os.path.join(run_path, sub, ses)):
                                for file in files:
                                    if file.endswith('png'):
                                        if file.startswith('original'):
                                            original_to_display.append(os.path.join(run_path, sub, ses, 'original', file))
                                        elif file.startswith('segm'):
                                            segmentation_to_display.append(os.path.join(run_path, sub, ses, 'segmentation', file))
                                        elif file.startswith('explanation'):
                                            explanation_to_display.append(os.path.join(run_path, sub, ses, 'explanation', file))



            # Define a list of options for the dropdown
            options = [str(i) for i in range(len(original_to_display) // 3)]
            # Create the dropdown and store the selected value
            selected_option = st.selectbox('Result No.:', options)
                            
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

            tab1, tab2, tab3 = st.tabs(["Original", "Segmentation", "Explanation"])

            with tab1:
                st.header("Original")

                
                for file_path in original_to_display:
                    file = file_path.split('/')
                    if selected_option == file[-1].split('_')[1]:
                        st.subheader(f'Slice Number: {file[-1].split("_")[5].split(".")[0]}')
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        plt.imshow(Image.open(file_path))
                        plt.axis('off')  # Turn off axis
                        st.pyplot()  # Display the plot in Streamlit
                

            with tab2:
                st.header("Segmentation")
                
                for i in range(len(segmentation_to_display)):
                    file = segmentation_to_display[i].split('/')
                    if file[-1].split('_')[1] == selected_option:
                        st.subheader('Slice Number: ' + file[-1].split('_')[5].split(".")[0])
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        plt.imshow(Image.open(segmentation_to_display[i]))
                        plt.axis('off')  # Turn off axis
                        st.pyplot()  # Display the plot in Streamlit
                        
                
            with tab3:
                st.header("Explanation")
                
                for i in range(len(explanation_to_display)):
                    file = explanation_to_display[i].split('/')
                    if file[-1].split('_')[1] == selected_option:
                        st.subheader('Slice Number: ' + file[-1].split('_')[5].split(".")[0])
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        plt.imshow(Image.open(explanation_to_display[i]))
                        plt.axis('off')  # Turn off axis
                        st.pyplot()  # Display the plot in Streamlit

            for dir in os.listdir(input_folder):
                shutil.rmtree(os.path.join(input_folder, dir))

############################## Main Function ##############################

if __name__ == '__main__':
    setup_page()
    main()
