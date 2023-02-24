import socket

# Define the host and port
HOST = 'localhost'
PORT = 8000

# Create a new socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the host and port
    s.bind((HOST, PORT))
    # Listen for incoming connections
    s.listen()
    
    while True:
        # Wait for a new client to connect
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            # Receive data from the client
            data = conn.recv(1024)
            # Process the data
            processed_data = data
            # Send the processed data back to the client
            conn.sendall(processed_data)
        # Close the connection with the client
        conn.close()
        
        # Close the socket
        # s.close()

        # Reopen the socket and wait for a new client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()