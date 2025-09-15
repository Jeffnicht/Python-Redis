from memory import MEMORY
def LLEN(clientConnection,command:list):
    try:
        key = command[1]
        if len(command) != 2:
            clientConnection.sendall(b"-ERR wrong number of arguments for 'LLEN' command\r\n")
            return
        
        if key in MEMORY:
           response = b":" + str(len(MEMORY[key][0])).encode() + b"\r\n"
           clientConnection.sendall(response)
           return
        else:
            clientConnection.sendall(b":0\r\n")
    except Exception as e:
        print(e)
        clientConnection.sendall(b"-Unknown error")