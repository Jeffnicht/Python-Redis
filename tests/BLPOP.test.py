import socket
import threading

SERVER_ADDRESS = ("127.0.0.1", 6379)

def blpop_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    try:
        message = b"*3\r\n$5\r\nBLPOP\r\n$8\r\nlist_key\r\n$1\r\n5\r\n"
        client_socket.sendall(message)

        response = client_socket.recv(1024)  # BLPOP waits if list is empty
        print("[BLPOP] Received:", response.decode())
    finally:
        client_socket.close()

def rpush_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    try:
        message = (
            b"*6\r\n$5\r\nRPUSH\r\n$8\r\nlist_key\r\n"
            b"$1\r\na\r\n$1\r\nb\r\n$1\r\nc\r\n$1\r\nd\r\n"
        )
        client_socket.sendall(message)
        response = client_socket.recv(1024)  # RPUSH response
        print("[RPUSH] Received:", response.decode())
    finally:
        client_socket.close()

def lpush_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    try:
        message = (
            b"*5\r\n$5\r\nLPUSH\r\n$8\r\nlist_key\r\n$1\r\nx\r\n$1\r\ny\r\n"
        )
        client_socket.sendall(message)
        response = client_socket.recv(2000)  # LPUSH response
        print("[LPUSH] Received:", response.decode())
    finally:
        client_socket.close()

# Create threads
t1 = threading.Thread(target=blpop_client)
t2 = threading.Thread(target=rpush_client)
t3 = threading.Thread(target=lpush_client)

# Start threads
t1.start()
t2.start()
t3.start()

# Wait for threads to finish
t1.join()
t2.join()
t3.join()
