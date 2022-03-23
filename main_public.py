import requests
from datetime import datetime
import os

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
TOKEN = os.environ.get("TOKEN")

GENDER = "male"
WEIGHT = 66.6
HEIGHT = 174.5
AGE = 30

natural_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"


headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0"
}

exercise_params = {
    "query": input("What exercise did you do today? "),
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=natural_exercise_endpoint, json=exercise_params, headers=headers)
data = response.json()

sheety_headers = {"Authorization": f"Bearer {TOKEN}"}

for exercise in data["exercises"]:
    date = datetime.today().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    new_row = {"workout": {
        "date": date,
        "time": time,
        "exercise": exercise["name"].title(),
        "duration": exercise["duration_min"],
        "calories": exercise["nf_calories"]
    }
    }
    exercise_response = requests.post(url=SHEET_ENDPOINT, json=new_row, headers=sheety_headers)
    exercise_response.raise_for_status()
    print(new_row)
