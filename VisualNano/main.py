import zmq
import time
import os
import visualGlobals

# Function to simulate waiting for an external signal from a website
def wait_for_website_signal():
    print("Waiting for signal from website...")
    time.sleep(2)  # Simulate waiting

    visualGlobals.sheetMusicName = input("Sheet Music Name: ")
    visualGlobals.imagePath = input("Image Path: ")
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

    midi_filepath = "midi_file.mid"

    if message == "NEW_MUSIC":
        # 1) Tell user to enter image and name on website
        print("Tell user to enter image and name on website")
        # 2) Wait for the user to press "Submit" on the website
        wait_for_website_signal()

        # 3) Run SheetVision to convert visualGlobals.imagePath to MIDI file        
        # Simulate processing an image to MIDI and saving it to a file
        print(f"Simulation of SheetVision converting {visualGlobals.imagePath} to a MIDI file")
        time.sleep(1)

        file_contents = b"This is midi data"  # Predefined MIDI data as bytes
        try:
            with open(midi_filepath, 'wb') as f:
                f.write(file_contents)
                print(f"MIDI data written to {midi_filepath}")
            send_file_and_string(socket, client_id, midi_filepath, visualGlobals.sheetMusicName)
        except Exception as e:
            print(f"Error writing MIDI file: {e}")

    elif message == "TEST":
        # Grade posture (dummy grading for example)
        visualGlobals.testName = data[3].decode('utf-8')
        print(f"Received testname: {visualGlobals.testName} from Aural Nano. Will perform test and store results in database.")
        
        start_time = time.time()
        duration = 3 


        # Call postureMain function instead
        while time.time() - start_time < duration:
            print("Grading posture...")
            time.sleep(0.25) 

        print(f"Saving Posture Test data under test name : {visualGlobals.testName}")
        print("Posture Graded")

        test_done_message = "Test Done on Visual!"
        
        # Send posture grade to the client
        socket.send_multipart([client_id, test_done_message.encode('utf-8')])
        print("Visual done signal sent to Aural Nano")
