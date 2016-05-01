from flask import render_template, session, redirect, request, url_for
from requests import get

from breqwatrapp import app


@app.route('/')
def main_page():
    return render_template("mainSearch.html")


@app.route('/notfound404')
def not_found():
    return render_template("notFound.html")


@app.route('/', methods=['POST'])
def search_query():
    session["username"] = request.form["username"]
    return redirect(url_for('get_user'))


@app.route('/search/user')
def get_user():
    url = "https://api.github.com/users"
    search = "/" + session["username"]
    user = get(url + search).json()
    if 'message' in user:
        return redirect(url_for('not_found'))
    else:
        return render_template('searchResult.html', user=user, repo=get(user["repos_url"]).json())


@app.route('/search/users')
def get_users():
    url = "https://api.github.com/search/users?q="
