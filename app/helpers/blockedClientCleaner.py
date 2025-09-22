import threading
import time
from memory import BLOCKED_CLIENTS, lock  # reuse your existing lock

def blockedClientCleaner():
    """
    Active cleaner for blocked clients.
    Checks all keys in BLOCKED_CLIENTS and removes clients whose
    lock/timeout has expired, sending $-1 to unblock them.
    """
    while True:
        now = time.time()
        with lock:
            keys_to_remove = []

            # iterate over all blocked keys
            for key, clients in BLOCKED_CLIENTS.items():
                i = 0
                while i < len(clients):
                    clientConnection, expire_time = clients[i]

                    # check if client has a timeout and it's expired
                    if expire_time != 0 and expire_time <= now:
                        try:
                            clientConnection.sendall(b"$-1\r\n")
                        except Exception as e:
                            print(f"Error sending timeout to client: {e}")
                        clients.pop(i)  # remove expired client
                    else:
                        i += 1  # only increment if we didn't pop

                # mark key for removal if no clients remain
                if not clients:
                    keys_to_remove.append(key)

            # remove empty keys from BLOCKED_CLIENTS
            for key in keys_to_remove:
                BLOCKED_CLIENTS.pop(key, None)

        # sleep a short interval before next check
        time.sleep(0.5)  # check twice per second
