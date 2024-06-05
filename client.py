#!/usr/bin/env python

from websockets.sync.client import connect
import json

def hello():
    with connect("ws://localhost:8765") as websocket:
        websocket.send(json.dumps({ 
        "event": "connected",
        "protocol": "Call", 
        "version": "1.0.0"
        }))

        with open('./decoded.bin', 'rb') as file:
            while True:
                chunk = file.read(216)
                if chunk:
                    websocket.send(json.dumps(
                    { 
                    "event": "media",
                    "sequenceNumber": "1", 
                    "media": { 
                    "track": "outbound", 
                    "chunk": "1", 
                    "timestamp": "5",
                    "payload": chunk
                    } ,
                    "streamSid": "MZXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                    }
                ))
                else:
                    break
                
        message = websocket.recv()
        print(f"Received: {message}")

hello()