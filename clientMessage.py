import socket
from splitter import Splitter


class ClientMessage:
    def __init__(self, header, *value):
        self.header = header
        self.values = []
        for val in value:
            self.values.append(val)

    def format(self):
        out = self.header + Splitter.HEADER
        for val in self.values:
            out += str(val) + Splitter.VALUE_SPLITTER
        return out

