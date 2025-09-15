from memory import MEMORY
from helpers.arrayToRESPString import arrayToRESP
def LRANGE(clientConnection,command:list):
    if len(command) != 4:
        response = b"-LRANGE commmand takes 3 Arguments "+ str(len(command)-1).encode() + b"wherer provided"
        clientConnection.sendall(response + b"\r\n")
        return
    #LRANGE list_key 0 2
    try:

        key,start,end = command[1],int(command[2]),int(command[3])
        # start index bigger than end 
        if start >= end and end > 0:
            clientConnection.sendall(b"*0\r\n")
            return
        
        #key doesnt exist
        elif key not in MEMORY:
            clientConnection.sendall(b"*0\r\n")
            return
        
        # start index bigger or equal to length or start with - index would reach index before 0 
        listLen = len(MEMORY[key][0])
        if start >= listLen or listLen - start < 0:
            clientConnection.sendall(b"*0\r\n")
            return
        elif listLen - end < 0 and end < 0 :
            clientConnection.sendall(b"*0\r\n")
            return

        # endindex bigger or equal to length will result in end becoming -1 (last element of list)
        elif end >= listLen:
            subArray = MEMORY[key][0][start:]
            response = arrayToRESP(subArray)
            clientConnection.sendall(response)
            return
        
        #checks if end -1 would become 0 
        if end +1 == 0:
            subArray = MEMORY[key][0][start:]
        else:
            subArray = MEMORY[key][0][start:end+1]
        print(subArray)
        response = arrayToRESP(subArray)
        clientConnection.sendall(response)
        
        
    except Exception as e:
        print(e)
        clientConnection.sendall(b"-Unknown error")
