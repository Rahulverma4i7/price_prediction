from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from bs4 import BeautifulSoup
import requests

def home_view(request):
    return HttpResponse("welcome to home")

def about_view(request):
    return HttpResponse("This is about")

def fetch_village_details(request):
    url = "https://www.yelp.com/biz/village-the-soul-of-india-hicksville"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract restaurant name
        name = soup.find('h1').text.strip()

        # Extract address
        address_section = soup.find('address')
        address = address_section.text.strip() if address_section else "Address not found"

        # Extract opening hours
        hours_section = soup.find_all('p', class_='css-1h1j0y3')
        hours = [hour.text.strip() for hour in hours_section] if hours_section else "Hours not available"

        # Extract menu items (fallback: mention manually if not on the page)
        menu = "Menu not available on website"

        details = {
            "name": name,
            "address": address,
            "hours": hours,
            "menu": menu
        }

        return JsonResponse(details)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def fetch_nearby_restaurants(request):
    # Hardcoded nearby restaurants
    nearby_restaurants = [
        {
            "name": "Saffron Indian Cuisine",
            "address": "123 Main St, Hicksville, NY",
            "rating": 4.5,
            "total_ratings": 120,
        },
        {
            "name": "Curry Club",
            "address": "456 Elm St, Hicksville, NY",
            "rating": 4.2,
            "total_ratings": 85,
        },
        {
            "name": "Bombay Delight",
            "address": "789 Oak Ave, Hicksville, NY",
            "rating": 4.0,
            "total_ratings": 150,
        },
        {
            "name": "Spicy Bites",
            "address": "101 Maple Dr, Hicksville, NY",
            "rating": 3.8,
            "total_ratings": 60,
        },
        {
            "name": "Royal Masala",
            "address": "202 Pine Ln, Hicksville, NY",
            "rating": 4.3,
            "total_ratings": 98,
        },
    ]

    return JsonResponse({"restaurants": nearby_restaurants})
def fetch_busy_times(request):
    # Hardcoded busy times for Village: The Soul of India
    busy_times = {
        "Monday": "Moderate (5:00 PM - 8:00 PM)",
        "Tuesday": "Busy (6:00 PM - 9:00 PM)",
        "Wednesday": "Quiet (12:00 PM - 3:00 PM)",
        "Thursday": "Moderate (5:00 PM - 8:00 PM)",
        "Friday": "Very Busy (6:00 PM - 10:00 PM)",
        "Saturday": "Very Busy (6:00 PM - 10:00 PM)",
        "Sunday": "Moderate (12:00 PM - 9:00 PM)",
    }

    return JsonResponse({"busy_times": busy_times})

def fetch_weather_data(request):
    WEATHER_API_KEY = "UZ79432DZFDZQK9ZTQ8Z9TDR4"  # Replace with your API key
    location = "mohali"  # Location name (can be a city name or latitude,longitude)

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"
    params = {
        "key": WEATHER_API_KEY,
        "unitGroup": "metric",  # Using metric system for Celsius
        "include": "days",  # Include daily weather data
        "contentType": "json",  # Specify JSON response format
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        # Check if the days data is available
        if "days" in data:
            weather_info = []
            for day in data["days"]:
                weather_info.append({
                    "date": day["datetime"],
                    "temperature": day["temp"],  # Temperature in Celsius
                    "weather": day["conditions"],  # Weather condition for the day
                })

            return JsonResponse({"weather": weather_info})

        else:
            return JsonResponse({"error": "Weather data for the specified location is unavailable."})

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)
def display_all_data(request):
    # Example hardcoded restaurant data (you can replace this with Yelp API data if available)
    village_restaurant = {
        "name": "Village - The Soul of India",
        "address": "123 Main Street, Village City",
        "open_times": "Mon-Sun: 11 AM - 10 PM",
        "menu_items": [
            {"item": "Paneer Tikka", "price": 12.5},
            {"item": "Butter Chicken", "price": 14.0},
            {"item": "Dal Makhani", "price": 10.0},
            {"item": "Naan", "price": 2.5}
        ]
    }

    # Fetch weather data (this part can be dynamic)
    WEATHER_API_KEY = "UZ79432DZFDZQK9ZTQ8Z9TDR4"
    location = "mohali"  # You can replace this with actual coordinates
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"
    params = {
        "key": WEATHER_API_KEY,
        "unitGroup": "metric",  # Celsius
        "include": "days",
        "contentType": "json"
    }
    
    weather_response = requests.get(weather_url, params=params)
    weather_data = weather_response.json()

    if "days" in weather_data:
        weather_info = weather_data["days"][0]  # Get today's weather info
        temperature = weather_info["temp"]
        weather_condition = weather_info["conditions"]
    else:
        temperature = "Data not available"
        weather_condition = "Data not available"

    # Hard-code whether the restaurant is busy (this can be dynamic if you have data)
    is_busy = True  # You can change this to dynamic data or make a prediction based on time of day, etc.

    # Call the price prediction function
    predicted_prices = predict_price(village_restaurant["menu_items"], temperature, weather_condition, is_busy)

    # Now send both restaurant and predicted prices to the template
    context = {
        'village_restaurant': village_restaurant,
        'temperature': temperature,
        'weather_condition': weather_condition,
        'predicted_prices': predicted_prices
    }

    return render(request, 'main/display.html', context)

def predict_price(menu_items, temperature, weather_condition, is_busy):
    """Predict prices based on weather and busyness."""
    adjusted_prices = []

    # Convert temperature from Celsius to Fahrenheit (if needed)
    if temperature < 45:
        price_increase_factor = 1.2  # Increase by 20% if temperature is cold
    elif "snow" in weather_condition.lower() or "rain" in weather_condition.lower():
        price_increase_factor = 1.3  # Increase by 30% if it's snowing or raining
    elif is_busy:
        price_increase_factor = 1.15  # Increase by 15% if the restaurant is busy
    else:
        price_increase_factor = 1.0  # No increase if none of the conditions are met

    # Adjust the prices based on the factors
    for item in menu_items:
        adjusted_price = item["price"] * price_increase_factor
        adjusted_prices.append({"item": item["item"], "price": round(adjusted_price, 2)})

    return adjusted_prices