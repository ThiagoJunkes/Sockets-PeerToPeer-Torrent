#Conectar ao servidor
#Detectar arquivos no computador
#Enviar Informações para servidor
#Conectar com o peer
#Baixar arquivos do peer

#A cada 3 mim enviar ao servidor lista dos arquivos que possui

#Rarest First

import socket
import os
import threading
import time
import re
import ast

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"
global MY_IP

peers_files = []
my_files = []

def format_list(temp):
    peers_files.clear

    # Extrai o IP e a porta usando uma expressão regular
    port_ip = re.findall(r"\('([\d.]+)',\s(\d+)\)", temp)
    # Extrai a lista de arquivos como uma string
    lista_arquivos = re.findall(r"\((\[.*?\])\)", temp)
    
    # Cria uma lista de dicionários com os dados extraídos
    connection_data = []
    for i in range(len(port_ip)):
        ip, port = port_ip[i]
        files = ast.literal_eval(lista_arquivos[i])
        connection_data.append({
            'ip': ip,
            'port': int(port),
            'files': files
        })
    #Remove dados do proprio peer
    connection_data = [data for data in connection_data if data['ip'] != MY_IP]

    return connection_data

def download_files(client):
    temp = client.recv(SIZE).decode(FORMAT)
    global peers_files
    peers_files = format_list(temp)

    print("Files to download: ")
    for arquivos in peers_files:
        print(arquivos['files'])

    rarest, rarest_ip = rarest_file()
    if(rarest==None):
        print("Não tem arquivo na rede")
    else:
        print(f"Baixar {rarest} do {rarest_ip}")


def select_peer_with_file(file):
    for peer in peers_files:
        if file in peer:
            return peer.split('(')[0]
    return None

def rarest_file():
    rarest = None
    rarest_ip = None
    rarest_count = float('inf')

    for peer in peers_files:
        files = peer['files']
        for file, count in files.items():
            if count < rarest_count:
                rarest = file
                rarest_ip = peer['ip']
                rarest_count = count

    # Verifica se pelo menos um arquivo foi encontrado
    if rarest is not None:
        return rarest, rarest_ip
    else:
        # Retorna o último arquivo percorrido caso não haja um arquivo mais raro
        last_peer = peers_files[-1] if len(peers_files) > 0 else None
        if last_peer is not None:
            files = last_peer['files']
            last_file = list(files.keys())[-1] if len(files) > 0 else None
            if last_file is not None:
                return last_file, last_peer['ip']

    return None, None


def files():
    local = os.path.dirname(os.path.realpath(__file__))

    my_files.clear()
    my_files.append("!FILES!")
    no_files=True
    for file in os.listdir(local):
        if file.endswith(".txt"):
            my_files.append(str(file))
            no_files=False
    if(no_files==True):
        my_files.remove("!FILES!")

def send_files(client):
    while True:
        time.sleep(180)  # Envio a cada 3 minutos
        files()
        client.send(str(my_files).encode(FORMAT))



def main():
    global MY_IP
    MY_IP = input("Type your IP: ")
    
    print("Type Server Adress")
    IP = input("IP: ")
    PORT = int(input("PORT: "))
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    print(f"Connected to {IP}:{PORT}")

    connected = True

    #Coleta arquivos txt pela primeira vez
    files()
    #Envia Arquivos txt para servidor
    client.send(str(my_files).encode(FORMAT))

    thread_send_files = threading.Thread(target=send_files, args=(client,))
    thread_send_files.start()

    while connected:
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        
        if msg == "!baixar":
            download_files(client)

    thread_send_files.join()
    client.close()


if __name__ == "__main__":
    main()
