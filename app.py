import pandas as pd
import streamlit as st
import pickle
import numpy as np
# import tkinter as tk
# import tkinter.messagebox as tkmb


data = pd.read_csv('cleaned_data.csv')
pipe = pickle.load(open('LinearModel.pkl', 'rb'))

def predict_price(sqft, bath, balcony, location, bhk):
    input_data = pd.DataFrame([[sqft, bath, balcony, location, bhk]], columns=['total_sqft', 'bath', 'balcony', 'site_location', 'bhk'])
    prediction = pipe.predict(input_data)[0] * 1e5
    return np.round(prediction, 2)


st.title("Hyderabad House Price Predictor")

# Get unique locations from the data
locations = sorted(data['site_location'].unique())

# Input components
location = st.selectbox("Select Location", locations)
bhk = st.text_input("Enter BHK", "")
sqft = st.text_input("Enter total house area in sqft", "")
bath = st.text_input("Enter number of bathroom(s)", "")
balcony = st.text_input("Enter number of balcony(ies)", "")


# Predict button
if st.checkbox("Predict Price"):
    if location and bhk and sqft and bath and balcony:
        prediction = predict_price(float(sqft), int(bath), int(balcony), location, int(bhk))
        st.write(f"Prediction: ₹{prediction}")

        pred = prediction
        st.title("Calculate EMI on Above Amount")
        R = (st.number_input("Enter Your Interest Rate"))
        t = (st.number_input("Enter Your Tennure in Months"))
        if st.button("Calculate EMI"):
            if R and t:
                r = R/(12*100)
                emi = pred * r * ((1+r)**t)/((1+r)**t - 1)
                # emi = pipe[pred * r * ((1+r)**t)/((1+r)**t - 1)] * 1e5
                interest = (emi*t)-pred
                emi = round(emi , 2)
                interest = round(interest , 3)
                st.write(f"EMI :  ₹{emi} Per Month" )
                st.write(f"Interest :  ₹{interest}" )
                
    

else:
    st.warning("Please fill in all the input fields.")

