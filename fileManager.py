import time


class fileManager:
    def __init__(self, filename: str, readOrWrite:bool,chunkSize=4096) -> None:
        self.filename = "Files/" + filename
        self.chunkSize = chunkSize
        self.target = open(self.filename, readOrWrite)
        self.chunk = chunkSize

    def getChunk(self): 
        chunk = self.target.read(self.chunkSize)
        self.chunk = len(chunk)
        return chunk

    def close(self):
        self.target.close()
    
