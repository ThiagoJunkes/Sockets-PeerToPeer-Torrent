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

    count = 1
    while True or count < 4:
        files()
        files_to_download = get_files_to_download()

        if not files_to_download:
            print("No files to download.")
            break

        print("Files to download:")
        for file, info in files_to_download.items():
            if info[1]:  # Verifica se o arquivo está disponível para download
                print(f"File: {file}, Rarity: {info[0]}")

        rarest_file = get_rarest_file(files_to_download)
        if rarest_file is None:
            print("No rarest file found.")
            break

        print(f"Downloading {rarest_file}")
        # Implementar lógica para baixar o arquivo "rarest_file" do peer adequado
        count=+1

def get_rarest_file(files_to_download):
    rarest_file = next(iter(files_to_download))  # Define o primeiro arquivo como o mais raro
    rarity_count = float('inf')

    for file, info in files_to_download.items():
        if info[1] and info[0] < rarity_count:  # Verifica se o arquivo está disponível e tem menor contagem de raridade
            rarest_file = file
            rarity_count = info[0]

    return rarest_file


    
def get_files_to_download():
    files_info = {}

    for peer in peers_files:
        for file in peer['files']:
            if file not in my_files:
                if file in files_info:
                    # O arquivo já está na estrutura, incrementa a contagem de raridade
                    files_info[file][0] += 1
                else:
                    # O arquivo é novo, adiciona à estrutura
                    files_info[file] = [1, True]

    return files_info


def select_peer_with_file(file):
    for peer in peers_files:
        if file in peer:
            return peer.split('(')[0]
    return None

def files():
    local = os.path.dirname(os.path.realpath(__file__))

    global my_files
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
