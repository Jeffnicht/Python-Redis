from memory import MEMORY,lock
import threading

import time
nx = False
def SET(clientConnection,command: list[str]):
    i = 0
    ttl = None
    key,value = command[1], command[2]
    while i< len(command):
        try:
            if command[i].upper() == "NX":
                if  key in MEMORY:
                    clientConnection.sendall(b"$-1\r\n")
                    return
        
            elif command[i].upper() == "EX":
                ttl = int(command[i+1])
                now = time.time()  # seconds, float
                ttl = now + ttl # absolute expiry timestamp in seconds

            elif command[i].upper() == "PX":
                ttl = int(command[i + 1]) / 1000
            i += 1
        except Exception as e:
            print(e)
            break
    
    try:
        with lock:
            MEMORY[key] = (value, ttl)
            print("Memory: ",MEMORY)
            clientConnection.sendall(b"+OK\r\n")
    except Exception as e:
        print(e)
        clientConnection.sendall(b"-ERR couldnt SET key\r\n")
    
    # keep in mid to check if there is problems that the function that keeps track of what keys to delete is hardcoded to use milliseconds and here you have a choice  
