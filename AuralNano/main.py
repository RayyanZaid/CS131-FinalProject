import zmq
import time
import os
import uuid

# Function to receive a file from the server
def receive_file(socket, save_path):
    data = socket.recv_multipart()
    file_data = data[0]


    with open(save_path, 'wb') as f:
        f.write(file_data)
    print(f"File received and saved to {save_path}")

# Set up ZMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.DEALER)  # DEALER socket for more complex communication
client_id = str(uuid.uuid4()).encode('utf-8')
socket.identity = client_id
socket.connect("tcp://192.168.4.45:5555")  # Connect to the server's port

print("Aural Nano client started, waiting for user command...")

while True:
    # Simulate user command
    user_command = input("Enter command (NEW_MUSIC/TEST/PLAY/SYNC): ").strip().upper()
    
    if user_command == "NEW_MUSIC":
        # Send new music command to the server
        socket.send_multipart([client_id, b"NEW_MUSIC"])
        # Wait for the server's response (file data)
        receive_file(socket, "received_midi_file.mid")
        
        # Simulate waiting for user command for the next step
        time.sleep(2)

    elif user_command == "TEST":
        # Send test command to the server
        socket.send_multipart([client_id, b"TEST"])
        # Wait for the server's response
        data = socket.recv_multipart()
        message = data[0]
        print(f"Received from server: {message.decode('utf-8')}")
        
        # Simulate processing received data
        print("Grading music...")
        time.sleep(1)
        print("Music graded.")
        
    elif user_command == "PLAY":
        # Simulate playing music
        print("Playing music measures 3-5...")
        time.sleep(3)
        print("Music played.")

    elif user_command == "SYNC":
        # Send sync signal to the server
        socket.send_multipart([client_id, b"SYNC"])
        # Wait for the server's response
        data = socket.recv_multipart()
        message = data[0]
        print(f"Received from server: {message.decode('utf-8')}")

    else:
        print("Invalid command.")
