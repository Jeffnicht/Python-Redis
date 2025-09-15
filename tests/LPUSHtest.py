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
        data = s.recv(65536)

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
    # Detect if it's an integer reply
    if actual_resp.startswith(":"):
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
    print("== Testing LPUSH ==")

    # Ensure clean slate
    send_command(["DEL", "list_key"])

    # Single LPUSH with multiple values in one call:
    # LPUSH list_key "a" "b" "c" -> pushes "a", then "b", then "c"
    # final list should be ["c","b","a"] and the returned integer is 3.
    result = send_command(["LPUSH", "list_key", "a", "b", "c"])
    check_response('LPUSH list_key "a" "b" "c" (length)', result, 3)

    result = send_command(["LRANGE", "list_key", "0", "-1"])
    check_response('LRANGE after LPUSH "a" "b" "c"', result, ["c", "b", "a"])

    # Push another single element (head)
    result = send_command(["LPUSH", "list_key", "d"])
    check_response('LPUSH list_key "d" (length)', result, 4)

    result = send_command(["LRANGE", "list_key", "0", "-1"])
    check_response('LRANGE after LPUSH "d"', result, ["d", "c", "b", "a"])

    # Demonstrate difference when doing multiple LPUSH calls:
    send_command(["DEL", "list_key"])
    res1 = send_command(["LPUSH", "list_key", "c"])
    check_response('LPUSH list_key "c" (single)', res1, 5)
    res2 = send_command(["LPUSH", "list_key", "b", "a"])
    # LPUSH "b" then "a" => final ["a","b","c"]
    check_response('LPUSH list_key "b" "a" (length)', res2, 7)
    res3 = send_command(["LRANGE", "list_key", "0", "-1"])
    check_response('LRANGE after LPUSH "c" then LPUSH "b" "a"', res3, ['a', 'b', 'c', 'd', 'c', 'b', 'a'])


if __name__ == "__main__":
    main()
