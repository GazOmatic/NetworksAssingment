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

    def receive(self, BATCH=BATCH):
        """Receive data from the socket and decrypt it.

            Args:
                BATCH: An integer representing the maximum amount of data to receive at once (default: BATCH).

            Returns:
                If data is received successfully, a string containing the decrypted data is returned.
                If the connection is lost, the function returns 0.
        """
        try:
            data = self.sock.recv(BATCH + 1464)
            data = self.decrypt(data)
            data = data.decode()
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            return 0
        return data

    def send(self, data: str):
        """Encrypt the given data and send it to the connected socket.

        Args:
            data: A string representing the data to send.
        Returns:
            If the data is sent successfully, the function returns 1.
            If the connection is lost or aborted, the function returns 0.
        """
        try:
            if type(data) == bytes:
                self.sock.sendall(self.encrypt(data))
            else:
                self.sock.sendall(self.encrypt(data.encode()))
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            print("Connection aborted")
            return 0
        return 1

    def sendBytes(self, data: str):
        """Encrypt the given data and send it to the connected socket.

        Args:
            data: A string representing the data to send.
        Returns:
            If the data is sent successfully, the function returns 1.
            If the connection is lost or aborted, the function returns 0.
        """
        try:

            self.sock.sendall(self.encrypt(data))
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            print("Connection aborted")
            return 0
        return 1

    def receiveBytes(self, BATCH=BATCH):
        """Receive data from the socket and decrypt it.

            Args:
                BATCH: An integer representing the maximum amount of data to receive at once (default: BATCH).

            Returns:
                If data is received successfully, a string containing the decrypted data is returned.
                If the connection is lost, the function returns 0.
        """
        try:
            data = self.sock.recv(BATCH + 1464)
            data = self.decrypt(data)
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            return 0
        return data

    def encrypt(self, message: bytes):
        """
        Encrypts a message using the Fernet library.
        """
        print(len(message))
        print(len(self.f.encrypt(message)))
        return self.f.encrypt(message)

    def decrypt(self, message: bytes):
        """
        Decrypts a message using the Fernet Library.
        """
        print(message)
        return self.f.decrypt(message)
