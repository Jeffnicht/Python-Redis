def PONG(clientConnection,data):
    print(f"data:{data}")
    if data:
        clientConnection.send("+PONG\r\n".encode())
        return
    return