import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Load the audio file
audio_file_path = "decoded.wav"
with sr.AudioFile(audio_file_path) as source:
    audio_data = recognizer.record(source)

# Recognize (convert from audio to text)
try:
    text = recognizer.recognize_google(audio_data)
    print("Transcription: " + text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
