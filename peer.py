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

def fetch_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def format_list(temp):
    peers_files.clear

    # Extrai o IP e a porta usando uma expressão regular
    ip_porta = re.findall(r"\('([\d.]+)',\s(\d+)\)", temp)
    # Extrai a lista de arquivos como uma string
    lista_arquivos = re.findall(r"\((\[.*?\])\)", temp)
    
    # Cria uma lista de dicionários com os dados extraídos
    dados_conexao = []
    for i in range(len(ip_porta)):
        ip, porta = ip_porta[i]
        arquivos = ast.literal_eval(lista_arquivos[i])
        dados_conexao.append({
            'ip': ip,
            'port': int(porta),
            'files': arquivos
        })
    #Remove dados do proprio peer
    print("MEU IP: ", MY_IP)
    dados_conexao = [dado for dado in dados_conexao if dado['ip'] != MY_IP]

    return dados_conexao

def download_files(client):
    temp = client.recv(SIZE).decode(FORMAT)
    peers_files = format_list(temp)

    print("Arquivos para baixar: ")
    for arquivos in peers_files:
        print(arquivos['files'])

def select_peer_with_file(file):
    for peer in peers_files:
        if file in peer:
            return peer.split('(')[0]
    return None

def files():
    local = os.path.dirname(os.path.realpath(__file__))

    my_files.clear()
    my_files.append("!FILES!")
    for file in os.listdir(local):
        if file.endswith(".txt"):
            my_files.append(str(file))

def enviar_arquivos_periodicamente(client):
    while True:
        time.sleep(180)  # Envio a cada 3 minutos
        files()
        client.send(str(my_files).encode(FORMAT))

def main():
    global MY_IP
    MY_IP = input("Digite o proprio IP: ")
    print("Meu ip: ", MY_IP)
    if(True):
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

    thread_enviar_arquivos = threading.Thread(target=enviar_arquivos_periodicamente, args=(client,))
    thread_enviar_arquivos.start()

    while connected:
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        
        if msg == "!baixar":
            download_files(client)

    thread_enviar_arquivos.join()
    client.close()


if __name__ == "__main__":
    main()
