def arrayToRESP(elements: list[str]) -> bytes:
    """
    Convert a Python list of strings into a RESP array.
    Example: ["SET", "mykey", "value"] ->
    b"*3\r\n$3\r\nSET\r\n$5\r\nmykey\r\n$5\r\nvalue\r\n"
    """
    resp = f"*{len(elements)}\r\n"
    for elem in elements:
        resp += f"${len(elem)}\r\n{elem}\r\n"
    return resp.encode()

