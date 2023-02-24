import socket

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
host = 'localhost'  # The remote host IP address
port = 420       # The remote host port number

# Connect to the server
sock.connect((host, port))

# Send data to the server
data = 'Hello, server!'
sock.sendall(data.encode())

# Receive data from the server
received_data = sock.recv(1024)
print(f"Received data: {received_data.decode()}")

# Close the socket connection
sock.close()