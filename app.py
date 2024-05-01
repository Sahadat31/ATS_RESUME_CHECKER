from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai


# configure the genai with api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to specify gemini response
def get_gemini_response(input_prompt,pdf_content,input_text):
    # which model to use
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,pdf_content[0],input_text])
    return response.text



# function to convert pdf into image
def pdf_to_image(pdf_file):
    if pdf_file:
        # convert into image
        # to use pdf2image you need to use poppler too
        images = pdf2image.convert_from_bytes(pdf_file.read())

        first_page = images[0]

        # convert to bytes
        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr,format='JPEG')
        image_byte_arr=image_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("NO FILE UPLOADED")


# streamlit app
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Resume Checker")
job_description = st.text_area("Job Description..",key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)..",type=["pdf"])

if uploaded_file:
    st.write("File uploaded successfully..")

btn1 = st.button("Tell me about your resume")
btn2 = st.button("Percentage Match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


if btn1:
    if uploaded_file:
        pdf_content = pdf_to_image(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,job_description)
        st.subheader("Resume summary:")
        st.write(response)
    else:
        st.write("resume not uploaded")
elif btn2:
    if uploaded_file:
        pdf_content = pdf_to_image(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content,job_description)
        st.subheader("Percentage match and missing skills:")
        st.write(response)
    else:
        st.write("resume not uploaded")



    

