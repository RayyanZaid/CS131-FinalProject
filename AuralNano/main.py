import zmq
import time
import os
import uuid
import datetime
import auralGlobals
from MusicPlayingGrading import testMusic
from playMidiFile import play_midi

from TextToSpeech import playText
from SpeechRecognition import speech_recognition
def receive_file_and_string(socket, save_path):
    data = socket.recv_multipart()
    file_data = data[0]
    message_str = data[1].decode('utf-8')
    auralGlobals.sheetMusicName = message_str
    with open(save_path, 'wb') as f:
        f.write(file_data)
    print(f"File received and saved to {save_path} and string {message_str}")



# Set up ZMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.DEALER)
client_id = str(uuid.uuid4()).encode('utf-8')
socket.identity = client_id
socket.connect("tcp://192.168.7.191:5555")
print("Aural Nano client started, waiting for user command...")

while True:
    speech = speech_recognition()
    if speech == "error":
        continue

    if "new music" in speech:
        os.remove("received_midi_file.mid")
        playText("Upload a clear screenshot of your sheet music on the website.")
        socket.send_multipart([client_id, b"NEW_MUSIC"])
        playText("I am processing your sheet music is processing now. This may take a while, so feel free to practice on your own until you hear me tell you I'm ready")
        receive_file_and_string(socket, "received_midi_file.mid")
        playText("I have finished processing the sheet music. Feel free to say any of the commands you see on the screen")

    elif "test" in speech:
        playText("Angle the camera to have a side view of yourself.")
        playText("Get ready for a 4 beat count off and then play the music. You have 5 seconds before the count off")
        time.sleep(5)
        testName = auralGlobals.sheetMusicName + "-" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        socket.send_multipart([client_id, b"TEST", testName.encode('utf-8')])
        import json

        # Assuming 'testMusic' returns an integer grade and a feedback array
        grade, feedback = testMusic()

        # Convert feedback array to JSON string
        feedback_json = json.dumps(feedback)

        # Send grade and feedback as part of the multipart message
        socket.send_multipart([client_id, b"TEST_DONE", str(grade).encode('utf-8'), feedback_json.encode('utf-8')])

        print("Test results and feedback sent to Visual Nano")
        playText(f"Music Test Completed: You played {auralGlobals.sheetMusicName} and receieved a music grade of {grade}%. Check your test cards on the website for more details and feedback.")

        print("Test results sent to Visual Nano")

    elif "play" in speech:
        playText("I will play the music for you now. Feel free to follow along")
        play_midi('received_midi_file.mid')
        playText("Music has finished playing")

    else:
        playText("Please say a valid command")
