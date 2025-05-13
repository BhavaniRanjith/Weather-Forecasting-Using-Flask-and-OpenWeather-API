from flask import Flask, render_template, request
from datetime import datetime
import csv
import requests
import os
import platform

# Set file permissions for non-Windows systems
if platform.system() != 'Windows':
    os.chmod('weather_data.csv', 0o660)

print("Script running....")

app = Flask(__name__)

weather_images = {
    "Clear": "https://cdn-icons-png.flaticon.com/512/869/869869.png",
    "Clouds": "https://cdn-icons-png.flaticon.com/512/414/414825.png",
    "Rain": "https://cdn-icons-png.flaticon.com/512/1163/1163624.png",
    "Snow": "https://cdn-icons-png.flaticon.com/512/642/642102.png",
    "Drizzle": "https://cdn-icons-png.flaticon.com/512/4005/4005901.png",
    "Thunderstorm": "https://cdn-icons-png.flaticon.com/512/1146/1146860.png",
    "Mist": "https://cdn-icons-png.flaticon.com/512/4005/4005817.png",
    "Haze": "https://cdn-icons-png.flaticon.com/512/1197/1197102.png",
    "Fog": "https://cdn-icons-png.flaticon.com/512/1779/1779940.png"
}

# OpenWeatherMap API key
API_KEY = "Your API key"

# Main route for the app
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        # Get the city from the form input
        city = request.form["city"]
        
        # API URL to fetch weather data
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        # Make the API request
        response = requests.get(url)
        print(response.json())

        if response.status_code == 200:
            # Extract weather data from the response
            data = response.json()
            condition = data["weather"][0]["main"]
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            
            weather_data = {
                'city': city,
                'temperature': temperature,
                'description': description,
                'image_url': weather_images.get(condition, "data:image/png;base64,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")
                # You can add an image URL based on weather condition
            }

            # Extract desired fields for the CSV record
            weather_row = {
                'City': data['name'],
                'Temperature (°C)': data['main']['temp'],
                'Feels Like (°C)': data['main']['feels_like'],
                'Humidity (%)': data['main']['humidity'],
                'Weather': data['weather'][0]['description'],
                'Wind Speed (m/s)': data['wind']['speed'],
                'Country': data['sys']['country'],
                'Date/Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Define the CSV file name
            csv_filename = 'weather_data.csv'

            # Write header only if file doesn't exist or is empty
            try:
                with open(csv_filename, 'r', encoding='utf-8', errors='ignore') as f:
                    file_empty = f.read().strip() == ''
            except FileNotFoundError:
                file_empty = True

            # Append the row to the CSV file
            with open(csv_filename, mode='a', newline='', encoding='utf-8',errors='ignore') as file:
                writer = csv.DictWriter(file, fieldnames=weather_row.keys())
                if file_empty:
                    writer.writeheader()
                writer.writerow(weather_row)

            # Open the CSV file and handle possible UnicodeDecodeError
            try:
                with open(csv_filename, encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row)
            except UnicodeDecodeError as e:
                print(f"Error reading CSV file: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif response.status_code == 401:
            weather_data = {"error": "Invalid API key. Please check your key."}
        else:
            weather_data = {"error": "City not found!"}

    return render_template("index.html", weather=weather_data)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
