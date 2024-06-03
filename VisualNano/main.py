import zmq
import time
import os

import visualGlobals
import postureMain

from SheetVision import main
from midiFogLayer import transposeToBFlat, remove_last_note_events

# Function to simulate waiting for an external signal from a website
def wait_for_website_signal():
    print("Waiting for signal from website...")
    time.sleep(2)  # Simulate waiting
    visualGlobals.sheetMusicName = input("Sheet Music File Name: ")
    print("Received signal from website")

# Function to send a file to the client
def send_file_and_string(socket, client_id, filepath, sheetMusicName):
    try:
        with open(filepath, 'rb') as f:
            file_data = f.read()
        print(f"File {filepath} read successfully with length {len(file_data)}")
        socket.send_multipart([client_id, file_data, sheetMusicName.encode('utf-8')])
        print(f"File {filepath} and sheet music name '{sheetMusicName}' sent to Aural Nano")
    except Exception as e:
        print(f"Failed to send file: {e}")

# Set up ZMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.ROUTER)  # ROUTER socket for more complex communication
socket.bind("tcp://192.168.4.45:5555")  # Bind to port 5555

print("Visual Nano server started, waiting for client...")

while True:
    # Wait for a request from the client
    data = socket.recv_multipart()
    client_id = data[1]
    message = data[2].decode('utf-8')
    print(f"Received request: {message}")

    if message == "NEW_MUSIC":
        print("Tell user to enter image and name on website")
        wait_for_website_signal()
        visualGlobals.imagePath = f"{visualGlobals.sheetMusicName}"

        # Run SheetVision to convert visualGlobals.imagePath to MIDI file 
        untransposed_midi_filepath = main.sheetvisionMain(visualGlobals.imagePath)
        transposed_midi_filepath = transposeToBFlat(untransposed_midi_filepath)
        finalized_midi_filepath = remove_last_note_events(transposed_midi_filepath)

        print(f"Transposed MIDI file path: {transposed_midi_filepath}")

        try:
            send_file_and_string(socket, client_id, transposed_midi_filepath, visualGlobals.sheetMusicName)
            os.remove(finalized_midi_filepath)
        except Exception as e:
            print(f"Error with MIDI file: {e}")

    elif message == "TEST":
        visualGlobals.testName = data[3].decode('utf-8')
        print(f"Received test name: {visualGlobals.testName} from Aural Nano. Will perform test and store results in database.")
        
        visualGlobals.testDoneFlag = False
        import threading
        grading_thread = threading.Thread(target=postureMain.postureGrading)
        grading_thread.start()
        
        while not visualGlobals.testDoneFlag:
            try:
                data = socket.recv_multipart(flags=zmq.NOBLOCK)
                message = data[2].decode('utf-8')
                if message == "TEST_DONE":
                    print("Received TEST_DONE signal from Aural Nano.")
                    visualGlobals.testDoneFlag = True
            except zmq.Again:
                time.sleep(0.1)

        grading_thread.join()
        print(f"Saving Posture Test data under test name : {visualGlobals.testName}")
        print("Posture Graded")

