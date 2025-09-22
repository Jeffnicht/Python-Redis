import socket
HOST = "127.0.0.1"
PORT = 6379

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"*2\r\n$4\r\nTYPE\r\n$3\r\nkfy\r\n")
    data = s.recv(65536)
    print(data)