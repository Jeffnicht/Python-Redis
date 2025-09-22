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


def parse_resp_array(resp: str) -> list:
    """Parse a RESP array string into a Python list of strings."""
    lines = resp.replace("\r\n", "\n").split("\n")
    result = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("$") and i + 1 < len(lines):
            result.append(lines[i + 1])
            i += 2
        else:
            i += 1
    return result


def check_response(testcase: str, actual_resp: str, expected_value):
    """
    Compare the parsed RESP response from the socket to an expected Python value
    (list or int) and print the test result with colors.
    """
    if actual_resp.startswith(":"):  # Integer reply
        actual_value = int(actual_resp[1:].strip())
    else:
        actual_value = parse_resp_array(actual_resp)

    print(f"Testcase: {testcase}")
    print(f"Value given:    {actual_value}")
    print(f"Value expected: {expected_value}")
    if actual_value == expected_value:
        print(f"Test Result: {GREEN}PASS{RESET}")
    else:
        print(f"Test Result: {RED}FAIL{RESET}")
    print("-" * 50)


def main():
    print("== Testing RPUSH ==")


    # RPUSH one element
    result = send_command(["RPUSH", "list_key","a"])
    check_response("RPUSH a", result, 1)

    # RPUSH multiple elements at once
    result = send_command(["RPUSH", "list_key", "b", "c"])
    check_response("RPUSH b c", result, 3)

    # Verify list order (tail is rightmost)
    result = send_command(["LRANGE", "list_key", "0", "-1"])
    check_response("LRANGE full list", result, ["a", "b", "c"])

    # Push another element at tail
    result = send_command(["RPUSH", "list_key", "z"])
    check_response("RPUSH z", result, 4)

    # Verify order again
    result = send_command(["LRANGE", "list_key", "0", "-1"])
    check_response("LRANGE after RPUSH z", result, ["a", "b", "c", "z"])


if __name__ == "__main__":
    main()
