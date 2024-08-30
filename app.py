from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Nutritionix API credentials (replace with your actual API keys)
APP_ID = '838cd12c'
API_KEY = '87793ca39cbdb7c22b3a6d6e33687434'

# Function to fetch nutritional data from Nutritionix API
def fetch_nutritional_data(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "query": food_item,
        "timezone": "US/Eastern"
    }
    
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['foods']:
            return data['foods'][0]  # Return first food item found
    return None

# Function to determine health status and provide remedy message
def determine_health_status(calories):
    """
    Determines the health status of a food item based on its calorie content.

    Args:
    - calories (float): The calorie content of the food item.

    Returns:
    - tuple: (health_status, remedy_message)
    """
    if calories > 300:
        return "Unhealthy", "Consider reducing your intake of high-calorie foods. Opt for healthier options like fruits, vegetables, and lean proteins."
    elif calories > 200:
        return "Moderate", "Enjoy in moderation. Try to balance your diet with lower-calorie options and maintain portion control."
    else:
        return "Healthy", None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        food_item = request.form['food_item'].lower()
        nutrition = fetch_nutritional_data(food_item)
        if nutrition:
            calories = nutrition['nf_calories']
            health_status, remedy_message = determine_health_status(calories)
            return render_template('index.html', food_item=food_item, nutrition=nutrition, health_status=health_status, remedy_message=remedy_message)
        else:
            return render_template('index.html', error="Sorry, we couldn't find nutritional data for that food item.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
