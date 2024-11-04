from flask import Flask, render_template, request
import requests

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


# github exercise

@app.route("/github")
def github_username():
    return render_template("github.html")

@app.route("/github-submit", methods=["POST"])
def process_github_lookup():
    input_username = request.form.get("username")
    
    response = requests.get(f"https://api.github.com/users/{input_username}/repos")
    
    if response.status_code == 200:
        repos = response.json()
        
        repo_data = []
        for repo in repos:
            repo_info = {
                "name": repo["name"],
                "updated_at": repo["updated_at"], 
                "url": repo["html_url"] 
            }
            repo_data.append(repo_info)
    else:
        repo_data = [] 
    return render_template("githubSubmit.html", username=input_username, repositories=repo_data)


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


# call to GitHub API

