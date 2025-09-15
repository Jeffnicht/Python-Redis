import socket

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def send_command(command: list[str]) -> str:
    """Build RESP array from command and send it to the server."""
    resp = f"*{len(command)}\r\n"
    for elem in command:
        resp += f"${len(elem)}\r\n{elem}\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 6379))
        s.sendall(resp.encode())
        data = s.recv(4096)

    return data.decode(errors="ignore")


def parse_bulk_string(resp: str) -> str | None:
    """Parse RESP bulk string ($len\r\nvalue\r\n)."""
    if resp.startswith("$-1"):  # nil bulk string
        return None
    if resp.startswith("$"):
        parts = resp.split("\r\n", 2)
        if len(parts) >= 2:
            return parts[1]
    return resp


def parse_array(resp: str) -> list[str]:
    """Parse RESP array response into list of strings."""
    lines = resp.split("\r\n")
    result = []
    i = 1  # skip *N
    while i < len(lines) - 1:
        if lines[i].startswith("$"):
            length = int(lines[i][1:])
            if length == -1:
                result.append(None)
            else:
                result.append(lines[i + 1])
            i += 2
        else:
            i += 1
    return result


def check_response(testcase: str, actual, expected):
    """Compare actual vs expected and print result."""
    print(f"Testcase: {testcase}")
    print(f"Value given:    {actual}")
    print(f"Value expected: {expected}")
    if actual == expected:
        print(f"Test Result: {GREEN}PASS{RESET}")
    else:
        print(f"Test Result: {RED}FAIL{RESET}")
    print("-" * 50)


def main():
    # Clean up
    send_command(["DEL", "list_key"])

    # Create list [a, b, c, d, e]
    send_command(["RPUSH", "list_key", "a", "b", "c", "d", "e"])

    # LPOP with count 3 (normal case)
    result = send_command(["LPOP", "list_key", "3"])
    removed_elements = parse_array(result)
    check_response("LPOP with count=3", removed_elements, ["a", "b", "c"])

    # LPOP with count larger than remaining list
    result = send_command(["LPOP", "list_key", "10"])
    removed_elements = parse_array(result)
    # Expect only remaining elements ["d", "e"]
    check_response("LPOP with count larger than list", removed_elements, ["d", "e"])

    # LRANGE should now return empty list
    result = send_command(["LRANGE", "list_key", "0", "-1"])
    arr = parse_array(result)
    check_response("LRANGE after all removed", arr, [])


if __name__ == "__main__":
    main()
