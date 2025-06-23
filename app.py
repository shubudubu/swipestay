from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import csv
import os

app = Flask(__name__)

# CSV file to store emails
EMAIL_FILE = "emails.csv"

# Ensure the file exists with headers
if not os.path.exists(EMAIL_FILE):
    with open(EMAIL_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Email", "Timestamp"])


@app.route("/")
def index():
    with open("templates/index.html") as f:
        return f.read()


@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")

    if not email:
        return jsonify({"message": "Invalid email"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(EMAIL_FILE, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([email, timestamp])
        return jsonify({"message": f"We'll notify you at {email}!"})
    except Exception as e:
        return jsonify({"message": "Server error: " + str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
