import socket

class connectionManager:
    def __init__(self, sending: bool, sock: socket.socket, BATCH: int) -> None:
        self.sending = sending
        self.sock = sock
        self.BATCH = BATCH

    def next(self, data: str):  # Function that makes sure the there is no conflict in the sending / receiving
        if self.sending == True:
            self.sending = False
            return self.send(data)
        else:
            self.sending = True
            return self.receive(data)

    def receive(self, data: str):  # Function that will receive data
        try:
            data = self.sock.recv(self.BATCH).decode()
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            return 0
        return data

    def send(self, data: str):  # Function that will send the data
        try:
            self.sock.sendall(data.encode())
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            print("Connection aborted")
            return 0
        return 1

    def createHeader(command: str, arg1: str, arg2: str, data:str):
        header = command + "#" + arg1 + "#" + arg2 + "#" + data + "%"
        return header
    
