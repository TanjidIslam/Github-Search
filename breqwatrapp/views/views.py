from flask import render_template, session, redirect, request, url_for
from requests import get

from breqwatrapp import app


@app.route('/')
def main_page():
    return render_template("mainSearch.html")


@app.route('/', methods=['POST'])
def search_query():
    session["username"] = request.form["username"]
    return redirect(url_for('search_result'))


@app.route('/results')
def search_result():
    url = "https://api.github.com/users"
    search = "/" + session["username"]
    user = get(url + search).json()
    if 'message' in user:
        return '<center><h1>User not found</h1></br><a href="/">Back to search.</a></center>', 404
    else:
        return render_template('searchResult.html', user=user, repo=get(user["repos_url"]).json())
