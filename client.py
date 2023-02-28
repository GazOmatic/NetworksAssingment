import socket
import time
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
host = 'localhost'  # The remote host IP address
port = 3000       # The remote host port number

# Connect to the server
sock.connect((host, port))

# Receive data from the server
while True:
    received_data = sock.recv(1024).decode()
    print(f"Server: {received_data}")
    message = input(":")
    if len(message) == 0:
        message = "#"
    sock.sendall(message.encode())


sock.close()
