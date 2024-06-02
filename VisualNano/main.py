import zmq
import time
import os

# Function to simulate waiting for an external signal from a website
def wait_for_website_signal():
    print("Waiting for signal from website...")
    time.sleep(2)  # Simulate waiting
    print("Received signal from website")

# Function to send a file to the client
def send_file(socket, client_id, filepath):
    with open(filepath, 'rb') as f:
        file_data = f.read()
    socket.send_multipart([client_id, file_data])
    print(f"File {filepath} sent to Aural Nano")

# Set up ZMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.ROUTER)  # ROUTER socket for more complex communication
socket.bind("tcp://192.168.4.45:5555")  # Bind to port 5555

print("Visual Nano server started, waiting for client...")

while True:
    # Simulate waiting for an external signal
    wait_for_website_signal()
    
    # Simulate processing an image to MIDI and saving it to a file
    midi_filepath = "midi_file.mid"
    with open(midi_filepath, 'wb') as f:
        f.write(b'MIDI_DATA yay')  # Dummy MIDI data

    while True:
        # Wait for a request from the client
        data = socket.recv_multipart()

        message = data[2]
        client_id = data[1]
        message = message.decode('utf-8')
        print(f"Received request: {message}")

        if message == "NEW_MUSIC":
            # Send the MIDI file to the client
            send_file(socket, client_id, midi_filepath)

        elif message == "TEST":
            # Grade posture (dummy grading for example)
            print("Grading posture...")
            time.sleep(1)  # Simulate grading time
            posture_grade = "POSTURE_GRADE"
            
            # Send posture grade to the client
            socket.send_multipart([client_id, posture_grade.encode('utf-8')])
            print("Posture grade sent to Aural Nano")

        elif message == "SYNC":
            # Handle synchronization request from the client
            sync_signal = "SYNC_ACK"
            socket.send_multipart([client_id, sync_signal.encode('utf-8')])
            print("Synchronization signal sent to Aural Nano")

