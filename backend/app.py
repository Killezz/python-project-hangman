import json
import os
import sys
from random import randint
from flask import Flask, request

os.chdir(sys.path[0])

app = Flask(__name__)
apiSecret = "verySecretPassword123321"
highScores = []

try:
    with open("data.json", "r") as data:
        highScores = json.load(data)
except BaseException:
    print("No data.json found")


def addHighScore(name, score):
    while True:
        generatedId = randint(100, 10000000)
        for item in highScores:
            if item["id"] == generatedId:
                break
        else:
            break
    highScores.append({"id": generatedId, "name": name, "score": score})
    json_object = json.dumps(highScores, indent=4)
    with open("data.json", "w") as data:
        data.write(json_object)


@app.route("/api/scores", methods=["GET", "POST", "DELETE"])
def scores():
    if request.headers.get("Authorization") == apiSecret:
        if request.method == "GET":
            try:
                limit = int(request.args.get("limit"))
            except BaseException:
                limit = -1

            scores = sorted(highScores, key=lambda k: k['score'])

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


app.run(debug=True)
