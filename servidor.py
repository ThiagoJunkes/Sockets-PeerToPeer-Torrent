import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 50555
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"

peer_list = []

def handle_client(conn, addr):
    print("Nova conexao estabelecida: ", addr)

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        
        if msg == DISCONNECT_MSG:
            connected = False
        
        peer_list.append(f"{addr}({msg})")
        print(peer_list)
        #print(f"[{addr}] {msg}")
        #conn.send((f"Received: {msg}").encode(FORMAT))

    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    print(f"Server : {IP}:{PORT}  | Esperando conexao")
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("Conexoes: ", threading.active_count()-1)

if __name__ == "__main__":
    main()