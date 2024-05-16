import fnmatch
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.add_vertical_space import add_vertical_space
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
from subprocess import CalledProcessError

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
def predict(file_path, input_folder):
    with open(os.path.join(PROJECT_PATH, 'inference/config_inference.json'), 'r') as file:
        data = json.load(file)

    # Modify the value of a particular key
    data['demo_dir'] = file_path
    data['inference_outputs_path'] = os.path.join(STREAMLIT_PATH, 'outputs')

    # Write the modified JSON back to the file
    with open(os.path.join(PROJECT_PATH, 'inference/config_inference_streamlit.json'), 'w') as file:
        json.dump(data, file, indent=4)
    try:
        process = subprocess.run(["python",
                              os.path.join(PROJECT_PATH, "inference/patient_wise_sliding_window.py"),
                              "--config",
                              os.path.join(PROJECT_PATH, "inference/config_inference_streamlit.json")],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.check_returncode()
    except CalledProcessError as e:
        error_output = e.stderr.decode('utf-8')
        # Check for specific error cases and display custom messages
        if 'MultipleSubjectsError' in error_output:
            st.error("Mutiple subjects found in uploaded file; please include only one subject.")
        elif 'NoSubjectsError' in error_output:
            st.error("No subjects found in uploaded file; please include one subject with a proper directory name (eg. sub-123).")
        elif 'MissingDerivativesError' in error_output:
            st.error("Derivatives directory is missing or not structured correctly; please check zip file structure.")
        else:
            st.error(f"An error occurred: {error_output}.\nPlease check zip file structure or contact developers.")

        for dir in os.listdir(input_folder):
            shutil.rmtree(os.path.join(input_folder, dir))

        return
    
    return file_path  

def main():
    st.title('Intracranial Aneurysm Detection and Segmentation')
    add_vertical_space(3)
    st.subheader('Upload TOF-MRA Image (.zip)')

    # warning message
    st.warning('''
        **Kindly read this before uploading any file.**  
        1. File types accepted is only .zip. Please upload only a single .zip file!  
        2. The root of the .zip file must contain exactly one directory (call it input directory), i.e., one single folder.  
        3. The input directory must contain two directories: the subject directory whose name starts with “sub-” followed by three digits, and the derivatives directory named “derivatives”.  
        4. The subject directory should contain the session directory whose name starts with “ses-” followed by six digits (the session date in ‘yyyymmdd’ format), whereas the session directory should contain a directory named “anat”, which itself contains the NIfTI TOF-MRA images and machine parameter JSON files.  
        5. The derivatives directory contains the subject’s derivative files; it should contain three directories at its root: “manual_masks”, “N4_bias_field_corrected” and “registrations”.  
        6. The “manual_masks” directory should have the following directory hierarchy: subject-code > session-date > anat > mask files. This is similar to the structure in rules 2 and 3.  
        7. Similar to rule 6, the “N4_bias_field_corrected” directory should have the following directory hierarchy: subject-code > session-date > anat > N4 bias field corrected files.   
        8. The “registrations” directory should contain three subdirectories: “reg_metrics”, “reg_params” and “vesselMNI_2_angioTOF”.  
        9. Each “registrations” subdirectory should have a directory hierarchy similar to that of rules 5 and 6, with the base containing their respective files.  
               
        **Please refer to the End User Guide for full details (including examples).**
    ''', icon="⚠️")

    uploaded_file = st.file_uploader("Upload input zip file (.zip)...", type="zip")

    os.makedirs(os.path.join(STREAMLIT_PATH, 'upload'), exist_ok=True)
    input_folder = os.path.join(STREAMLIT_PATH, 'upload')
    os.makedirs(os.path.join(STREAMLIT_PATH, 'outputs'), exist_ok=True)
    output_folder = os.path.join(STREAMLIT_PATH, 'outputs')

    if uploaded_file is not None:
        with ZipFile(uploaded_file, 'r') as zObject:
            with st.spinner("Processing files..."):
                zObject.extractall(path=input_folder)

        if len(os.listdir(input_folder)) != 1:   # no folders or more than one folder was extracted
            st.error("Zip file must contain exactly one directory at its root!")
            for dir in os.listdir(input_folder):
                shutil.rmtree(os.path.join(input_folder, dir))

            return
        
        if 'last_uploaded_file' in st.session_state and st.session_state.last_uploaded_file != uploaded_file:
            st.session_state.button_clicked = False
            st.session_state.prediction_done = False
        st.session_state.last_uploaded_file = uploaded_file


        # Display the uploaded image
        add_vertical_space(2)
        st.subheader('Detect Uploaded TOF-MRA Image')   

        if st.button('Detect and Segment Aneurysms') or st.session_state.get('button_clicked', False):
            st.session_state.button_clicked = True
            if not st.session_state.get('prediction_done', False):
                with st.spinner("Model running (this may take a while...)"):
                    inference = predict(os.path.join(input_folder, os.listdir(input_folder)[0]), input_folder)
                    # terminate application
                    if inference is None:
                        return
                st.session_state.prediction_done = True

            # Display segmented image
            add_vertical_space(2)
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

            # no aneurysms found
            if len(original_to_display) == 0:
                st.success("No aneurysms detected!")
                for dir in os.listdir(input_folder):
                    shutil.rmtree(os.path.join(input_folder, dir))

                return

            # Define a list of options for the dropdown
            options = [str(i+1) for i in range(len(original_to_display) // 3)]
            # Create the dropdown and store the selected value
            selected_option = str(int(st.selectbox('Result No.:', options))-1)
                            
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

                st.info("These are slices of the original image where aneurysms were detected.", icon="ℹ️")

                for file_path in original_to_display:
                    file = file_path.split('/')
                    if selected_option == file[-1].split('_')[1]:
                        st.subheader(f'Slice Number: {file[-1].split("_")[5].split(".")[0]}')
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        plt.figure(figsize=(10,10))
                        plt.imshow(Image.open(file_path))
                        plt.axis('off')  # Turn off axis
                        st.pyplot()  # Display the plot in Streamlit
                

            with tab2:
                st.header("Segmentation")

                st.info("Detected aneurysms are highlighted in purple.", icon="ℹ️")
                
                for i in range(len(segmentation_to_display)):
                    file = segmentation_to_display[i].split('/')
                    if file[-1].split('_')[1] == selected_option:
                        st.subheader('Slice Number: ' + file[-1].split('_')[5].split(".")[0])
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        plt.figure(figsize=(10,10))
                        plt.imshow(Image.open(segmentation_to_display[i]))
                        plt.axis('off')  # Turn off axis
                        st.pyplot()  # Display the plot in Streamlit
                        
                
            with tab3:
                st.header("Explanation")

                st.info("These are slices with Grad-CAM heatmaps to explain AI decisions.", icon="ℹ️")
                
                for i in range(len(explanation_to_display)):
                    file = explanation_to_display[i].split('/')
                    if file[-1].split('_')[1] == selected_option:
                        st.subheader('Slice Number: ' + file[-1].split('_')[5].split(".")[0])
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        plt.figure(figsize=(10,10))
                        plt.imshow(Image.open(explanation_to_display[i]))
                        plt.axis('off')  # Turn off axis
                        st.pyplot()  # Display the plot in Streamlit

            for dir in os.listdir(input_folder):
                shutil.rmtree(os.path.join(input_folder, dir))

############################## Main Function ##############################

if __name__ == '__main__':
    setup_page()

    with open("streamlit_app/config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    profile_authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["pre-authorized"],
    )

    if st.session_state["authentication_status"]:
        main()
    else:
        st.switch_page("Home.py")

    uiconf.page_footer()
