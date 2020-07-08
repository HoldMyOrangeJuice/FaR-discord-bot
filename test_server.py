import socket
import time

socket = socket.socket()
socket.bind(('0.0.0.0', 1337))
socket.listen(5)
conn, addr = socket.accept()

while True:

    conn.send("hi from server".encode())
    time.sleep(1)