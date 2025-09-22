from memory import MEMORY,lock
from helpers.stringToNormalRespString import stringToNormalRespString 
def TYPE(clientConnection,command:list):
    try:
        key = command[1]
        print(command)
        if MEMORY.get(key) != None:
            typeName = type(MEMORY[key][0]).__name__
            clientConnection.sendall(stringToNormalRespString(typeName))
        else:
            clientConnection.sendall(b'+none\r\n')
    except Exception as e:
        print(e)
        clientConnection.sendall(b"-TYPE command didnt work")