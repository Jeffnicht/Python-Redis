import socket
import threading, time
from Pong import PONG
from RPP import decodeCommand
from ECHO import ECHO
from GET import GET
from SET import SET
from memory import MEMORY
from RPUSH import RPUSH
from LPUSH import LPUSH 
from LRANGE import LRANGE
from LLEN import LLEN
from LPOP import LPOP
from BLPOP import BLPOP
storeKeyExpires = {} #schema key : (value,timestamp)
storeKeyExpiresLock = threading.Lock()
bytesPerMessage = 1024

command_map = {
    "ECHO": ECHO,
    "PING": PONG,
    "SET": SET,
    "GET": GET,
    "RPUSH" : RPUSH,
    "LPUSH" : LPUSH,
    "LRANGE" : LRANGE,
    "LLEN"  : LLEN,
    "LPOP"  : LPOP,
    "BLPOP" : BLPOP
}


def expireKeys():
    while True:
        now = time.time()
        keys_to_delete = []

        for key, (value, expiry) in MEMORY.items():
            if expiry and expiry <= now:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            MEMORY.pop(key, None)

        time.sleep(0.1)




         

def commandMapper(command: list[str]):
    # look up the function in O(1)
    func = command_map.get(command[0].upper())
    if func:
        return func
    else:
        return lambda conn, cmd: conn.sendall(b"-ERR unknown command\r\n")

# function to handle a single client
def handle_client(clientConnection):
    buffer = bytearray()  # per-client buffer

    try:
        while True:
            try:
                chunk = clientConnection.recv(bytesPerMessage)
            except (ConnectionResetError, ConnectionAbortedError):
                print("Client connection aborted")
                break

            if not chunk:
                print("Client disconnected gracefully")
                break

            buffer.extend(chunk)

            # parse all complete commands
            while True:
                try:
                    command, consumed = decodeCommand(buffer)  # decodeCommand must return bytes consumed
                    buffer = buffer[consumed:]
                    func = commandMapper(command)
                    if func:
                        func(clientConnection, command)
                except ValueError:
                    # incomplete command, wait for more data
                    break

    finally:
        clientConnection.close()
        print("Connection closed")


def main():
    print("Logs from your program will appear here!")
    threading.Thread(target=expireKeys, daemon=True).start()
    server_socket = socket.create_server(("127.0.0.1", 6379))
    

    while True:
        clientConnection, _ = server_socket.accept()
        print("Got new connection")
        thread = threading.Thread(target=handle_client, args=(clientConnection,))
        thread.start()

if __name__ == "__main__":
    main()

