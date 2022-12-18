from threading import Thread
from flask import Flask
import socket

class FlaskAppWithThreads:
    def __init__(self):
        self.app = Flask(__name__)

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to a specific port to listen for incoming messages
        self.sock.bind(('0.0.0.0', 5000)) # Listen on all available interfaces on port 5000

    def start(self):
        # Start the Flask app in a separate thread
        app_thread = Thread(target=self.app.run)
        app_thread.start()

        # Start the UDP message handler in a separate thread
        handler_thread = Thread(target=self.handle_udp_messages)
        handler_thread.start()

    def handle_udp_messages(self):
        while True:
            # Wait for an incoming message and store the sender's address and message data
            data, addr = self.sock.recvfrom(1024) # receive up to 1024 bytes of data

            # Handle the incoming message
            print('Received message from {}: {}'.format(addr, data))

    @self.app.route('/')
    def index():
        # Return a response to the client
        return 'Hello from Flask app!'

if __name__ == '__main__':
    # Create an instance of the Flask app with threads
    app = FlaskAppWithThreads()

    # Start the Flask app and the UDP message handler
    app.start()
