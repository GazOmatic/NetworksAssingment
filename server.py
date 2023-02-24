import socket
import time
controlHost = ""
controlPort = 420


def negotiate(conn):
    conn.sendall(b"PORT:1000")
    return True

def server(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                if PORT == 420:
                    if negotiate(conn):
                        s.close()
                        time.sleep(2)
                        print("Not closed")
                # data = conn.recv(1024)


while True:
    server(controlHost,controlPort)
    print("Resetting control port")
    time.sleep(2)
