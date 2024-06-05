import speech_recognition as sr

def speech_recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")

        audio = r.listen(source)

        try:
            speech = r.recognize_google(audio).lower()
            print(speech)

            if "new music" in speech:
                print("tell user to get new music")

            elif "play" in speech:
                print("Audio file played!")

            elif "test" in speech:
                print("Testing user...")


        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you repeat?")
        except sr.RequestError:
            print("Sorry, I am having trouble accessing the service. Please try again later.")

if __name__ == "__main__":
    speech_recognition()