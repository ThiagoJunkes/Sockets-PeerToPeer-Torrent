import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 50555
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"

def handle_client(conn, addr):
    print("Nova conexao estabelecida: ", addr)

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        
        if msg == DISCONNECT_MSG:
            connected = False
        
        print(f"[{addr}] {msg}")
        conn.send((f"Received: {msg}").encode(FORMAT))

    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    print(f"Server : {IP}:{PORT}  | Esperando conexão")
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("Conexoes: ", threading.activeCount()-1)

#if __name__ == "__main__":
main()