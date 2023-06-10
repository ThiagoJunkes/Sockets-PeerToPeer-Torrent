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

    print("Files to download:")
    files_to_download = []
    for peer in peers_files:
        for file in peer['files']:
            if file not in my_files and file not in files_to_download:
                files_to_download.append(file)
    print(files_to_download)

    files_rarity = []
    for peer in peers_files:
        for file in peer['files']:
            found = False
            for item in files_rarity:
                if item['file'] == file:
                    item['count'] += 1
                    found = True
                    break
            if not found:
                files_rarity.append({'file': file, 'count': 1})

    print(files_rarity)



    rarest = rarest_file()
    if(rarest==None):
        print("Não tem arquivo mais raro")
    else:
        print(f"Baixar {rarest}")
    


def select_peer_with_file(file):
    for peer in peers_files:
        if file in peer:
            return peer.split('(')[0]
    return None

def rarest_file():
    if not peers_files:
        return None

    # Cria um dicionário para armazenar a contagem de cada arquivo
    file_count = {}

    # Itera sobre cada peer na lista de peers_files
    for peer in peers_files:
        files = peer['files']

        # Itera sobre cada arquivo no peer
        for file in files:
            # Incrementa a contagem do arquivo
            file_count[file] = file_count.get(file, 0) + 1

    # Ordena os arquivos com base na contagem (do menos comum para o mais comum)
    sorted_files = sorted(file_count.items(), key=lambda x: x[1])

    # Retorna o arquivo menos comum (mais raro)
    return sorted_files[0][0] if sorted_files else None


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
