from memory import MEMORY,lock
import threading
from helpers.serveBlockedClients import serveBlockedClients

def RPUSH(clientConnection,command:list):
    try:
        if len(command) < 3:
            clientConnection.sendall(b"-ERR wrong number of arguments for 'LPUSH' command\r\n")
            return

        ttl = None
        key,elements = command[1], command[2:]
        print(elements)
        if key in MEMORY:
            if isinstance(MEMORY[key][0],list):
                with lock:
                    MEMORY[key][0].extend(elements)
                indexOfNewItem = len(MEMORY[key][0])   
                response = b":" + str(indexOfNewItem).encode() + b"\r\n" 
                clientConnection.sendall(response)
                serveBlockedClients(key)    
            else:
                clientConnection.sendall(b"-cant perform RPUSH on a non list element\r\n")
        elif key not in MEMORY:
             with lock:
                MEMORY[key] = ([*elements],None) #hardcode TTL to none
             response = b":" + str(len(MEMORY[key][0])).encode() + b"\r\n"
             clientConnection.sendall(response)
             serveBlockedClients(key)
             
    except Exception as e:
        print(e)
        clientConnection.sendall(b"-RPUSH didnt work\r\n")
        return    
