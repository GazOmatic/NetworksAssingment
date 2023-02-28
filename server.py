import socket
import threading
import os
controlHost = ""
PORT = 3000


def processHeader(message, conn):
    print(f"Client: {message}")
    if message.split("#")[0] == "LIST":
        actionList(message)
    elif message.split("#")[0] == "GET":
        actionGet(message)
    elif message.split("#")[0] == "POST":
        actionPost(message)
    elif message.split("#")[0] == "HELP":
        actionHelp(message)
    else:
        conn.sendall("Unknown Server Command".encode())
    output = "Output"
    conn.sendall(output.encode())


# This method lists all files to the client
def actionList(message):
    if message.split("#")[1] == "":

        files = os.listdir("Files/")
        for f in files:
            list.append("/n", f)

        conn.sendall(list.encode())
    elif message.split("#")[1] == "ACCESS":
        conn.sendall("List all files I have access to".encode())
    else:
        conn.sendall("Unknown Server Command".encode())


def actionGet(message):
    print("GET")


def actionPost(message):
    print("POST")


# This function prints a list of all commands the server accepts to the client


def actionHelp(message):

    print("HELP")


def clientThread(conn):
    with conn:
        print(f"Connected by {addr} on {PORT}")
        conn.sendall("Hello from server".encode())
        while True:
            # decoded
            data = conn.recv(1024).decode()
            if not data:
                break
            processHeader(data, conn)


threads = []

print("test: ", actionList("LIST##"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.bind((controlHost, PORT))
        clientSocket.listen()
        while True:
            try:
                conn, addr = clientSocket.accept()
                t = threading.Thread(target=clientThread,
                                     daemon=True, args=(conn,))
                t.start()
                threads.append(t)
                print(len(threads))
            except KeyboardInterrupt:
                print("DONe")
                socket.close()
