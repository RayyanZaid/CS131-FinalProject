import zmq

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")  # Bind on all interfaces on port 5556

# Wait for the subscriber to connect
time.sleep(1)

# Send the start testing signal
socket.send_string("start testing")
print("Signal sent.")

# Clean up
socket.close()
context.term()
