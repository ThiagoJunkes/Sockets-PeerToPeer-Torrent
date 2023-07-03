import socket
import threading
import time

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"

peer_list = []
peer_ghost = []

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))

    def handle_client(self, conn, addr):
        print("New Connection Established: ", addr)

        connected = True
        while connected:
            msg = conn.recv(SIZE).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                for peer in peer_list:
                    ip = f"{addr[0]}"
                    if ip in peer:
                        peer_list.remove(peer)
                        break
                connected = False
                print("Connection Closed: ", addr)
                print(": ", peer_list)
            elif msg == "!baixar":
                conn.send((f"{peer_list}").encode(FORMAT))
            elif "!FILES!" in msg:
                msg = msg.replace("'!FILES!',", "")
                ip = f"{addr[0]}"
                for peer in peer_list:
                    if ip in peer:
                        peer_list.remove(peer)
                        break
                peer_list.append(f"{ip}({msg})")
                
                peer_ghost.append({"ip": ip, "count": 3})
                print(": ", peer_list)

        conn.close()

    def decrease_ghost_peer(self):
        while True:
            time.sleep(120)
            peers_to_remove = []
            for peer in peer_ghost:
                peer["count"] -= 1
                if peer["count"] == 0:
                    peer_ghost.remove(peer)
                    peer_list.remove(peer)

            print("Updated Peer List: ", peer_list)

    def start(self):
        print(f"Server: {self.ip}:{self.port} | Waiting for connections")
        self.server.listen()

        ghost_thread = threading.Thread(target=self.decrease_ghost_peer)
        ghost_thread.start()

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print("Connections: ", threading.active_count() - 2)

if __name__ == "__main__":
    IP = input("Type Servers IP: ")
    PORT = int(input("PORT: "))
    server = Server(IP, PORT)
    server.start()
