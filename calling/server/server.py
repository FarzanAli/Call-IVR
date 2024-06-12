from flask import Flask, Response, jsonify, request
import os
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import Dial, VoiceResponse, Start
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(logger=True, engineio_logger=True)
socketio.init_app(app)

@app.route("/token", methods=["GET"])
def token():
    # required for all twilio access tokens
    # To set up environmental variables, see http://twil.io/secure
    account_sid = 'ACfce0bee058855c707f4c5690c22fe852'
    api_key = 'SK4c8a280d6347ace78dd3ff2d90b87829'
    api_secret = 'PZbd09tyH6Qn9f70p60j4zphCUnnk638'

    # required for Voice grant
    outgoing_application_sid = 'AP9e0a6f4bead7347a842b3667fe28da34'
    identity = 'user'

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a Voice grant and add to token
    voice_grant = VoiceGrant(
        outgoing_application_sid=outgoing_application_sid,
        incoming_allow=True, # Optional: add to allow incoming calls
    )
    token.add_grant(voice_grant)

    # Return token info as JSON
    print(token.to_jwt())

    return token.to_jwt()


@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    start = Start()
    start.stream(name='streaming', url='wss://13df-2607-fea8-f4d9-4df0-3021-ab47-d56c-7074.ngrok-free.app/', track='outbound_track')
    resp.append(start)
    resp.dial(request.form.get("To"), caller_id='+13656560656')
    return Response(str(resp), mimetype="text/xml")

@socketio.on('connect')
def test_connect(auth):
    print('connected brotherrrr')
    emit('my response', {'data': 'Connected'})

@socketio.on('message')
def connected(data):
    print("Connected message received: {}".format(data))

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 4000), app, handler_class=WebSocketHandler)
    print("Server listening on: http://localhost:" + str(4000))
    server.serve_forever()