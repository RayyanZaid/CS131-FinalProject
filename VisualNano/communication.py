import zmq
import time

def setup_visual_nano(aural_ip):
    context = zmq.Context()
    # Create a PAIR socket
    socket = context.socket(zmq.PAIR)
    # Connect the socket to the Aural Nano server
    socket.connect(f"tcp://{aural_ip}:5555")  # Replace aural_ip with the Aural Nano's IP

    # Optionally send a message first
    socket.send_string("Visual Nano is ready")
    print("Message sent to Aural Nano.")

    while True:
        # Wait for a response or new message
        message = socket.recv_string()
        print("Received from Aural Nano:", message)
        
        # Respond back or send new messages as needed
        time.sleep(5)  # Simulate some delay or processing
        socket.send_string("Acknowledged by Visual Nano")
        print("Response sent to Aural Nano.")

    # Clean up
    socket.close()
    context.term()

if __name__ == "__main__":
    # Replace 'aural_ip' with the actual IP address of the Aural Nano
    setup_visual_nano("10.13.130.221")
