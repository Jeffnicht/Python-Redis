import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 6379


def send_command(command: bytes, label: str):
    """Send a raw RESP command and print the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command)
        data = s.recv(65536)
        print(f"{label} response: {data}")


if __name__ == "__main__":
    # BLPOP command (blocking)
    blpop_cmd = b"*3\r\n$5\r\nBLPOP\r\n$8\r\nlist_key\r\n$1\r\n5\r\n"

    # LPUSH command (because your server only implements LPUSH)
    lpush_cmd = (
        b"*6\r\n$5\r\nLPUSH\r\n$8\r\nlist_key\r\n"
        b"$6\r\nvalue1\r\n$6\r\nvalue2\r\n$6\r\nvalue3\r\n$6\r\nvalue4\r\n"
    )

    # Start BLPOP in a separate thread (will block until a value is pushed)
    blpop_thread = threading.Thread(
        target=send_command, args=(blpop_cmd, "BLPOP"), daemon=True
    )
    blpop_thread.start()

    # Give BLPOP time to connect and block
    time.sleep(1)

    # Push values to unblock BLPOP
    send_command(lpush_cmd, "LPUSH")

    # Wait for BLPOP thread to finish
    blpop_thread.join()
