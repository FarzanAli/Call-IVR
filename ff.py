import subprocess

PIPE_PATH = '/tmp/audio_pipe'

process = subprocess.Popen(
    ['ffmpeg', '-re', '-stream_loop', '-1', '-i', 'voice.mp3', '-c', 'copy', '-f', 'rtsp', 'rtsp://localhost:8554/mystream'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Optional: read output and error streams if needed
# stdout, stderr = process.communicate()

# print("FFmpeg Output:", stdout.decode())
# print("FFmpeg Errors:", stderr.decode())