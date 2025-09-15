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


def check_response(testcase: str, actual_resp: str, expected_value):
    """Compare RESP integer response from socket to expected integer."""
    if actual_resp.startswith(":"):
        actual_value = int(actual_resp[1:].strip())
    else:
        actual_value = actual_resp  # fallback

    print(f"Testcase: {testcase}")
    print(f"Value given:    {actual_value}")
    print(f"Value expected: {expected_value}")
    if actual_value == expected_value:
        print(f"Test Result: {GREEN}PASS{RESET}")
    else:
        print(f"Test Result: {RED}FAIL{RESET}")
    print("-" * 50)


def main():
    # Clean up keys
    send_command(["DEL", "list_key"])
    send_command(["DEL", "missing_list_key"])

    # Create a list with 3 elements
    send_command(["RPUSH", "list_key", "a", "b", "c"])

    # Test LLEN for existing list
    result = send_command(["LLEN", "list_key"])
    check_response("LLEN existing list", result, 3)

    # Test LLEN for non-existent list
    result = send_command(["LLEN", "missing_list_key"])
    check_response("LLEN missing list", result, 0)


if __name__ == "__main__":
    main()
