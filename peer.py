#Conectar ao servidor
#Detectar arquivos no computador
#Enviar Informações para servidor
#Conectar com o peer
#Baixar arquivos do peer

#A cada 3 mim enviar ao servidor lista dos arquivos que possui

#Rarest First

import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 50555
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"

files_client = []

def files():
    local = os.path.dirname(os.path.realpath(__file__))

    for file in os.listdir(local):
        if file.endswith(".txt"):
            files_client.append(str(file))
        

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    print(f"Conectado no servidor {IP}:{PORT}")

    connected = True
    files()
    while connected:
        client.send(str(files_client).encode(FORMAT))
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")


if __name__ == "__main__":
    main()
