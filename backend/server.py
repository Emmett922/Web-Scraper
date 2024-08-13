# Necessary imports
import asyncio
from flask import Flask, jsonify
from web_scraper_io_scraper import main as run_scraper
import os
from fasteners import InterProcessLock
from flask_cors import CORS

app = Flask(__name__) # Initialize Flask app
CORS(app) # Enable CORS to allow cross-origin requests

lock_file_path = "G:\\web-scrapers\\eCommerce-scraper\\backend\\scraper.lock" # Path to lock file
scraped_data = None # Global variable, stores scraped data


@app.route("/start-scraper", methods=["POST"])
def start_scraper():
    global scraped_data
    print("Received request to start scraper.")
    if os.path.exists(lock_file_path): # Check if scraper is already running
        print("Scraper is already running.")
        return jsonify({"message": "Scraper is already running."}), 400
    else:
        print("Starting scraper...")
        open(lock_file_path, 'w').close() # Create lock file
        try:
            scraped_data = asyncio.run(run_scraper()) # Run the scraper asynchonously
            print("Scraped Data:", scraped_data)
        except Exception as e:
            print(f"Error occured while running scraper: {e}")
            return jsonify({"message": "Failed to start scraper."}), 500
        finally:
            if os.path.exists(lock_file_path):
                os.remove(lock_file_path) # Remove lock file when done
            print("Scraper started successfully.")
        return jsonify({"message": "Scraper started."}), 200
    


@app.route("/status")
def status():
    if os.path.exists(lock_file_path): # Check if scraper is running
        print("Scraper is running")
        return jsonify({"status": "running"})
    else:
        print("Scraper is idle")
        return jsonify({"status": "idle"})

@app.route("/laptops")
def laptops():
    global scraped_data
    if os.path.exists(lock_file_path): # Check if data is still being processed
        if scraped_data is None:
            return jsonify({"message": "Data is being processed."}), 202
        return jsonify({"data": scraped_data}) # Return scraped data if available
    else:
        if scraped_data:
            return jsonify({"data": scraped_data}) # Return scraped data if scraping is finished
        return jsonify({"message": "Scraper not started or already finished."}), 400

if __name__ == "__main__":
    app.run(debug=False) # Run app
