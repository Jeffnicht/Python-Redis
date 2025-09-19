from memory import BLOCKED_CLIENTS, MEMORY
import threading
from helpers.arrayToRESPString import arrayToRESP

lock = threading.Lock()

def serveBlockedClients(key: str):
    print("Got to the W8 list")

    if key in BLOCKED_CLIENTS and key in MEMORY:
        with lock:
            values, expire_time = MEMORY[key]

            if not values:  # nothing to pop
                return

            poppedItem = values.pop(0)  # BLPOP → pop from head
            clientConnection, locktime = BLOCKED_CLIENTS[key].pop(0)

            # update or delete MEMORY
            if not values:
                del MEMORY[key]
            else:
                MEMORY[key] = (values, expire_time)

            # cleanup blocked clients
            if not BLOCKED_CLIENTS[key]:
                del BLOCKED_CLIENTS[key]

        response = arrayToRESP([key, poppedItem])
        clientConnection.sendall(response)
        print("Sent response to blocked client")

    return
