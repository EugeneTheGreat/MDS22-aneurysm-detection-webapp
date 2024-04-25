import glob
from pathlib import Path
import shutil
from matplotlib import pyplot as plt
import streamlit as st
import requests
import tempfile
import nibabel as nib
import os



# Function to perform prediction
def predict(file_path):
    # process = subprocess.run(["python", "inference/patient_wise_sliding_window.py", "--config", "inference/config_inference.json", "--input_file", file_path], check=True, capture_output=True, text=True)
    return file_path

def main():
    st.title('Intracranial Aneurysm Detection and Segmentation')

    st.subheader('Upload TOF-MRA Image (.nii)')
    uploaded_file = st.file_uploader("Choose a TOF-MRA image (.nii.gz)...",accept_multiple_files=True)
    save_folder = "C:\\Users\\navee\\Downloads\\Aneurysm_Detection-main\\Aneurysm_Detection-main\\upload"


    for files in uploaded_file:
        save_path = Path(save_folder, files.name)
        with open(save_path, mode='wb') as w:
                w.write(files.getvalue())

    if len(uploaded_file) != 0:
        # Display the uploaded image
        st.subheader('Uploaded TOF-MRA Image')   

        st.write("Uploaded file path:", save_folder)

        if st.button('Detect and Segment Aneurysms'):
            # url = 'http://127.0.0.1:5000/predict'
            # response = requests.post(url, json={'file_path': tmp_file_path})
            prediction = predict(save_path)


            # Display segmented image
            st.subheader('Segmented Image with Detected Aneurysms')
            # Load the NIfTI file
            nii_img = nib.load("C:\\Users\\navee\\Downloads\\Aneurysm_Detection-main\\Aneurysm_Detection-main\\upload\\sub-001_ses-20101222_desc-angio_N4bfc_brain_mask.nii")
            img_data = nii_img.get_fdata()

            st.set_option('deprecation.showPyplotGlobalUse', False)
            # Display the middle slice of the image
            middle_slice = img_data.shape[2] // 2
            plt.imshow(img_data[:, :, middle_slice], cmap='gray')
            plt.axis('off')  # Turn off axis
            st.pyplot()  # Display the plot in Streamlit
            files = glob.glob(r'C:\\Users\\navee\\Downloads\\Aneurysm_Detection-main\\Aneurysm_Detection-main\\upload\*')
            for items in files:
                os.remove(items)

    

if __name__ == '__main__':
    main()
