import socket
import threading
import time

#PORT = 50555
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"

peer_list = []
peer_ghost = []

class Server: 
    def handle_client(conn, addr):
        print("New Connection Established: ", addr)

        connected = True
        global peer_list
        while connected:
            msg = conn.recv(SIZE).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                for peer in peer_list:
                    ip = f"{addr}"
                    if ip in peer:
                        peer_list.remove(peer)
                        break
                connected = False
                print("Connection Closed: ", addr)
                print(": ",peer_list)
            elif msg == "!baixar":
                conn.send((f"{peer_list}").encode(FORMAT))
            elif "!FILES!" in msg:
                msg = msg.replace("'!FILES!',", "")
                ip = f"{addr}"
                for peer in peer_list:
                    if ip in peer:
                        peer_list.remove(peer)
                        break
                peer_list.append(f"{ip}({msg})")
                peer_ghost.append({"ip": ip, "count": 3})
                print(": ",peer_list)

        conn.close()

    def decrease_ghost_peer():
        while True:
            time.sleep(120)  # Espera por 2 minutos
            
            for peer in peer_ghost:
                peer["count"] -= 1
                if peer["count"] == 0:
                    peer_ghost.remove(peer)  # Remove o par da lista peer_ghost

            print("Updated Peer List: ", peer_list)
    
    def main():
        IP = input("Type Servers IP: ")
        PORT = int(input("PORT: "))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM -> TCP Socket
        server.bind((IP, PORT))
        print(f"Server : {IP}:{PORT}  | Waiting for connections")
        server.listen()

        ghost_thread = threading.Thread(target=Server.decrease_ghost_peer)
        ghost_thread.start()

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=Server.handle_client, args=(conn, addr))
            thread.start()
            print("Connections: ", threading.active_count()-1)

if __name__ == "__main__":
    Server.main()