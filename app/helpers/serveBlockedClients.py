from memory import BLOCKED_CLIENTS, MEMORY
import threading
import time
from helpers.arrayToRESPString import arrayToRESP

lock = threading.Lock()

def serveBlockedClients(key: str):
    while True:
        # Step 1: exit if no blocked clients or no memory
        if key not in BLOCKED_CLIENTS or key not in MEMORY:
            break

        with lock:
            # Step 2: check first client for timeout
            clientConnection, expire_time = BLOCKED_CLIENTS[key][0]
            if expire_time != 0 and expire_time < time.time():
                clientConnection.sendall(b"$-1\r\n")
                del BLOCKED_CLIENTS[key][0]
                if not BLOCKED_CLIENTS.get(key):
                    del BLOCKED_CLIENTS[key]
                continue  # skip to next iteration

            # Step 3: check if there is a value to pop
            values, retainTime = MEMORY[key]
            if not values:
                break

            # Step 4: pop value and client
            poppedItem = values.pop(0)
            clientConnection, _ = BLOCKED_CLIENTS[key].pop(0)

            # Step 5: clean up memory
            if not values:
                del MEMORY[key]

            # Step 6: clean up blocked clients key
            if not BLOCKED_CLIENTS.get(key):
                BLOCKED_CLIENTS.pop(key, None)

        # Step 7: send response outside lock
        response = arrayToRESP([key, poppedItem])
        clientConnection.sendall(response)
