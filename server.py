from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json
from json import JSONDecoder
import sys


class Match:
    def __init__(self, data):
        self.winner = data["winner"]
        player1 = data["player1"]
        player2 = data["player2"]
        
        self.playerName1 = player1["name"]
        self.playerName2 = player2["name"]
        self.player1MatchData = player1["matchdata"]
        self.player2MatchData = player2["matchdata"]

    def toJson(self):
        return {"winner" : self.winner,
                "player1" : {"name" : self.playerName1, "matchdata" : self.player1MatchData},
                "player2" : {"name" : self.playerName2, "matchdata" : self.player2MatchData}}


class MatchId(Resource):
    def get(self, match_id):
        return matches[match_id]        

    def post(self, match_id):
        return 201

class Matches(Resource):
    def get(self):
        return matches

    def post(self):
        post_data = request.json
        device_id = post_data["device_id"]
        print(device_id)

        updated = False
        for match_info in matches:
            if device_id == match_info["device_id"]:
                match_info["match"] = Match(post_data["match"]).toJson()
                updated = True
                return post_data, 201
        
        if not updated:
            matches.append({"device_id" : post_data["device_id"], "match" : Match(post_data["match"]).toJson()})
            return post_data, 201

        return post_data, 404

            ##add the new device
            #if matches[match_id]["device_id"] == None:
            #    matches[match_id]["device_id"] = match_data["device_id"]
            #    matches[match_id]["match"] = Match(match_data["match"]).toJson()
            #    return match_data, 201
            ##update the existing match information
            #elif matches[match_id]["device_id"] == device_id:
            #    matches[match_id]["match"] = Match(match_data["match"]).toJson()
            #    return match_data, 201
            #else: 
            #    return match_data, 404


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)

    matches = []

    #{"device_id" : None, "match" : None}, 
    #{"device_id" : None, "match" : None}, 
    #{"device_id" : None, "match" : None}

    api.add_resource(MatchId, "/matches/<int:match_id>")
    api.add_resource(Matches, "/matches")
    app.run(host="0.0.0.0", debug=True)