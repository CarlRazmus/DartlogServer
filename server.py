from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO
from flask_cors import CORS
import json
from json import JSONDecoder
import sys


matches = []
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'dartlogSecret!'
socketio = SocketIO(app, cors_allowed_origins=['http://localhost:3000'])


def update_matches(match_info_input):
    device_id = match_info_input["device_id"]
    updated = False
    print(match_info_input)
    for match_info in matches:
        if device_id == match_info['device_id']:
            match_info["match"] = match_info_input["match"]
            updated = True
            return 201

    if not updated:
        matches.append(match_info_input)
        return 201

    return 404

@socketio.on('connect')
def client_connected():
    print('client connected')

@socketio.on('matchdata-update-from-android')
def update_matchdata(match_info):
    print("client sent matchdata via SocketIO from device " + mach_info["device_id"])
    update_matches(match_info)
    socketio.emit('matchdata-update-from-server', matches)


class MatchId(Resource):
    def get(self, match_id):
        return matches[match_id]        

    def post(self, match_id):
        return 201

class Matches(Resource):
    def get(self):
        return matches

    def post(self):
        match_info = request.json
        print("client sent matchdata via POST request from device " + match_info["device_id"])
        return_code = update_matches(match_info)
        if return_code == 201:
            socketio.emit('matchdata-update-from-server', matches)

        return match_info, return_code


if __name__ == "__main__":
    api = Api(app)
    api.add_resource(MatchId, "/matches/<int:match_id>")
    api.add_resource(Matches, "/matches")

    socketio.run(app, debug=True, port="5000", host='0.0.0.0')