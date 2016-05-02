from flask import render_template, session, redirect, request, url_for
from requests import get

from breqwatrapp import app


@app.route('/')
def main_page():
    return render_template("mainSearch.html")


@app.route('/notfound404')
def not_found():
    return render_template("notFound.html", error=session["error"])


@app.route('/', methods=['POST'])
def search_query():
    category = request.form["selectCategory"]
    if category == "Username":
        session["username"] = request.form["username"]
        return redirect(url_for('get_user'))
    elif category == "Users":
        session["users"] = {
            "keyword": request.form["keywordUsers"],
            "type": request.form["userType"],
            # "language": request.form["languageUsers"],
            "repos": request.form["repoNum"],
            "followers": request.form["followerUsers"],
            "location": request.form.get("countryUsers")
        }
        return redirect(url_for('get_users'))
    elif category == "Repositories":
        session["repos"] = {
            "keyword": request.form["keywordRepo"].replace(" ", "+"),
            "repo": request.form["repoName"],
            "user": request.form["repoOwner"],
            "size": request.form["repoSize"],
            "forks": request.form["forkNum"],
            "stars": request.form["minStar"]
        }
        return redirect(url_for('get_repos'))


@app.route('/user')
def get_user():
    url = "https://api.github.com/users"
    search = "/" + session["username"]
    user = get(url + search).json()
    if 'message' in user:
        session["error"] = "No result was found based on your input. Try Again!"
        return redirect(url_for('not_found'))
    else:
        return render_template('searchResult.html', user=user, repo=get(user["repos_url"]).json())


@app.route('/users')
def get_users():
    userInput = session["users"]

    userInfo = {key: value for key, value in userInput.items() if value}

    if len(list(userInfo.keys())) <= 1:
        session["error"] = "Search Result is too large, be more specific!"
        return redirect(url_for('not_found'))

    if "repos" in userInfo:
        userInfo["repos"] = ">=" + userInfo["repos"]

    if "followers" in userInfo:
        userInfo["followers"] = ">=" + userInfo["followers"]

    api = "https://api.github.com/search/users?q=" + userInfo.pop("keyword")
    if userInfo["type"] != all:
        api += "+" + "type:" + userInfo["type"]
        userInfo.pop("type")
    for key in userInfo:
        if key == "location":
            api += "&" + key + ":" + userInfo[key]
        else:
            api += "+" + key + ":" + userInfo[key]

    userJson = get(api).json()
    if userJson["total_count"] < 1:
        session["error"] = "No result was found based on your input. Try Again!"
        return redirect(url_for("not_found"))
    userList = []
    for user in userJson["items"]:
        userList.append(get(user["url"]).json())
    return render_template('usersResult.html', users=userList, count=userJson["total_count"])


@app.route('/repos')
def get_repos():
    userInput = session["repos"]

    repoInfo = {key: value for key, value in userInput.items() if value}

    if len(list(repoInfo.keys())) < 1:
        session["error"] = "Search Result is too large, be more specific!"
        return redirect(url_for('not_found'))

    if "size" in repoInfo:
        repoInfo["size"] = ">=" + repoInfo["size"]

    if "forks" in repoInfo:
        repoInfo["forks"] = ">=" + repoInfo["forks"]

    if "stars" in repoInfo:
        repoInfo["stars"] = ">=" + repoInfo["stars"]

    api = "https://api.github.com/search/repositories?q=" + repoInfo.pop("keyword")

    for key in repoInfo:
        api += "+" + key + ":" + repoInfo[key]

    repoJson = get(api).json()

    if repoJson["total_count"] < 1:
        session["error"] = "No result was found based on your input. Try Again!"
        return redirect(url_for("not_found"))
    repoList = []
    for repo in repoJson["items"]:
        repo["owner_obj"] = repo["owner"]
        repoList.append(repo)
    return render_template('repoResults.html', repos=repoList, count=repoJson["total_count"])
