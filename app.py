from flask import Flask, request, jsonify, render_template_string, send_file, abort
import csv
import os

app = Flask(__name__)

ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "changeme123")  # Read from env, fallback for local

@app.route("/")
def home():
    return render_template_string(open("templates/index.html").read())

@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    if not email:
        return jsonify({"message": "Email is required."}), 400

    file_exists = os.path.exists("emails.csv")
    with open("emails.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Email"])
        writer.writerow([email])

    return jsonify({"message": f"We'll notify you at {email}."})

@app.route("/download")
def download_csv():
    key = request.args.get("key")
    if key != ADMIN_SECRET:
        abort(403)  # Forbidden

    if not os.path.exists("emails.csv"):
        abort(404)

    return send_file("emails.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
