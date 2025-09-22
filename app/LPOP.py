from memory import MEMORY,lock
import threading
from helpers.arrayToRESPString import arrayToRESP
def LPOP(clientConnection,command:list):
    try:
        commandLen = len(command)
        # checks if command is exactly 2 or 3 params 
        if commandLen != 3:
            if commandLen != 2:
                clientConnection.sendall(b"-LRANGE commmand takes 2 or 3 arguments\r\n")
                return
        
        key = command[1]
        if key in MEMORY:
            tempQueryedElement = MEMORY[key] # make a copy of element i work on so i dont have to lookup in dict everytime i need len() for example
            if isinstance(tempQueryedElement[0],list) and tempQueryedElement[0] != []:
                #command is 2 long pop left most value by default 
                if commandLen == 2:
                    with lock:
                        response = MEMORY[key][0].pop(0)
                        if not MEMORY[key][0]:  # list is empty
                            del MEMORY[key]
                    response = str(response).encode()
                    strLen = str(response).encode() 
                    clientConnection.sendall(b"$" + strLen + b"\r\n" + response + b"\r\n") #$<length>\r\n<data>\r\n"
                    return
                #command has to be 3 long 
                else:
                    # to remove range cant be bigger than list itself
                    try:
                        toRemoveRange = int(command[2]) 
                    except Exception as e:
                        clientConnection.sendall(b"-Provided range wasnt a valid number")
                        return
                    listLen = len(tempQueryedElement[0])
                    if toRemoveRange <= 0:
                        clientConnection.sendall(b"-LPOP only accepts positive integer")
                        return
                    elif  listLen >= toRemoveRange:
                        removeList = tempQueryedElement[0][:toRemoveRange]
                        response = arrayToRESP(removeList)
                        clientConnection.sendall(response)
                        with lock:
                            MEMORY[key][0][:] = tempQueryedElement[0][toRemoveRange:]
                            if not MEMORY[key][0]:  # list is empty
                                del MEMORY[key]
                            
                    else:
                        # list elements to delete are longer than the list return the list 
                        clientConnection.sendall(arrayToRESP(tempQueryedElement[0]))

                #if we got here none of the errors where caught or the command didnt fulfill its purpose 
                clientConnection.sendall(b"-Unknown error")
                return
            else:
                clientConnection.sendall(b"$-1\r\n")
                return 
        else:
            clientConnection.sendall(b"$-1\r\n")
            return 
    except Exception as e:
        clientConnection.sendall(b"-Unknown error")
        print(e)
        return
    
