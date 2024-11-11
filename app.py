from flask import Flask, render_template, request
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename
#from model import process_image_model  # Import the function from model.py

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to load treatments from a JSON file
def load_treatments():
    with open("treatments.json", "r") as file:
        return json.load(file)


# Function to get treatment info from the JSON data
def get_treatment(disease, days):
    treatments = load_treatments()
    for treatment in treatments["diseases"]:
        if (
            treatment["disease"].lower() == disease.lower()
            and treatment["min_days"] <= int(days) <= treatment["max_days"]
        ):
            return treatment["treatment"]
    return None


# Function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    age = request.form["age"]
    disease = request.form["disease"]
    days = request.form["days"]

    treatment = get_treatment(disease, days)

    if treatment:
        return render_template(
            "result.html", name=name, age=age, disease=disease, treatment=treatment
        )
    else:
        return render_template(
            "result.html",
            name=name,
            age=age,
            disease=disease,
            treatment="No treatment found for this disease.",
        )

'''
@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return "No file part", 400
    file = request.files["image"]

    if file.filename == "":
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Process the image using the function from model.py
        result = process_image_model(filepath)

        return render_template(
            "result.html",
            name=request.form["name"],
            age=request.form["age"],
            disease=result,
            treatment="Model detected disease: " + result,
        )

    return "File type not allowed", 400'''


if __name__ == "__main__":
    app.run(debug=True)
