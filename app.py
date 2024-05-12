from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app


st.set_page_config(page_title="uHEALTHY")

st.header("uHEALTHY")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Help me")

input_prompt="""
        you are Tejas an expert gym trainer and expert dietician,
        give body fat percentage from image
        tell about what fitness goal should be followed from image
        tell full workout plan according to fitness goal
        focus more on diet plan give more appropriate diet plan as per fitness goal and fat percentage
        tell full detailed diet plan as per indian diet 
        focus more on telling gym workout plan and diet plan, include mixture of cardio and 
        weight training in the workout plan, tell workout plan based on the fitness goal identified by
        you
"""

## If submit button is clicked
## tell gender,  tell body fat percentage,tell fitness goal from what should the person follow arrange it properly, tell everything properly like expert gym trainer and guide and 
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

