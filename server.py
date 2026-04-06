import socket
import ssl
import threading
import time

HOST = '0.0.0.0'
PORT = 12345

clients = {}        # conn → username
rooms = {}          # room → [connections]
user_rooms = {}     # conn → room
room_seq = {}       # room → sequence

lock = threading.Lock()


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def broadcast(message, sender, room):
    for client in rooms.get(room, []):
        if client != sender:
            try:
                client.send(message.encode())
            except:
                pass


def handle_client(conn, addr):
    log(f"NEW CONNECTION {addr}")

    username = None

    try:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    raise ConnectionResetError()

                message = data.decode().strip()

                if len(message) > 1024:
                    conn.send("[ERROR] Message too long".encode())
                    continue

            except (ConnectionResetError, BrokenPipeError):
                break

            #/name
            if message.startswith("/name"):
                parts = message.split(" ", 1)
                if len(parts) < 2:
                    conn.send("[ERROR] Usage: /name <username>".encode())
                    continue

                new_username = parts[1]

                with lock:
                    if new_username in clients.values():
                        conn.send("[ERROR] Username taken".encode())
                        continue

                    clients[conn] = new_username
                    username = new_username

                conn.send(f"[SERVER] Username set to {username}".encode())
                log(f"{username} registered")

            #/join
            elif message.startswith("/join"):
                parts = message.split(" ", 1)
                if len(parts) < 2:
                    conn.send("[ERROR] Usage: /join <room>".encode())
                    continue

                room = parts[1]

                with lock:
                    if conn in user_rooms:
                        conn.send("[ERROR] Leave current room first".encode())
                        continue

                    if room not in rooms:
                        rooms[room] = []
                        room_seq[room] = 0

                    rooms[room].append(conn)
                    user_rooms[conn] = room

                broadcast(f"[SERVER] {username} joined {room}", conn, room)
                log(f"{username} joined {room}")

            #/leave
            elif message.startswith("/leave"):
                with lock:
                    room = user_rooms.get(conn)

                    if not room:
                        conn.send("[ERROR] Not in a room".encode())
                        continue

                    rooms[room].remove(conn)
                    del user_rooms[conn]

                broadcast(f"[SERVER] {username} left {room}", conn, room)
                log(f"{username} left {room}")

            #/msg
            elif message.startswith("/msg"):
                parts = message.split(" ", 1)
                if len(parts) < 2:
                    conn.send("[ERROR] Usage: /msg <text>".encode())
                    continue

                room = user_rooms.get(conn)

                if not room:
                    conn.send("[ERROR] Join a room first".encode())
                    continue

                text = parts[1]

                with lock:
                    room_seq[room] += 1
                    seq = room_seq[room]

                formatted = f"[{room}][{seq}] {username}: {text}"
                broadcast(formatted, conn, room)

                log(f"{formatted}")

            #/pm
            elif message.startswith("/pm"):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    conn.send("[ERROR] Usage: /pm <user> <msg>".encode())
                    continue

                target, text = parts[1], parts[2]
                found = False

                with lock:
                    for c, name in clients.items():
                        if name == target:
                            c.send(f"[PM] {username}: {text}".encode())
                            found = True
                            break

                if not found:
                    conn.send("[ERROR] User not found".encode())

            else:
                conn.send("[ERROR] Unknown command".encode())

    except Exception as e:
        log(f"ERROR {addr}: {e}")

    #closing
    with lock:
        username = clients.get(conn, "Unknown")

        if conn in user_rooms:
            room = user_rooms[conn]
            if conn in rooms.get(room, []):
                rooms[room].remove(conn)
                broadcast(f"[SERVER] {username} disconnected", conn, room)

        clients.pop(conn, None)
        user_rooms.pop(conn, None)

    conn.close()
    log(f"DISCONNECTED {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem")

    server.bind((HOST, PORT))
    server.listen(10)

    log(f"SERVER STARTED on {PORT}")

    while True:
        client_socket, addr = server.accept()

        try:
            secure_conn = context.wrap_socket(client_socket, server_side=True)
        except ssl.SSLError as e:
            log(f"SSL ERROR: {e}")
            client_socket.close()
            continue

        thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
        thread.start()


start_server()