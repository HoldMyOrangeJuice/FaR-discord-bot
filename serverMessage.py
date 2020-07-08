from protocol import Protocol
from splitter import Splitter


class ServerMessage:
    def __init__(self, raw):
        if Splitter.HEADER in raw:
            self.header = raw.split(Splitter.HEADER)[0]
            self.values = raw.split(Splitter.HEADER)[1]
        else:
            self.header = Protocol.UNKNOWN
            self.values = []

    def getValue(self, i):
        if i > len(self.values)-1:
            return ""
        return self.values[i]