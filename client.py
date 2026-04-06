import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 12345


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TLS setup
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

secure_client = context.wrap_socket(client)

secure_client.connect((HOST, PORT))

print("""
Connected to server!

Commands:
/name <username>
/join <room>
/msg <message>
/pm <user> <message>
/leave
""")

thread = threading.Thread(target=receive_messages, args=(secure_client,))
thread.daemon = True
thread.start()

while True:
    message = input()
    try:
        secure_client.send(message.encode())
    except:
        break