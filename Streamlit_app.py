import streamlit as st
import pickle
import pandas as pd
import numpy as np
from PIL import Image
import time


model = pickle.load(open('Medicalcharge.1b','rb'))

df=pd.read_csv('insurance.csv')


st.set_page_config(page_title="Smart Predictions", page_icon="🤖", layout="wide")

def main_page():
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: center; color: #00308F;'>Medical Insurance Premium Cost Predictor!╰(*°▽°*)╯</h1>", unsafe_allow_html=True)

    sidebar_style = """
                  <style>
                 [data-testid="stSidebar"] h1 {
                        font-size: 40px; 
                        color: green;
                         }
                  </style>
                  """


    st.markdown(sidebar_style, unsafe_allow_html=True)
    img2 = Image.open("logowo.jpg")
    col1, col2 = st.columns([1, 2]) 

    with col1:
      st.sidebar.image(img2, width=200)  

    with col2:
      st.sidebar.markdown("<h1 style='text-align: left;color:blue;'>Smart Predictions</h1>", unsafe_allow_html=True)

    st.sidebar.divider()

    st.sidebar.title("Welcome!")
    st.sidebar.subheader(":blue[Our Health Insurance Cost Predictor is designed to provide you with an accurate estimate of your potential insurance costs.]")
    st.sidebar.subheader(":blue[Powered by advanced algorithms to ensure precision]")


    gender=df['sex'].unique()
    region_list=df['region'].unique()
    smoke=df['smoker'].unique()

    st.subheader(":green[Enter your details to get your premium cost:]")
    
    age=st.slider("Age:", min_value=0, max_value=100)

    sex=st.selectbox("Gender:",gender)

    region=st.selectbox("Region:",region_list)

    bmi = st.query_params.get("bmi", None)
    bmi_value = float(bmi) if bmi is not None else None
    bmi_input=st.number_input("BMI:",value=bmi_value,placeholder="Type a number...")
    if st.button("Don't know your bmi?"):
        st.query_params["page"]="second"
    

    children=st.number_input("How many children do you have:",value=None,placeholder="Type a number...")
                            
    smoker=st.selectbox("Do you smoke:",smoke)

    st.write('')
    if st.button("Get Cost"):
        inp1=int(age)
        inp2=float(bmi_input)
        inp3=int(children)
        inp4=int(np.where(gender==sex)[0][0])
        inp5=int(np.where(smoke==smoker)[0][0])
        inp6=int(np.where(region_list==region)[0][0])

        X=[inp5,inp1,inp3]
        charges=model.predict([X])
        f_charge = round(charges[0], 2)

        with st.spinner("Calculating..."):
            time.sleep(1)
            
        if charges is not None:
            #st.success("Calculation successful!")
            st.markdown(
                """<style>.custom-metric-label {
                font-size: 30px;
                font-weight: bold;
                color: #007FFF;
                }</style>""", unsafe_allow_html=True)
            st.markdown('<div class="custom-metric-label">Estimated Monthly Premium:</div>', unsafe_allow_html=True)

            st.metric(label="", value=f"${f_charge:.2f}")
    st.write("***")

    st.subheader(":blue[Your information is securely processed and not stored]")

def second_page():
    img1 = Image.open("body-mass-index.jpg")

    st.markdown("<h1 style='text-align: center; color: #0000FF;'>Know Your BMI!⚕️</h1>", unsafe_allow_html=True)   
    st.title("Enter your details to know your BMI.")
    

    sidebar_style = """
                  <style>
                 [data-testid="stSidebar"] h1 {
                        font-size: 65px; 
                        font-family: 'Luckiest Guy', cursive;
                        color: #5D3FD3;
                         }
                  </style>
                  """
    
    st.markdown(sidebar_style, unsafe_allow_html=True)
    

    st.sidebar.title("Fun Fact!😃")
    st.sidebar.write("🔍While Body Mass Index is commonly used to categorize individuals as underweight, normal weight, overweight, or obese, it doesn't actually measure body fat directly. \t Instead, it's a simple calculation using height and weight. This means a very muscular person might be classified as overweight or obese, even though they have low body fat!🔍")
    st.sidebar.image(img1, use_column_width=True)

    weight = st.number_input("Enter your weight in kilograms:", min_value=0.0, step=0.1,value=None,placeholder="Type a number...")
    height = st.number_input("Enter your height in centimeters:", min_value=0.0, step=0.01,value=None,placeholder="Type a number...")

    if st.button("Get BMI"):
        if height <= 0:
                print("Invalid height")
        
        elif weight <= 0:
            print("Invalid weight")
        
        else: 
            height=height/100
            calculated_bmi = weight / (height ** 2)

            st.query_params['bmi'] = calculated_bmi

            if calculated_bmi is not None:
                st.write(f"Your BMI is: {calculated_bmi:.2f}")

                st.query_params['page'] = 'main'
    
    if st.button("Go back to Main Page"):
        st.query_params["page"]="main"

    st.write('')
    st.write('')
    st.write('')

      
        


query_params = st.query_params

if "page" in query_params:
    page = query_params["page"]
    if page == "second":
        second_page()
    else:
        main_page()
else:
    main_page()
