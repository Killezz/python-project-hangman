"""
Backend for Hangman console game that has various functions.
"""
import json
import os
import sys
from random import randint
from flask import Flask, request, render_template

os.chdir(sys.path[0])

app = Flask(__name__)
apiSecret = "verySecretPassword123321"


@app.route("/", methods=["GET"])
def displayScores():
    """
    Returns page that contains all high scores.
    """
    sort = request.args.get("sort")
    if sort == "asc":
        scores = sorted(highScores, key=lambda k: k['score'])
    elif sort == "desc":
        scores = sorted(highScores, key=lambda k: k['score'], reverse=True)
    else:
        return render_template('scores.html', scores=highScores)
    return render_template('scores.html', scores=scores)


@app.route("/api/scores", methods=["GET", "POST"])
def scores():
    """
    Authorization required else Unauthorized 401 is returned.

    GET Method:
    Returns JSON formatted high score list with possible filtering options: limit, sort.

    POST Method:
    Gets name, score from request.json and tries to add them to high score json file. Returns Success 201, Bad Request 400.
    """
    if request.headers.get("Authorization") == apiSecret:
        if request.method == "GET":
            try:
                limit = int(request.args.get("limit"))
            except BaseException:
                limit = -1
            sort = request.args.get("sort")
            if sort == "asc":
                scores = sorted(highScores, key=lambda k: k['score'])
            elif sort == "desc":
                scores = sorted(highScores, key=lambda k: k['score'], reverse=True)
            else:
                return highScores[:limit]
            return scores[:limit]
        if request.method == "POST":
            data = request.json
            if "name" in data and "score" in data:
                name = data["name"]
                score = data["score"]
                addHighScore(name, score)
                return {"message": "Success"}, 201
            else:
                return {"message": "Bad Request"}, 400
    else:
        return {"message": "Unauthorized"}, 401


@app.route("/api/scores/<ID>", methods=["GET", "DELETE"])
def scoresById(ID):
    """
    Authorization required else Unauthorized 401 is returned.

    GET Method:
    Returns specific ID data containing id, name, score if found else Not Found 404.

    DELETE Method:
    Deletes passed ID if found and returns Success 200 and Not Found 404 if ID does not exist.
    """
    if request.headers.get("Authorization") == apiSecret:
        if request.method == "GET":
            data = getHighScore(ID)
            if data:
                return data
            else:
                return {"message": "Not Found"}, 404
        if request.method == "DELETE":
            success = deleteHighScore(ID)
            if success:
                return {"message": "Success"}, 200
            else:
                return {"message": "Not Found"}, 404
    else:
        return {"message": "Unauthorized"}, 401


def saveHighScoreJson():
    """
    Saves high scores to data.json file.

    Args:
    None

    Returns:
    None
    """
    json_object = json.dumps(highScores, indent=4)
    with open("data.json", "w") as data:
        data.write(json_object)


def addHighScore(name, score):
    """
    Adds new high score to high scores.

    Args:
    name (str): User name
    score (int): Seconds value in int format.

    Returns:
    None
    """
    while True:
        generatedId = randint(100, 10000000)
        for item in highScores:
            if item["id"] == generatedId:
                break
        else:
            break
    highScores.append({"id": generatedId, "name": name, "score": score})
    saveHighScoreJson()


def deleteHighScore(ID):
    """
    Tries to find ID on high scores and returns success boolean.

    Args:
    ID (int): ID to be deleted.

    Returns:
    bool: True if deleted else False
    """
    try:
        ID = int(ID)
        for item in highScores:
            if item["id"] == ID:
                highScores.remove(item)
                saveHighScoreJson()
                return True
    except BaseException:
        return False


def getHighScore(ID):
    """
    Searches high scores based on given ID.

    Args:
    ID (int): ID to be searched.

    Returns:
    ID Data or if not found None
    """
    try:
        ID = int(ID)
        for item in highScores:
            if item["id"] == ID:
                return item
    except BaseException:
        return None


try:
    with open("data.json", "r") as data:
        highScores = json.load(data)
except BaseException:
    highScores = []
    print("No data.json found")


if __name__ == "__main__":
    app.run(debug=True)
