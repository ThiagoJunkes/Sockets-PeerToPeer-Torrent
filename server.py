import socket
import threading

#PORT = 50555
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"

peer_list = []

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
                print(": ",peer_list)

        conn.close()

    def main():
        IP = input("Type Servers IP: ")
        PORT = int(input("PORT: "))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM -> TCP Socket
        server.bind((IP, PORT))
        print(f"Server : {IP}:{PORT}  | Waiting for connections")
        server.listen()

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=Server.handle_client, args=(conn, addr))
            thread.start()
            print("Connections: ", threading.active_count()-1)

if __name__ == "__main__":
    Server.main()