import asyncio
import websockets
import json
import base64

from google.cloud.speech_v2_pb2 import StreamingRecognizeRequest, RecognitionConfig

client = SpeechClient()

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

def transcribe_streaming_v2(audio_generator):
    config = {
        "encoding": "MULAW",
        "sample_rate_hertz": 8000,
        "language_code": "en-US",
    }

    streaming_config = {
        "config": config,
    }

    # Call the generator to start iterating over its elements
    audio_chunks = audio_generator()

    requests = (
        StreamingRecognizeRequest(streaming_config=config, audio_content=chunk)
        for chunk in audio_generator
    )

    responses = client.streaming_recognize(requests=requests)

    for response in responses:
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")

async def stream(websocket):
    async for message in websocket:
        if message is None:
            break
        
        data = json.loads(message)
        if data['event'] == "connected":
            print("Connected Message received: {}".format(message))
        if data['event'] == "start":
            print("Start Message received: {}".format(message))
        if data['event'] == "media":
            payload = data['media']['payload']
            # Decode PCMU (G.711 mu-law) audio
            decoded_audio = decode_pcmu(payload)
            asyncio.create_task(transcribe_streaming_v2(decoded_audio))
        if data['event'] == "closed":
            print("Closed Message received: {}".format(message))
            break
    print("WS connection closed")

def decode_pcmu(encoded_data):
    # The generator function will yield chunks of the decoded audio
    def generator():
        for i in range(0, len(encoded_data), 160):
            chunk = encoded_data[i:i + 160]
            yield chunk
    return generator

async def main():
    async with websockets.serve(stream, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())  # This will run the WebSocket server
