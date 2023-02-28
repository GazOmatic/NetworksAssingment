import socket
import threading
controlHost = ""
PORT = 3000

def processHeader(header,conn):
   print(f"Client: {header}")
   output = "sdjskdjk"
   conn.sendall(output.encode())


def clientThread(conn):
    with conn:
        print(f"Connected by {addr} on {PORT}")
        conn.sendall("Hello from server".encode())
        while True:
            data = conn.recv(1024)
            if not data:
                break
            processHeader(data,conn)

threads = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.bind((controlHost, PORT))
        clientSocket.listen()
        while True:
            try:
                conn, addr = clientSocket.accept()
                t = threading.Thread(target=clientThread, daemon=True, args=(conn,))
                t.start()
                threads.append(t)
                print(len(threads))
            except KeyboardInterrupt:
                print("DONe")
                socket.close()
    

    
