import os
import time
import schedule
import requests
from flask import Flask
from flask_restful import Resource, Api
from threading import Thread

app = Flask(__name__)
api = Api(app)

class Greeting(Resource):
    def get(self):
        return "𝗦𝗰𝗼𝗿𝗽𝗶𝗼 𝘄𝗼𝗿𝗸𝘀 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"

api.add_resource(Greeting, '/')

def visit_site():
    url = f"http://localhost:{os.environ.get('PORT', 5000)}"  # Change default port to 5000
    try:
        response = requests.get(url)
        print(f"Visited {url} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to visit {url} - Error: {e}")

# Schedule the task to run every 5 minutes
schedule.every(5).minutes.do(visit_site)

def run_flask_app():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))  # Ensure port is an integer

if __name__ == "__main__":
    # Run the Flask app in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
