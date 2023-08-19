from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_BASE_URL = "http://20.244.56.144/train"
CLIENT_ID = "b46118f0-fbde-4b16-a4b1-6ae6ad718b27"
CLIENT_SECRET = "XOyol0RPasKWODAN"

def get_authorization_token():
    auth_data = {
        "companyName": "Train Central",
        "clientID": CLIENT_ID,
        "ownerName": "Rahul",
        "ownerEmail": "rahul@abc.edu",
        "rollNo": "1",
        "clientSecret": CLIENT_SECRET
    }
    response = requests.post(f"{API_BASE_URL}/auth", json=auth_data)
    token_data = response.json()
    return token_data["access_token"]

def get_train_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{API_BASE_URL}/trains", headers=headers)
    train_data = response.json()
    return train_data

def process_train_data(train_data):
    # Process and filter train data as per your requirements
    # Implement the sorting and filtering logic here
    return train_data

@app.route("/trains", methods=["GET"])
def get_next_12_hour_trains():
    try:
        access_token = get_authorization_token()
        train_data = get_train_data(access_token)
        processed_trains = process_train_data(train_data)
        return jsonify(processed_trains), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/trains/<train_number>", methods=["GET"])
def get_train_details(train_number):
    try:
        access_token = get_authorization_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_BASE_URL}/trains/{train_number}", headers=headers)
        train_details = response.json()
        return jsonify(train_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
