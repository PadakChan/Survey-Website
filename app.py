from flask import Flask, render_template, request, jsonify, session, redirect, url_for
#  render_template: to render HTML templates
#  request: to handle incoming data from the frontend
#  jsonify: to send JSON responses back to the frontend
#  session: to keep track of which survey the user is currently taking
#  redirect and url_for: to navigate between different pages of the survey

import random 
# for shuffling the order of the surveys.
import csv
# for saving the survey data into CSV Files
import os

from datetime import datetime

app = Flask(__name__)
app.secret_key = "emotion_survey_secret_key" 
# This secret key is necessary for using Flask's session to keep track of the user's progress through the surveys.


#  SURVEY LIST
# Shifting from JAVA script to python, I had to change the way I store the survey pages.
# Instead of storing them in a JavaScript array, I am now storing them in a Python list. 
# This allows me to easily shuffle the order of the surveys and keep track of which survey the user is currently taking using Flask's session.
SURVEYS = [
    "survey_1.html",
    "survey_2.html",
    "survey_3.html",
    "survey_4.html",
    "survey_5.html",
    "survey_6.html"
]


#CREATE CSV FILE IF IT DOES NOT EXIST 
if not os.path.exists("data.csv"):
    with open("data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp",
            "survey",
            "text",
            "happy",
            "sad",
            "fear",
            "anger"
        ])


# HOME PAGE
@app.route('/')
def home():
    return render_template("index.html")


#  ABOUT PAGE
@app.route('/about')
def about():
    return render_template("about.html")


# INTRO PAGE 
@app.route('/intro')
def intro():
    return render_template("intro.html")


#  START SURVEY
@app.route('/start')
def start():
    surveys = SURVEYS.copy()
    random.shuffle(surveys)
    # shuffle the order of the surveys to ensure that each user takes the surveys in a different order, 
    # which can help reduce bias in the results.
    session["surveys"] = surveys

    return redirect(url_for("intro"))


#  NEXT SURVEY 
@app.route('/next')
def next_survey():
    if "surveys" not in session or len(session["surveys"]) == 0:
        return redirect(url_for("thankyou"))
# if there are no more surveys left in the session, redirect to the thank you page
    next_page = session["surveys"].pop()
    session["surveys"] = session["surveys"]

    # remember which survey page user is answering
    session["current_survey"] = next_page

    return render_template(next_page)

# SAVE DATA 
# POST request is used to send data from the frontend to the backend. 
@app.route('/submit', methods=['POST']) 

def submit():
    # data = request.json is used to get the data sent from the frontend in JSON format.
    data = request.json

    text = data.get("text") 
    # get the text input from the frontend
    happy = data.get("happy")
    sad = data.get("sad")
    fear = data.get("fear")
    anger = data.get("anger")

    # get current survey from Flask session
    survey = session.get("current_survey", "unknown_survey.html")

    # survey_1.html -> survey_1
    survey_name = survey.replace(".html", "")

    # save into survey_1.csv, survey_2.csv, etc.
    filename = f"{survey_name}.csv"
    
    file_exists = os.path.exists(filename) 
    # check if the file exists

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp", "text", "happy", "sad", "fear", "anger"])

        writer.writerow([
            # writeerow is use to write a row of data into the csv file. 
            # save to the CSV file with the following colums
            datetime.now(),
            text,
            happy,
            sad,
            fear,
            anger
        ])
    # the data is saved into a CSV file named after the current survey page (e.g., survey_1.csv, survey_2.csv, etc.).
    return jsonify({"status": "saved"}) 
# cite: https://www.geeksforgeeks.org/python/how-to-create-csv-output-in-flask/?utm_source=chatgpt.com

# THANK YOU PAGE 
@app.route('/thankyou')
def thankyou():
    return render_template("thankyou.html")


# VIEW ALL CSV DATA ON RENDER
@app.route('/view-data')
def view_data():
    survey_files = [
        "survey_1.csv",
        "survey_2.csv",
        "survey_3.csv",
        "survey_4.csv",
        "survey_5.csv",
        "survey_6.csv"
    ]

    html = "<h1>Survey Data</h1>"

    for filename in survey_files:
        html += f"<h2>{filename}</h2>"

        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.read()
                html += f"<pre>{content}</pre>"
        else:
            html += "<p>No data yet.</p>"

    return html

# VIEW ALL CSV DATA ON RENDER
@app.route('/view-data')
def view_data():
    survey_files = [
        "survey_1.csv",
        "survey_2.csv",
        "survey_3.csv",
        "survey_4.csv",
        "survey_5.csv",
        "survey_6.csv"
    ]

    html = "<h1>Survey Data</h1>"

    for filename in survey_files:
        html += f"<h2>{filename}</h2>"

        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.read()
                html += f"<pre>{content}</pre>"
        else:
            html += "<p>No data yet.</p>"

    return html

# RUN APP 
if __name__ == '__main__':
    app.run()