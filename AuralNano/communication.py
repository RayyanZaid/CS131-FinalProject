import zmq

def setup_aural_nano():
    context = zmq.Context()
    # Create a PAIR socket
    socket = context.socket(zmq.PAIR)
    # Bind the socket to a port
    socket.bind("tcp://*:5555")  # Bind on all interfaces on port 5555

    while True:
        # Wait for a message from the Visual Nano
        message = socket.recv_string()
        print("Received from Visual Nano:", message)
        
        # Send a response back or a new message
        socket.send_string("Start testing from Aural Nano")
        print("Message sent to Visual Nano.")

    # Clean up
    socket.close()
    context.term()

if __name__ == "__main__":
    setup_aural_nano()
