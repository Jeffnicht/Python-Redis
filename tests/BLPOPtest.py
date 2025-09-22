import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 6379


def send_command(command: bytes, label: str, delay: float = 0):
    """Send a raw RESP command and print the response."""
    time.sleep(delay)  # allow staggering of execution if needed
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command)
        try:
            data = s.recv(65536)
            print(f"{label} response: {data}")
        except Exception as e:
            print(f"{label} error: {e}")


if __name__ == "__main__":
    # --- BLPOP Commands ---
    # BLPOP on list1 (forever block)
    blpop_list1_forever = b"*3\r\n$5\r\nBLPOP\r\n$5\r\nlist1\r\n$1\r\n0\r\n"

    # BLPOP on list2 (forever block)
    blpop_list2_forever = b"*3\r\n$5\r\nBLPOP\r\n$5\r\nlist2\r\n$1\r\n0\r\n"

    # BLPOP with timeout = 5 seconds (will expire)
    blpop_timeout_5s = b"*3\r\n$5\r\nBLPOP\r\n$5\r\nlist3\r\n$1\r\n5\r\n"

    # --- LPUSH Commands ---
    lpush_list1 = b"*3\r\n$5\r\nLPUSH\r\n$5\r\nlist1\r\n$6\r\nval_l1\r\n"
    lpush_list2 = b"*3\r\n$5\r\nLPUSH\r\n$5\r\nlist2\r\n$6\r\nval_l2\r\n"

    # --- Start BLPOPs in threads ---
    threads = []

    # Forever blocking BLPOPs
    threads.append(threading.Thread(
        target=send_command, args=(blpop_list1_forever, "BLPOP list1 forever"), daemon=True
    ))
    threads.append(threading.Thread(
        target=send_command, args=(blpop_list2_forever, "BLPOP list2 forever"), daemon=True
    ))

    # Timeout BLPOP
    threads.append(threading.Thread(
        target=send_command, args=(blpop_timeout_5s, "BLPOP list3 timeout=5s"), daemon=True
    ))

    for t in threads:
        t.start()

    # Give BLPOPs time to connect and block
    time.sleep(1)

    # Push to list1 and list2 to unblock the forever BLPOPs
    send_command(lpush_list1, "LPUSH list1")
    send_command(lpush_list2, "LPUSH list2")

    # Wait longer than 5 seconds so the timeout BLPOP expires
    print("Waiting 6 seconds for timeout BLPOP to trigger $-1...")
    time.sleep(6)

    # Join threads (the forever ones may stay blocked until push)
    for t in threads:
        t.join(timeout=1)

    print("Test complete.")
