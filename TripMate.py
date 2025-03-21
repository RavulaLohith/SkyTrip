import os
import re
import requests
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
import urllib.parse  # To encode URLs
#from dotenv import load_dotenv  # Load environment variables

# Load environment variables from .env file
#load_dotenv()

# Retrieve API keys from environment variables
#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

GOOGLE_API_KEY="AIzaSyCtjlVOSnnjDNxGKvmH0FRIvvDXKUi1usA"
OPENWEATHER_API_KEY = "50d99d1168f3057a19c6c99069237e73"

# Initialize Gemini AI Model
model = GoogleGenerativeAI(model="gemini-1.5-pro")

# Function to fetch weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    else:
        return {"error": "City not found!"}

# Function to generate AI-based insights
@st.cache_data(ttl=3600)  # Cache responses for 1 hour
def generate_weather_report(city, category):
    try:
        weather_data = get_weather(city)
        
        if "error" in weather_data:
            return weather_data["error"]
        
        if category == "Weather Forecast":
            prompt = f"""Generate a detailed weather forecast for {city} based on:
            - Temperature: {weather_data['temperature']}°C
            - Weather: {weather_data['weather']}
            - Humidity: {weather_data['humidity']}%
            - Wind Speed: {weather_data['wind_speed']} km/h"""

        elif category == "Tourist Places":
            prompt = f"""List the Top 5 tourist places in {city}, providing their names and descriptions in a structured format:
            1. Place Name - Short Description."""

        elif category == "Recommendations":
            prompt = f"""Based on the current weather in {city}:
            - Temperature: {weather_data['temperature']}°C
            - Weather: {weather_data['weather']}
            - Humidity: {weather_data['humidity']}%
            - Wind Speed: {weather_data['wind_speed']} km/h
            
            Provide recommendations for:
            1. Clothing
            2. Hydration
            3. Outdoor activities
            4. Travel tips"""
        
        response = model.invoke(prompt)
        return response if response else "AI response unavailable. Please try later."
    
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="TripMate - Your AI Travel Guide", page_icon="🌍")

# Track user interaction with session state
if "submit_clicked" not in st.session_state:
    st.session_state.submit_clicked = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Weather Forecast"

# Sidebar for user input
city_name = st.sidebar.text_input("Enter City Name:", "")

# Store the category selection in session state
category = st.sidebar.radio("Select Category:", ["Weather Forecast", "Tourist Places", "Recommendations"],
                            index=["Weather Forecast", "Tourist Places", "Recommendations"].index(st.session_state.selected_category))

# Submit button logic
if st.sidebar.button("Get Insights"):
    if city_name.strip():  # Ensure city is entered before proceeding
        st.session_state.submit_clicked = True
        st.session_state.selected_category = category  # Store the selected category when submitting
    else:
        st.sidebar.warning("Please enter a city name before proceeding.")

# === HOME PAGE CONTENT (Visible Before Submission) ===
if not st.session_state.submit_clicked:
    st.title("🌍 Welcome to TripMate!")
    st.markdown(
        "#### Your AI-powered travel assistant to explore weather forecasts, tourist places, and travel recommendations. 🌟\n"
        "Enter a city and select a category from the sidebar, then hit **'Get Insights'** to begin!"
    )

# === DISPLAY RESULTS ONLY AFTER CLICKING "GET INSIGHTS" ===
if st.session_state.submit_clicked:
    st.subheader(f"📌 {st.session_state.selected_category} for {city_name}")

    weather_data = get_weather(city_name)
    ai_insight = generate_weather_report(city_name, st.session_state.selected_category)

    if "error" in weather_data:
        st.error(weather_data["error"])
    else:
        if st.session_state.selected_category == "Weather Forecast":
            st.write(f"🌡️ Temperature: {weather_data['temperature']}°C")
            st.write(f"🌥️ Condition: {weather_data['weather']}")
            st.write(f"💧 Humidity: {weather_data['humidity']}%")
            st.write(f"🌬️ Wind Speed: {weather_data['wind_speed']} km/h")
            st.subheader("🤖 AI-Based Weather Recommendations")
            st.write(ai_insight)

        elif st.session_state.selected_category == "Tourist Places":
            if not ai_insight or "Error" in ai_insight:
                st.warning("Could not fetch AI-generated tourist places. Try again later.")
            else:
                tourist_places = [
                    re.split(r"\d+\.\s*", line, maxsplit=1)[-1].strip()
                    for line in ai_insight.split("\n")
                    if re.match(r"^\d+\.\s*", line)
                ]
                if not tourist_places:
                    st.warning("AI did not return a valid list. Try again later.")
                else:
                    for place in tourist_places:
                        place_name, _, place_desc = place.partition(" -")
                        map_url = f"https://www.google.com/maps/dir/?api=1&destination={urllib.parse.quote(place_name + ', ' + city_name)}"

                        st.markdown(
                            f"""
                            <div style="display: flex; flex-direction: column; align-items: flex-start; margin-bottom: 10px;">
                                <span style="font-size: 18px; font-weight: bold;">🌍 {place_name}</span>
                                <span style="font-size: 16px;">📝 {place_desc}</span>
                                <div style="display: flex; justify-content: flex-end; width: 100%; margin-top: 5px;">
                                    <a href="{map_url}" target="_blank" style="text-decoration: none; font-weight: bold; color: #007BFF;">🗺️ Get Directions</a>
                                </div>
                            </div>
                            <hr style="border: 0.5px solid #ccc; width: 100%;">
                            """,
                            unsafe_allow_html=True,
                        )

        elif st.session_state.selected_category == "Recommendations":
            st.write(ai_insight)
