import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print("Certo: ",get_ip_address())

print("Errado: ",socket.gethostbyname(socket.gethostname()))