from tkinter import OptionMenu
import streamlit as st
import os
from zipfile import ZipFile
import zipfile
import cv2
import numpy as np
import requests
import hydralit as hy
import hydralit_components as hc
import time
import io
import matplotlib.pyplot as plt
import shutil
import base64
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from PIL import Image


app = hy.HydraApp(title='Img Detector',favicon="camera",hide_streamlit_markers=True,use_navbar=True, navbar_sticky=True)

def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

@app.addapp(is_home = True)
def Image_Detector():
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href
    def get_prediction(session , uploaded_file):
        response = session.post("http://127.0.0.1:8000/predict",
                        files = {'image': open(uploaded_file,'rb') } )
        return response.json()
    def extract_zip(input_zip):
        input_zip=ZipFile(input_zip)
        return {name: input_zip.read(name) for name in input_zip.namelist()}
    def save_uploadedfile(uploadedfile):
        with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())
        return st.success(f"Saved File:{uploadedfile.name} to tempDir")
    _left2, mid2= st.columns([1,2])
    with _left2:
        st.subheader("Image Detector")
        image_types = ['jpg','png','jpeg']
        # image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
        zip_file = st.file_uploader("Upload Zip", type=["zip"])
        X_pred = None
        prediction=None
        shutil.rmtree('images' , ignore_errors = True)
        shutil.rmtree('images.zip' , ignore_errors = True)
        os.system('rm images.zip')
        os.system('ls')
        if not os.path.isdir('images'):
            os.mkdir('images')
        if zip_file is not None:
            #all_imgs = []
            predictions = []
            #content_to_get = []
            with zipfile.ZipFile(zip_file) as z:
                #Select only images
                with requests.Session() as session:
                    for file in z.namelist():
                        if file.split('.')[-1] in image_types:
                            #Extract image locally
                            try:
                                extracted_file = z.extract(file)
                                prediction = get_prediction(session , extracted_file).get('prediction')
                                predictions.append(prediction)
                                #st.write(prediction)
                                if not os.path.isdir(f"images/{prediction}"):
                                    os.mkdir(f"images/{prediction}")
                                print(f'moving file {file}')
                                os.system(f'mv {file} images/{prediction}')
                                #plt.savefig(prediction , f"images/{prediction}")
                                #st.write(extracted_file.split('/')[-1])
                                #img = cv2.imread(extracted_file)
                                #img = cv2.resize(img,(32,32))
                                #all_imgs.append(img)
                            #Maybe here is a good moment to predict (#Predict the images) connect to api end point
                            #1) load the image variable
                            #2) Do the prediction
                            #3) Save the prediction
                            #4) Create a new file name
                            #5) Append the new file to a list
                                print("Extracted and moved file")
                                print(f'prediction: {prediction}')
                            except Exception as e:
                                print("Invalid file ", str(e))
            final_output = {}
            for i , prediction in enumerate(predictions):
                file = z.namelist()[i]
                final_output[file] = prediction
            st.markdown(final_output)
            shutil.make_archive('images', 'zip', 'images')
            st.markdown(get_binary_file_downloader_html('images.zip') , unsafe_allow_html=True)
    with mid2:
        lottie_url_0 = "https://assets10.lottiefiles.com/packages/lf20_wEt2nn.json"
        lottie_hello0 = load_lottieurl(lottie_url_0)
        st_lottie(lottie_hello0, key="b" , width = 450 , height = 450)

@app.addapp()
def About():
    _left, mid = st.columns([1,2])
    with _left:
        st.title("Image Detector Project")
        st.markdown("Our Team")
        st.markdown('''<img src='https://img.icons8.com/office/2x/linkedin-circled--v2.png%202x' alt='Linkedin' width="50" height="50"> <a href='https://www.linkedin.com/in/maria-borrell-rodr%C3%ADguez-616ba94a/'> Maria Borrell </a>''' , unsafe_allow_html = True)
        st.markdown('''<img src='https://img.icons8.com/office/2x/linkedin-circled--v2.png%202x' alt='Linkedin' width="50" height="50"> <a href='https://www.linkedin.com/in/fabrizio-capeccia/'> Fabrizio Capeccia </a>''' , unsafe_allow_html = True)
        st.markdown('''<img src='https://img.icons8.com/office/2x/linkedin-circled--v2.png%202x' alt='Linkedin' width="50" height="50"> <a href='https://www.linkedin.com/in/paolo-debiase/'> Paolo De Biase </a>''' , unsafe_allow_html = True)
    lottie_url_people = "https://assets1.lottiefiles.com/packages/lf20_qywhav7l.json"
    lottie_hello1 = load_lottieurl(lottie_url_people)
    lottie_url_image = "https://assets4.lottiefiles.com/packages/lf20_exi9acin.json"
    lottie_hello2 = load_lottieurl(lottie_url_image)
    lottie_url_ai = "https://assets7.lottiefiles.com/private_files/lf30_m075yjya.json"
    lottie_hello3 = load_lottieurl(lottie_url_ai)
    with mid:
        st_lottie(lottie_hello1, key="a" , width = 550 , height = 550)
    _left2, mid2= st.columns([1,2])
    with mid2:
        st_lottie(lottie_hello2, key="b" , width = 550 , height = 550)
    with _left2:
        for _ in range(15):
            st.markdown(" ")
        st.markdown("This work is part of a 2 weeks Project which aims at conceiving a WebApp capable to recognize unlabelled images from a zip file and create a new one containing these images renamed according to what they represent")
    _left3, mid3= st.columns([1,2])
    with mid3:
        st_lottie(lottie_hello3, key="c" , width = 550 , height = 550)
    with _left3:
        for _ in range(15):
            st.markdown(" ")
        st.markdown("This Image Detector is using AI based on CNN exploiting the ResNet-50 model.")
        #X_pred = np.stack(all_imgs , axis = 0)
        #Create the final zip file
        #Make a botton available that the user can download the zip file back
        #Summary for the prediction in each file and pass what is the probability that our model is outputing
    #User can download the finalzip
    # st.download_button(
    #         label="Download ZIP",
    #         data=zip_file,
    #         file_name="myfile.zip",
    #         mime="application/zip"
    #     )
    # with open("myfile.zip", "rb") as fp:
    #     btn = st.download_button(
    #         label="Download ZIP",
    #         data=fp,
    #         file_name="myfile.zip",
    #         mime="application/zip"
    #     )
with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[3,0,5]):
    time.sleep(1)
app.run()
