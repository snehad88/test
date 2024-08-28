from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Replace these with your actual Nutritionix API credentials
API_KEY = '87793ca39cbdb7c22b3a6d6e33687434'
APP_ID = '838cd12c'

def get_nutrition_data(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "query": food_item,
        "timezone": "US/Eastern"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            food_item = request.form['food_item']
            nutrition_data = get_nutrition_data(food_item)
            
            if nutrition_data and 'foods' in nutrition_data:
                return render_template('index.html', nutrition=nutrition_data['foods'])
            else:
                return render_template('index.html', error="Could not retrieve data.")
        
        return render_template('index.html')
    except Exception as e:
        # Log the exception
        app.logger.error(f"Error: {e}")
        # Return a generic error message to the user
        return render_template('index.html', error="An unexpected error occurred.")



if __name__ == '__main__':
    app.run(debug=True)
