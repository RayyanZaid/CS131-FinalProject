import zmq
import time
import os

# Function to receive a file from the server
def receive_file(socket, save_path):
    file_data = socket.recv()
    with open(save_path, 'wb') as f:
        f.write(file_data)
    print(f"File received and saved to {save_path}")

# Set up ZMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REQ)  # REQ socket for requests
socket.connect("tcp://192.168.4.45:5555")  # Connect to the server's port

print("Aural Nano client started, waiting for user command...")

while True:
    # Simulate user command
    user_command = input("Enter command (NEW_MUSIC/TEST/PLAY/SYNC): ").strip().upper()
    
    if user_command == "NEW_MUSIC":
        # Send new music command to the server
        socket.send_string("NEW_MUSIC")
        # Wait for the server's response (file data)
        receive_file(socket, "received_midi_file.mid")
        
        # Simulate waiting for user command for the next step
        time.sleep(2)

    elif user_command == "TEST":
        # Send test command to the server
        socket.send_string("TEST")
        # Wait for the server's response
        message = socket.recv_string()
        print(f"Received from server: {message}")
        
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
        socket.send_string("SYNC")
        # Wait for the server's response
        message = socket.recv_string()
        print(f"Received from server: {message}")

    else:
        print("Invalid command.")
