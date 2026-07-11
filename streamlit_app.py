import os

import streamlit as st
import requests

st.set_page_config(page_title="California Housing Predictor", page_icon="🏠", layout="centered")

st.title("🏠 California Housing Price Predictor for you !!")
st.markdown("Enter the housing features below to get a regression prediction from the Flask API.")

API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/predict")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        med_inc = st.number_input("Median Income", value=3.5, step=0.1)
        house_age = st.number_input("House Age", value=20, step=1)
        ave_rooms = st.number_input("Average Rooms", value=5.0, step=0.1)
        ave_bedrms = st.number_input("Average Bedrooms", value=1.0, step=0.1)

    with col2:
        population = st.number_input("Population", value=1000, step=10)
        ave_occup = st.number_input("Average Occupancy", value=3.0, step=0.1)
        latitude = st.number_input("Latitude", value=37.8, step=0.1)
        longitude = st.number_input("Longitude", value=-122.2, step=0.1)

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "MedInc": med_inc,
        "HouseAge": house_age,
        "AveRooms": ave_rooms,
        "AveBedrms": ave_bedrms,
        "Population": population,
        "AveOccup": ave_occup,
        "Latitude": latitude,
        "Longitude": longitude,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            st.success("Prediction completed")
            st.metric("Predicted House Value", f"{result['prediction']:.4f}")
            st.json(result)
        else:
            st.error(f"Request failed: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to Flask API. Make sure it is running on http://127.0.0.1:5000")
        st.write(str(e))
