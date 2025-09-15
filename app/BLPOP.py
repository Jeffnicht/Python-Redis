from memory import MEMORY,BLOCKED_CLIENTS
def BLPOP(clientConnection,command:list):
    try:
        listsToLock,lockDuration = command[1:-1],command[-1]
        for key in listsToLock:
            if key not in MEMORY or MEMORY[key][0] == []:
                if key in BLOCKED_CLIENTS:
                    print(BLOCKED_CLIENTS)
                    BLOCKED_CLIENTS[key].append([clientConnection,lockDuration])
                else:
                    BLOCKED_CLIENTS[key] = [[clientConnection,lockDuration]]

                
    except Exception as e:
        print(e)

BLPOP(None,["BLPOP","ggh","2"])
print(BLOCKED_CLIENTS)
