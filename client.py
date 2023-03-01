import socket
import time
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
host = 'localhost'  # The remote host IP address
port = 3000       # The remote host port number

# Connect to the server
sock.connect((host, port))

print("Welcome to CLS File Sharing Platform")
print("Type HELP for list of commands")


def get():
    header = "GET#zero.py#"
    return header


while True:
    # Receive data from the server
    received_data = sock.recv(1024).decode()
    print(f"Server: {received_data}")

    # Send data to server
    # message = input(":")

    message = get()
    if len(message) == 0:
        message = "#"
    #
    sock.sendall(message.encode())
    input("#")

sock.close()
