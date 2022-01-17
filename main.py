import speech_recognition as sr
import gtts
from playsound import playsound
import os
from datetime import datetime
from notion import NotionClient

r = sr.Recognizer()
ACTIVATION = "hello"

token = "//API_ID//"
database_id = "//DATABASE_ID"

client = NotionClient(token, database_id)


def get_audio():
    with sr.Microphone() as src:
        print("Please talk")
        audio = r.listen(src)
    return audio


def audio_to_text(audio):
    text = ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("The audio was not recognizable")
    except sr.RequestError:
        print("Could not request results from API")
    return text


def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = "//Location path for storing the temporary MP3 file//"
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except AssertionError:
        print("Could not play sound")


if __name__ == "__main__":
    while True:
        a = get_audio()
        command = audio_to_text(a)
        if ACTIVATION in command:
            print("activate")
            play_sound("What do you want me to do?")

            note = get_audio()
            note = audio_to_text(note)

            if note:
                play_sound(note)

                now = datetime.now().astimezone().isoformat()
                res = client.create_page(note, now, status="On Progress")

                if res.status_code == 200:
                    play_sound("Added to the to-do list")
