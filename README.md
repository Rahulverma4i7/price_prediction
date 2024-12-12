# Restaurant Price Prediction

This project predicts the price of restaurant menu items based on various factors such as weather conditions, busy hours, and location. The updated prices are determined dynamically using Django.

## Features

- **Dynamic Price Prediction**

  - Predicts restaurant prices based on real-time weather and business conditions.

- **APIs Used**

  - **Google Maps API**: Fetches busy hours and location details.
  - **OpenWeather API**: Retrieves current weather conditions to factor into price prediction.

- **Technology Stack**
  - **Backend**: Django framework for robust and scalable server-side logic.
  - **APIs Integration**: Seamlessly connects weather and location data to predict prices.

## How It Works

1. **Fetch Data**

   - Use the Google Maps API to determine busy hours and restaurant locations.
   - Retrieve weather data (temperature, rain, snow) using the OpenWeather API.

2. **Process Data**

   - Analyze the data to determine conditions that affect pricing:
     - High busy hours
     - Severe weather (e.g., rain, snow, low temperature)

3. **Predict Price**

   - Use predefined conditions and an ML algorithm to dynamically predict restaurant menu prices.

4. **Update Prices**
   - Display the predicted prices on the website, reflecting real-time adjustments.

## Outcome

- Real-time updates to restaurant pricing based on external factors.
- Increased relevance and adaptability of menu pricing for customers.
