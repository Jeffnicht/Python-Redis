@staticmethod
def decodeCommand(rawStr: bytes) -> tuple[list[str] | str | int, int]:
    """
    Parses one RESP message from rawStr.
    Returns (parsed_value, bytes_consumed).
    Raises ValueError if the message is incomplete.
    """
    if not rawStr:
        raise ValueError("Empty input")

    prefix = rawStr[0]

    # Simple string
    if prefix == ord('+') or prefix == ord('-') or prefix == ord(':'):
        end = rawStr.find(b"\r\n")
        if end == -1:
            raise ValueError("Incomplete message")
        data = rawStr[1:end]
        consumed = end + 2
        if prefix == ord('+') or prefix == ord('-'):
            return data.decode("utf-8"), consumed
        elif prefix == ord(':'):
            return int(data), consumed

    # Bulk string
    elif prefix == ord('$'):
        end = rawStr.find(b"\r\n")
        if end == -1:
            raise ValueError("Incomplete message")
        length = int(rawStr[1:end])
        total_len = end + 2 + length + 2
        if len(rawStr) < total_len:
            raise ValueError("Incomplete message")
        data = rawStr[end+2:end+2+length].decode("utf-8")
        return data, total_len

    # Array
    elif prefix == ord('*'):
        pos = 1
        end = rawStr.find(b"\r\n", pos)
        if end == -1:
            raise ValueError("Incomplete message")
        n_elements = int(rawStr[pos:end])
        pos = end + 2
        out = []

        for _ in range(n_elements):
            if pos >= len(rawStr):
                raise ValueError("Incomplete message")
            element_prefix = rawStr[pos]
            sub_value, consumed = decodeCommand(rawStr[pos:])
            out.append(sub_value)
            pos += consumed

        return out, pos

    # Boolean (RESP3)
    elif prefix == ord('#'):
        end = rawStr.find(b"\r\n")
        if end == -1:
            raise ValueError("Incomplete message")
        return rawStr[1:end].decode("utf-8"), end + 2

    # Unknown
    else:
        raise ValueError(f"Unknown prefix: {prefix}")
