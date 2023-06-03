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
            print("Conexao fechada: ", addr)
        
        if msg == "!baixar":
            conn.send((f"{peer_list}").encode(FORMAT))
        elif "!FILES!" in msg:
            msg = msg.replace("'!FILES!',", "")
            ip = f"{addr}"
            for peer in peer_list:
                if ip in peer:
                    peer_list.remove(peer)
                    break
            peer_list.append(f"{ip}({msg})")
            print(peer_list)
        else:
            print(msg)

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