from flask import Flask, render_template, request
import re

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/")  # route handler, is a decorator
def hello_world():  # route endpoint
    return render_template("index.html")


@app.route("/query", methods=["GET"])
def process_query_route():
    query = request.args.get("q")
    return process_query(query)


def addition_query(query):
    match = re.search(r"(\d+)\s+plus\s+(\d+)", query)
    if match:
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        return str(num1 + num2)
    else:
        return "Query not recognized."


def process_query(query):
    if "name" in query:
        return "ak4924"
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    if "plus" in query:
        return addition_query(query)
    elif query == "asteroids":
        return "Unknown"
    else:
        return "Unknown"
