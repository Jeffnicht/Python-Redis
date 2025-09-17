from memory import BLOCKED_CLIENTS, MEMORY
import threading
from helpers.arrayToRESPString import arrayToRESP
lock = threading.Lock()
def serveBlockedClients(key:str):
    if key in BLOCKED_CLIENTS and key in MEMORY:
        with lock:
            popedItem = MEMORY[key].pop()
            blockedClient = BLOCKED_CLIENTS[key].pop(0) #returns [clientConnection,locktime]
            if not MEMORY[key][0]:
                del MEMORY[key]
            if not blockedClient[key][0]:
                del blockedClient[key]
        response = arrayToRESP([key,popedItem[0]])
        print()
        blockedClient[0].sendall(response)

    return
        

