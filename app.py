from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")  # route handler, is a decorator
def hello_world():  # route endpoint
    return render_template("index.html")


@app.route("/query", methods=["GET"])
def process_query_route():
    query = request.args.get("q")
    return process_query(query)


@app.route("/github-submit", methods=["POST"])
def process_github_lookup():
    input_username = request.form.get("username")

    repos_response = requests.get(
        f"https://api.github.com/users/{input_username}/repos"
    )
    if repos_response.status_code == 200:
        repos = repos_response.json()
        repo_data = []

        for repo in repos:
            commits_response = requests.get(
                f"https://api.github.com/repos/{input_username}/"
                f"{repo['name']}/commits"
            )

            if commits_response.status_code == 200:
                latest_commit = commits_response.json()[0]
                commit_info = {
                    "commit_hash": latest_commit["sha"],
                    "author": latest_commit["commit"]["author"]["name"],
                    "date": latest_commit["commit"]["author"]["date"],
                    "message": latest_commit["commit"]["message"],
                }

            repo_data.append(
                {
                    "name": repo["name"],
                    "updated_at": repo["updated_at"],
                    "url": repo["html_url"],
                    "latest_commit": commit_info,
                    "watchers": repo["watchers_count"],
                }
            )
    else:
        repo_data = []

    return render_template(
        "githubSubmit.html", username=input_username, repositories=repo_data
    )


def addition_query(query):
    match = re.search(r"(\d+)\s+plus\s+(\d+)", query)
    if match:
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        return num1 + num2
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
