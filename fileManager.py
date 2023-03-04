import time


class fileManager:
    def __init__(self, filename: str, chunkSize=4096, write=False) -> None:
        self.filename = "Files/" + filename
        self.chunkSize = chunkSize
        b = 'rb'
        if write:
            b = 'wb'
        self.target = open(self.filename, b)
        self.chunk = chunkSize

    def getChunk(self):
        chunk = self.target.read(self.chunkSize)
        self.chunk = len(chunk)
        return chunk

    def close(self):
        self.target.close()