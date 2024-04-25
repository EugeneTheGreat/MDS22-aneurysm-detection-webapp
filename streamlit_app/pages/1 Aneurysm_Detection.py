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

PROJECT_PATH = '/home/student/Documents/MDS22/Aneurysm_Detection_dev'
STREAMLIT_PATH = '/home/student/Documents/MDS22/Aneurysm_Detection_dev/streamlit_app'
############################## Page Configuration ##############################

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

    st.subheader('Upload TOF-MRA Image (.nii)')
    uploaded_file = st.file_uploader("Upload input zip file (.zip)...", type="zip")

    os.makedirs(os.path.join(STREAMLIT_PATH, 'upload'), exist_ok=True)
    input_folder = os.path.join(STREAMLIT_PATH, 'upload')
    os.makedirs(os.path.join(STREAMLIT_PATH, 'outputs'), exist_ok=True)
    output_folder = os.path.join(STREAMLIT_PATH, 'outputs')

    if uploaded_file is not None:
        with ZipFile(uploaded_file, 'r') as zObject:
            zObject.extractall(path=input_folder)

        # Display the uploaded image
        st.subheader('Uploaded TOF-MRA Image')   

        st.write("Uploaded file path:", input_folder)

        if st.button('Detect and Segment Aneurysms'):
            # url = 'http://127.0.0.1:5000/predict'
            # response = requests.post(url, json={'file_path': tmp_file_path})
            predict(os.path.join(input_folder, uploaded_file.name.split('.')[0] + '_zip'))  # hardcoded

            # Display segmented image
            st.subheader('Segmented Image with Detected Aneurysms')

            output_path = os.path.join(output_folder, sorted(os.listdir(output_folder))[-1])

            st.set_option('deprecation.showPyplotGlobalUse', False)
            # Display the middle slice of the image

            for root, dirs, files in os.walk(output_path):
                for file in files:
                    if file.endswith('png'):
                        to_display = os.path.join(root, file)
                        break
            
            plt.imshow(Image.open(to_display))
            plt.axis('off')  # Turn off axis
            st.pyplot()  # Display the plot in Streamlit

            for dir in os.listdir(os.path.join(STREAMLIT_PATH, input_folder)):
                shutil.rmtree(os.path.join(STREAMLIT_PATH, input_folder, dir))
            


############################## Main Function ##############################

if __name__ == '__main__':
    main()
