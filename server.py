from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json
from json import JSONDecoder


class Match:
    def __init__(self, data):
        player1 = data["player1"]
        player2 = data["player2"]
        
        self.playerName1 = player1["name"]
        self.playerName2 = player2["name"]
        self.player1MatchData = player1["matchdata"]
        self.player2MatchData = player2["matchdata"]

    def toJson(self):
        return {"player1" : {"name" : self.playerName1, "matchdata" : self.player1MatchData},
                "player2" : {"name" : self.playerName2, "matchdata" : self.player2MatchData}}
        


class Matches(Resource):
    def get(self, match_id):
        return matches[match_id]

    def post(self, match_id):
        match_data = request.json
        matches[match_id]["match"] = Match(match_data["match"]).toJson()
        return match_data, 201


app = Flask(__name__)
api = Api(app)

matches = [{"device_id" : 0, "match" : None}, 
           {"device_id" : 1, "match" : None}, 
           {"device_id" : 2, "match" : None}]

api.add_resource(Matches, "/matches/<int:match_id>")
app.run(host="0.0.0.0")
