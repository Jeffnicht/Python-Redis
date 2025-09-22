def stringToNormalRespString(value: str) -> bytes:
    """
    Convert a string into a RESP simple string.

    Example:
        "list" -> b"+list\r\n"
    """
    return b"+" + value.encode() + b"\r\n"


# Example usage
if __name__ == "__main__":
    resp = stringToNormalRespString("list")
    print(resp)  # b"+list\r\n"
