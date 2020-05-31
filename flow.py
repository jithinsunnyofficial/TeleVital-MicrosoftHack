from tts import convert_and_play
from stt import generate_text
from dialogflow_api import analyze_text
import webbrowser
from playsound import playsound
import time

url = "https://televital.azurewebsites.net/"

def apicaller(text, session_id):
	final_text = analyze_text(text session_id)
	if final_text != 'end':
		convert_and_play(final_text)
		apicaller(analyze_text(generate_text), session_id)

def flow(text, session_id):
    apicaller(text, session_id)