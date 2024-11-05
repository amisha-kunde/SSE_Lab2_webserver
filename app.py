from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/github")
def github_username():
    return render_template("github.html")


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
                "https://api.github.com/repos/" + input_username + "/" + repo["name"] + "/commits"
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
                }
            )
    else:
        repo_data = []

    return render_template(
        "githubSubmit.html", username=input_username, repositories=repo_data
    )
