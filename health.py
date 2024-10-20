import time
import requests

url = "https://vyan-py.onrender.com/"  # Replace with your target URL

while True:
    try:
        response = requests.get(url)
        print(f"Request sent to {url}. Response Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    time.sleep(300)  # Sleep for 5 minutes (300 seconds)
