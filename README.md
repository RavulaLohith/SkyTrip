Here's an improved and more **detailed README** for your **SkyTrip – AI Travel Assistant** project, explaining **how it works step-by-step** and highlighting the key technologies and logic involved:

---

# 🌍 SkyTrip – Your AI Travel Assistant

SkyTrip is a smart and interactive AI-based travel assistant built with **Streamlit** and powered by **Google Gemini Pro** (via **LangChain**). It provides **real-time weather updates**, **top tourist attractions**, and **personalized travel recommendations**—all tailored to the selected destination’s current conditions.

> ✨ Whether you're planning a trip or just exploring virtually, SkyTrip helps you prepare better and discover more.

---

## 🚀 Features at a Glance

* **🔎 Live Weather Forecast**
  View real-time temperature, weather condition, humidity, and wind speed using **OpenWeather API**.

* **🗺️ Top Tourist Attractions**
  Get AI-curated top 5 must-visit places in any city, along with short descriptions and Google Maps directions.

* **💡 Travel Recommendations**
  Receive AI-generated tips on clothing, hydration, outdoor activities, and travel preparation based on weather.

* **📍 Google Maps Integration**
  Direct links to tourist locations via Google Maps for easy navigation.

* **🖥️ Modern UI with Streamlit**
  Clean, responsive UI with a sidebar for input and dynamic display based on user interactions.

---

## 🧠 How It Works (Architecture & Flow)

### 1. **User Input via Sidebar**

Users input a city name and select one of the three categories:

* **Weather Forecast**
* **Tourist Places**
* **Recommendations**

### 2. **Weather Data Retrieval**

A call is made to the **OpenWeatherMap API**:

```python
http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric
```

It returns structured weather details like:

* Temperature (°C)
* Weather condition (e.g., cloudy, sunny)
* Humidity (%)
* Wind Speed (km/h)

### 3. **Prompt Generation Based on Category**

Depending on the selected category, SkyTrip dynamically builds a prompt using weather data:

* **Weather Forecast**

  > "Generate a detailed weather forecast for {city}..."

* **Tourist Places**

  > "List the Top 5 tourist places in {city} with descriptions..."

* **Recommendations**

  > "Based on weather, recommend clothing, hydration tips, and activities..."

### 4. **AI Response via Gemini Pro (LangChain)**

The prompt is passed to **Google Gemini Pro** using **LangChain**, which processes the input and returns natural-language suggestions or lists.

### 5. **Dynamic UI Rendering**

SkyTrip dynamically shows:

* Weather cards for forecast
* Bullet-point lists with Maps links for tourist spots
* Personalized travel tips under Recommendations

### 6. **Caching for Speed**

To optimize API usage and improve performance, responses are cached using:

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
```

---

## 🧩 Tech Stack

| Component        | Technology Used                 |
| ---------------- | ------------------------------- |
| Frontend         | Streamlit                       |
| Weather API      | OpenWeatherMap API              |
| AI Model         | Google Gemini Pro via LangChain |
| Maps Integration | Google Maps URL encoding        |
| Caching          | `@st.cache_data`                |
| Language         | Python                          |

---

## 🛠 Setup & Installation

1. **Clone the Repo**

   ```bash
   git clone https://github.com/your-username/skytrip.git
   cd skytrip
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set API Keys**
   Replace the placeholder values with your actual keys in the script:

   ```python
   GOOGLE_API_KEY = "your_gemini_api_key"
   OPENWEATHER_API_KEY = "your_openweather_api_key"
   ```

4. **Run the App**

   ```bash
   streamlit run app.py
   ```

---



