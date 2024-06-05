import speech_recognition as sr
from TextToSpeech import playText
def speech_recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            speech = r.recognize_google(audio).lower()
            print("You said:", speech)
            return speech

        except sr.UnknownValueError:
            return "error"

        except sr.RequestError:
            playText("Sorry, I am having trouble accessing the service. Please try again later.")
            return "error"