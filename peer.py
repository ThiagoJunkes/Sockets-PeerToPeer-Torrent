#Conectar ao servidor
#Detectar arquivos no computador
#Enviar Informações para servidor
#Conectar com o peer
#Baixar arquivos do peer

#A cada 3 mim enviar ao servidor lista dos arquivos que possui

#Rarest First

import socket
import os


SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"
CONNECTING_MSG = "teste"

peers_files = []
my_files = []

def format_list(temp):
    peers_files.append = temp

def files():
    local = os.path.dirname(os.path.realpath(__file__))

    my_files.append("!FILES!")
    for file in os.listdir(local):
        if file.endswith(".txt"):
            my_files.append(str(file))
        

def main():
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 50555
    if(False):
        IP = input("IP: ")
        PORT = int(input("PORT: "))
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    print(f"Conectado no servidor {IP}:{PORT}")

    connected = True
    #Coleta arquivos txt pela primeira vez
    files()
    #Envia Arquivos txt para servidor
    client.send(str(my_files).encode(FORMAT)) 
    while connected:
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        
        if msg == "baixar":
            temp = client.recv(SIZE).decode(FORMAT)
            print(temp)
            #format_list(temp)


if __name__ == "__main__":
    main()
