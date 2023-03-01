import socket


class connectionManager:
    def __init__(self, sending: bool, sock: socket.socket, BATCH: int) -> None:
        self.sending = sending
        self.sock = sock
        self.BATCH = BATCH

    def next(self, data: str):
        if self.sending == True:
            sending = False
            return self.send(data)
        else:
            sending = True
            return self.receive(data)

    def receive(self, data: str):
        data = self.sock.recv(self.BATCH).decode()
        return data

    def send(self, data: str):
        self.sock.sendall(data.encode())
        return "Send success"
