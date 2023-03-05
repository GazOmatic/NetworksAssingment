import socket
from cryptography.fernet import Fernet
BATCH = 4096
KEY = b'h-IDapb9rhqFVERkTFDdijIrIlo_jX9v8NpONIqI1mQ='


class connectionManager:
    latestMessage = ""

    def __init__(self, sending: bool, sock: socket.socket, BATCH=4096) -> None:
        self.sending = sending
        self.sock = sock
        self.BATCH = BATCH
        self.f = Fernet(KEY)

    def next(self, data: str):  # Function that makes sure the there is no conflict in the sending / receiving
        if self.sending == True:
            self.sending = False
            return self.send(data)
        else:
            self.sending = True
            self.latestMessage = self.receive(data)
            return self.latestMessage

    def receive(self, BATCH=BATCH):  # Function that will receive data
        try:
            data = self.sock.recv(BATCH)
            data = self.decrypt(data).decode()
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            return 0
        return data

    def send(self, data: str):  # Function that will send the data
        try:
            self.sock.sendall(self.encrypt(data.encode()))
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            print("Connection aborted")
            return 0
        return 1

    def encrypt(self, message: str):
        """
        Encrypts a message using a shift cipher with the given key.
        """
        return self.f.encrypt(message)
        
        
    def decrypt(self, message: str):
        """
        Decrypts a ciphertext using a shift cipher with the given key.
        """
        return self.f.decrypt(message)
