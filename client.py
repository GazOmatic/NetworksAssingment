import socket
import time
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
host = 'localhost'  # The remote host IP address
port = 420       # The remote host port number

# Connect to the server
sock.connect((host, port))

# Receive data from the server
received_data = sock.recv(1024).decode()


newPort = int(received_data.split(":")[1])

print(newPort)

sock.close()


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

c.connect((host, newPort))
while True:
    s = c.recv(1024)
    print(s)
    c.sendall(input("#").encode())
c.close()


# Close the socket connection
# sock.close()
