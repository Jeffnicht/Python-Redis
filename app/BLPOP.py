from datetime import datetime, timedelta
from memory import MEMORY,BLOCKED_CLIENTS
def BLPOP(clientConnection,command:list):
    try:
        print(clientConnection)
        listsToLock,lockDuration = command[1:-1],command[-1]
        for key in listsToLock:
            lockDurationInt = int(lockDuration) 
            if  lockDurationInt != 0 and lockDurationInt > 0:
                lockExpiresAt = datetime.now() + timedelta(seconds=lockDurationInt)
            else:
                lockExpiresAt = 0
            if key not in MEMORY or MEMORY[key][0] == []:
                if key in BLOCKED_CLIENTS:
                    BLOCKED_CLIENTS[key].append([clientConnection,lockExpiresAt])
                else:
                    BLOCKED_CLIENTS[key] = [[clientConnection,lockExpiresAt]]
        print("Got Here", BLOCKED_CLIENTS)

        return
    except Exception as e:
        clientConnection.sendall(b"BLPOP didnt work")
        print(e)