import socket
import os
import threading
import time
import re
import ast


PORT = 50550
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!sair"
global MY_IP

peers_files = []
my_files = []


def format_list(temp):
    peers_files.clear()

    # Extrai o IP usando uma expressão regular
    ip = re.findall(r"([\d.]+)\(", temp)

    # Extrai a lista de arquivos como uma string
    lista_arquivos = re.findall(r"\(\s*\[(.*?)\]\)", temp)

    # Cria uma lista de dicionários com os dados extraídos
    connection_data = []
    for i in range(len(ip)):
        files = [file.strip().strip('\'"') for file in lista_arquivos[i].split(",")]
        connection_data.append({
            'ip': ip[i],
            'files': files
        })

    # Remove dados do próprio peer
    connection_data = [data for data in connection_data if data['ip'] != MY_IP]

    return connection_data




def download_files(client):
    temp = client.recv(SIZE).decode(FORMAT)
    global peers_files
    peers_files = format_list(str(temp))

    while True:
        files()
        #Manda lista de arquivos atuais para o servidor
        client.send(str(my_files).encode(FORMAT))
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
        peer_ip = select_peer_with_file(rarest_file)
        if(peer_ip == None):
            print(f"Impossible to download {rarest_file} from {peer_ip}")
        else:
            try:
                peer_connected = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_connected.connect((peer_ip, PORT))
            
                print(f"Connected to {peer_ip}:{PORT}")
                #Envia Arquivos txt que precisa ser baixado
                peer_connected.send(str(rarest_file).encode(FORMAT))

                #Recebe conteudo do arquivo
                content = peer_connected.recv(SIZE).decode(FORMAT)
                with open(rarest_file, "x") as f:
                    f.write(content)
            except Exception:
                print("Peer not found or connection refused, try again in a few minutes!")
                break


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
        if file in peer['files']:
            return peer['ip']
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
        files()
        client.send(str(my_files).encode(FORMAT))
        time.sleep(180)  # Envio a cada 3 minutos

def handle_peer(conn, addr):
    print(f"Peer {addr} connected")

    connected = True
    while connected:
        file = conn.recv(SIZE).decode(FORMAT)
        with open(file, "r") as f:
            conteudo = f.read()

        conn.send((f"{conteudo}").encode(FORMAT))
        connected = False

    print("Connection closed")
    conn.close()

def reciving_connection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((MY_IP, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        thread_peer = threading.Thread(target=handle_peer, args=(conn, addr))
        thread_peer.start()

def main():
    global MY_IP
    MY_IP = input("Type your IP: ")
    
    print("Type Server Adress")
    IP = input("IP: ")
    SERVER_PORT = int(input("PORT: "))
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, SERVER_PORT))
    print(f"Connected to {IP}:{SERVER_PORT}")

    connected = True

    #Coleta arquivos txt pela primeira vez
    files()
    #Envia Arquivos txt para servidor
    client.send(str(my_files).encode(FORMAT))

    thread_send_files = threading.Thread(target=send_files, args=(client,))
    thread_send_files.start()

    thread_peer_connection = threading.Thread(target=reciving_connection)
    thread_peer_connection.start()

    while connected:
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
            break
        
        if msg == "!baixar":
            download_files(client)

    thread_send_files.join()
    client.close()


if __name__ == "__main__":
    main()