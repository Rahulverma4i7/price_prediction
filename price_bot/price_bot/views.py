from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
from datetime import datetime




YELP_API_KEY = "u26uX88dUyTZqojeN_fYAg0qiLllipVT8xfiqw3UAJIeP9N4D1M87I7gCa3HwxVzwikXu-x5dijlf3kl4CoAZiXrynxzOdQpch-saAO9T_CwUneujoAcCVuC3N9bZ3Yx"

def fetch_village_details(request):
    url = "https://www.yelp.com/biz/village-the-soul-of-india-hicksville"

    try:
        headers = {
            "Authorization": f"Bearer {YELP_API_KEY}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        name_tag = soup.find('h1')
        name = name_tag.text.strip() if name_tag else "Name not found"

        address_section = soup.find('address')
        address = address_section.text.strip() if address_section else "Address not found"

        hours_section = soup.find_all('p', class_='css-1h1j0y3')  
        hours = [hour.text.strip() for hour in hours_section] if hours_section else "Hours not available"

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
    
def fetch_nearby_restaurants(latitude, longitude, radius=2000, term="restaurants"):
    """
    Fetch details of nearby restaurants using Yelp API.
    """
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {
        "term": term,
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "categories": "restaurants",  
        "limit": 5, 
        "sort_by": "rating"  
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        restaurants = []
        for business in data.get("businesses", []):
            location = business.get("location", {})
            restaurants.append({
                "name": business.get("name"),
                "rating": business.get("rating"),
                "address": ", ".join(location.get("display_address", [])),
                "phone": business.get("display_phone", "Phone not available"),
                "price": business.get("price", "Price not available")  
            })

        return restaurants

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


latitude = 19.203209283048952
longitude = 72.85996900294673
restaurants = fetch_nearby_restaurants(latitude, longitude)
print(restaurants)

def fetch_restaurant_details(business_id):
    """
    Fetch detailed information about a specific restaurant.
    """
    url = f"https://api.yelp.com/v3/businesses/{business_id}"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

       
        hours = []
        if "hours" in data:
            for hour in data["hours"]:
                hours.append(hour.get("open", [])) 

        details = {
            "name": data.get("name", "Name not available"),
            "address": ", ".join(data.get("location", {}).get("display_address", [])),
            "rating": data.get("rating", "Rating not available"),
            "reviews": data.get("review_count", "Review count not available"),
            "hours": hours or "Hours not available"
        }

        return details

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Business not found. Check the business ID."}
        return {"error": f"HTTP error: {str(e)}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}


business_id = "village-the-soul-of-india-hicksville" 
details = fetch_restaurant_details(business_id)
print(details)


def fetch_busy_times(request):
  
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
    WEATHER_API_KEY = "UZ79432DZFDZQK9ZTQ8Z9TDR4"  
    location = "Growel 101, 2nd Floor, Akurli Rd, Kandivali East, Mumbai, Maharashtra 400101" 
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"
    params = {
        "key": WEATHER_API_KEY,
        "unitGroup": "metric",  
        "include": "days",  
        "contentType": "json",  
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if "days" in data:
            weather_info = []
            for day in data["days"]:
                weather_info.append({
                    "date": day["datetime"],
                    "temperature": day["temp"], 
                    "weather": day["conditions"],  
                })

            return JsonResponse({"weather": weather_info})

        else:
            return JsonResponse({"error": "Weather data for the specified location is unavailable."})

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def fetch_weather(location):
    """
    Fetch weather data for a given location using the Visual Crossing Weather API.
    """
    WEATHER_API_KEY = "UZ79432DZFDZQK9ZTQ8Z9TDR4"
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"
    params = {
        "key": WEATHER_API_KEY,
        "unitGroup": "metric", 
        "include": "days",
        "contentType": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

      
        if "days" in data:
            today_weather = data["days"][0]
            return {
                "temperature": today_weather["temp"],
                "weather_condition": today_weather["conditions"]
            }
        else:
            return {
                "temperature": "Data not available",
                "weather_condition": "Data not available"
            }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    

def is_restaurant_busy():
    """
    Determine if the restaurant is busy based on the time of day.
    You can replace this with more sophisticated logic or data.
    """
    current_hour = datetime.now().hour

    
    if 18 <= current_hour <= 21:
        return True
    return False

    
def display_all_data(request):
    """
    Display all data including restaurant details, nearby restaurants,
    weather information, and predicted menu prices.
    """
    try:
        
        latitude, longitude = 19.203209283048952, 72.85996900294673

       
        village_details = fetch_restaurant_details("village-the-soul-of-india-hicksville")
        if not village_details or "error" in village_details:
            village_details = {"name": "Village Restaurant", "menu_items": []}

       
        nearby_restaurants = fetch_nearby_restaurants(latitude, longitude)
        if not nearby_restaurants:
            nearby_restaurants = []

        
        weather_data = fetch_weather("Growel 101, 2nd Floor, Akurli Rd, Kandivali East, Mumbai, Maharashtra 400101")
        temperature = weather_data.get("temperature", 75)  
        weather_condition = weather_data.get("weather_condition", "Clear")

       
        is_busy = is_restaurant_busy()

        
        menu_items = village_details.get("menu_items", [])
        predicted_prices = predict_price(menu_items, temperature, weather_condition, is_busy)

        
        context = {
            "village_restaurant": village_details,
            "nearby_restaurants": nearby_restaurants,
            "temperature": temperature,
            "weather_condition": weather_condition,
            "predicted_prices": predicted_prices,
        }

        return render(request, "main/display.html", context)

    except Exception as e:
        
        return render(request, "main/error.html", {"error": str(e)})


def predict_price(menu_items, temperature, weather_condition, is_busy):
    """Predict prices based on weather and busyness."""
    adjusted_prices = []

    
    try:
        if temperature < 45: 
            price_increase_factor = 1.2 
        elif "snow" in weather_condition.lower() or "rain" in weather_condition.lower():
            price_increase_factor = 1.3 
        elif is_busy:
            price_increase_factor = 1.15  
        else:
            price_increase_factor = 1.0  
       
        for item in menu_items:
            price = item.get("price", 0)
            adjusted_price = price * price_increase_factor
            adjusted_prices.append({"item": item.get("item", "Unknown"), "price": round(adjusted_price, 2)})

    except Exception as e:
       
        adjusted_prices = [{"item": "Error calculating price", "price": 0}]

    return adjusted_prices