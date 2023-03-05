import socket
BATCH = 4096
KEY = 3


class connectionManager:
    latestMessage = ""

    def __init__(self, sending: bool, sock: socket.socket, BATCH=4096) -> None:
        self.sending = sending
        self.sock = sock
        self.BATCH = BATCH

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
            data = self.decrypt(self.sock.recv(self.BATCH).decode())
        except ConnectionResetError:
            print("Error lost connection!")
            return 0
        except ConnectionAbortedError:
            return 0
        return data

    def send(self, data: str):  # Function that will send the data
        try:
            if type(data) != bytes:
                data = self.encrypt(data)
                data = data.encode()

            self.sock.sendall(data)
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
        global KEY
        ciphertext = ""
        for char in message:
            if char.isalpha():
                # Shift the character by the key, wrapping around if necessary
                shifted_char = chr(
                    (ord(char) - ord('a') + KEY) % 26 + ord('a'))
                ciphertext += shifted_char
            else:
                # Leave non-alphabetic characters unchanged
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext: str):
        """
        Decrypts a ciphertext using a shift cipher with the given key.
        """
        global KEY
        message = ""
        for char in ciphertext:
            if char.isalpha():
                # Shift the character by the inverse of the key, wrapping around if necessary
                shifted_char = chr(
                    (ord(char) - ord('a') - KEY) % 26 + ord('a'))
                message += shifted_char
            else:
                # Leave non-alphabetic characters unchanged
                message += char
        return message
