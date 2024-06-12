import asyncio
import websockets
import json
import base64
import subprocess
import os

PIPE_PATH = "/tmp/audio_pipe"

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def stream(websocket):

    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)

    # ffmpeg -re -stream_loop -1 -i voice.mp3 -c copy -f rtsp rtsp://localhost:8554/mystream

    process = subprocess.Popen(
    ['ffmpeg', '-f', 'mulaw', '-ar', '8000', '-i', PIPE_PATH, '-c:a', 'aac', '-b:a', '32k', '-f', 'rtsp', '-fflags', 'nobuffer', '-flags', 'low_delay', '-rtsp_transport', 'tcp', 'rtsp://localhost:8554/mystream'],
    # ['ffmpeg', '-f', 'mulaw', '-ar', '8000', '-i', PIPE_PATH, '-c:a', 'aac', '-b:a', '64k', '-f', 'rtsp', 'rtsp://localhost:8554/mystream/'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
    )
    # stdout, stderr = process.communicate()

    # print("FFmpeg Output:", stdout.decode())
    # print("FFmpeg Errors:", stderr.decode())
    with open(PIPE_PATH, 'wb') as pipe:
        print(pipe.closed)
        counter = 0
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
                chunk = base64.b64decode(payload)
                pipe.write(chunk)
            if data['event'] == "closed":
                print("Closed Message received: {}".format(message))
                break
        process.terminate()
        process.wait()
        os.remove(PIPE_PATH)
        print("WS connection closed")


async def main():
    async with websockets.serve(stream, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())  # This will run the WebSocket server
