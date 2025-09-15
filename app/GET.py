from memory import MEMORY
import threading
lock = threading.Lock()
def GET(clientConnection,command: list[str]):
    try:
        with lock:
            value = MEMORY.get(command[1])[0]
        if value:
            encoded = value.encode()              # convert string to bytes
            length = len(encoded)                 # length in bytes

            # RESP2 bulk string format: $<length>\r\n<data>\r\n
            resp = b"$" + str(length).encode() + b"\r\n" + encoded + b"\r\n"
            clientConnection.sendall(resp)
            print(MEMORY)
        else:
            clientConnection.sendall(b"$-1\r\n")
    except Exception as e:
        print(e)
        clientConnection.sendall(b"-ERR couldnt GET value\r\n")


