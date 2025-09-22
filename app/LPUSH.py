from memory import MEMORY,lock
import threading
from helpers.serveBlockedClients import serveBlockedClients
#insert elements at the beginning of list in reverse order 
def LPUSH(clientConnection,command:list):
    try:
        if len(command) < 3:
            clientConnection.sendall(b"-ERR wrong number of arguments for 'LPUSH' command\r\n")
            return
        ttl = None
        key,elements = command[1], command[2:]
        elements = command[2:][::-1]
        if key in MEMORY:
            if isinstance(MEMORY[key][0],list):
                with lock:
                    MEMORY[key][0][:0] = elements # prepends elements in reverse order 
                listLen = len(MEMORY[key][0])   
                response = b":" + str(listLen).encode() + b"\r\n" 
                clientConnection.sendall(response)
                serveBlockedClients(key)
                return
            else:
                clientConnection.sendall(b"-cant perform LPUSH on a non list element\r\n")
                return
        elif key not in MEMORY:
            with lock:
                MEMORY[key] = ([*elements],None) #hardcode TTL to none
            response = b":" + str(len(MEMORY[key][0])).encode() + b"\r\n"
            clientConnection.sendall(response)
            serveBlockedClients(key)
            return
    except Exception as e:
        print(e)
        clientConnection.sendall(b"-LPUSH didnt work\r\n")
        return    
