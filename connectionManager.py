import socket

class connectionManager:
    def __init__(self, sending: bool, sock: socket.socket, BATCH: int) -> None:
        self.sending = sending
        self.sock = sock
        self.BATCH = BATCH

    def receive(self, data: str):
        if self.sending == True:
            return self.send(data)
        else:
            return self.sock.recv(self.BATCH).decode()

    def send(self, data: str):
        print()
        if self.sending == False:
            return self.receive()
        else:
            return self.sock.sendall(data.encode())
