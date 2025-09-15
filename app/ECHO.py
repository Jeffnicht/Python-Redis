def ECHO(clientConnection, command: list[str]):
    # remove first word (command itself)
    command_to_send = command[1:]
    
    # join the remaining words into a single string
    command_str = " ".join(command_to_send)
    
    # encode to bytes
    encoded = command_str.encode("utf-8")
    length = len(encoded)
    
    # build RESP bulk string
    resp_message = b"$" + str(length).encode() + b"\r\n" + encoded + b"\r\n"
    
    # send everything
    clientConnection.sendall(resp_message)
