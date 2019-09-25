import socket

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ss.connect(('127.0.0.1', 3306))

print(ss.recv(1024))