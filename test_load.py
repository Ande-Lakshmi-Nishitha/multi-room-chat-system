import socket
import ssl
import threading
import time

HOST = '127.0.0.1'
PORT = 12345

NUM_CLIENTS = 10


def simulate_client(id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        s = context.wrap_socket(sock)
        s.connect((HOST, PORT))

        username = f"user{id}"
        s.send(f"/name {username}".encode())
        time.sleep(0.1)

        s.send(f"/join room1".encode())
        time.sleep(0.1)

        for i in range(5):
            msg = f"/msg hello {i} from {username}"
            s.send(msg.encode())
            time.sleep(0.05)

        s.close()

    except Exception as e:
        print(f"Client {id} error: {e}")


threads = []

start = time.time()

for i in range(NUM_CLIENTS):
    t = threading.Thread(target=simulate_client, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()

print(f"\nTest completed with {NUM_CLIENTS} clients")
print(f"Time taken: {end - start:.2f} seconds")