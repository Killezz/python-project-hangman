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
    json_object = json.dumps(highScores, indent=4)
    with open("data.json", "w") as data:
        data.write(json_object)


def addHighScore(name, score):
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
