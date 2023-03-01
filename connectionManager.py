import socket


class connectionManager:
    def __init__(self, sending: bool, sock: socket.socket, BATCH: int) -> None:
        self.sending = sending
        self.sock = sock
        self.BATCH = BATCH

    def next(self, data: str):
        if self.sending == True:
            self.sending = False
            return self.send(data)
        else:
            self.sending = True
            return self.receive(data)

    def receive(self, data: str):
        try:
            data = self.sock.recv(self.BATCH).decode()
        except ConnectionResetError:
            print("Lost connection to client")
        return data

    def send(self, data: str):
        try:
            self.sock.sendall(data.encode())
        except ConnectionResetError:
            print("Could not send data")
        return "Send success"
