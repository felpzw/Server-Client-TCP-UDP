import socket
import time

from datetime import datetime


def connect_to_tcp_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(1) 
    try:
        client_socket.connect((host, port))
        print("Connected to server.")
        return client_socket
    except socket.error as e:
        print(f"Connection error: {e}")
        return None
    
def connect_to_udp_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)
    print("Cliente UDP criado.")
    return client_socket

def send_udp_message(client_socket, message, address):
    try:
        client_socket.sendto(message.encode(), address)
        data, server = client_socket.recvfrom(1024)
        print(f"Servidor respondeu: {data.decode()}")
    except socket.timeout:
        print("Timeout: No response from server (1 second)")
    except socket.error as e:
        print(f"Socket error: {e}")

def send_tcp_message(client_socket, message):
    try:
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        print(f"Servidor respondeu: {response}")
    except socket.timeout:
        print("Timeout: No response from server (1 seconds)")
    except socket.error as e:
        print(f"Socket error: {e}")





if __name__ == "__main__":
    
    host = input("Digite o endereço IP do servidor (ou pressione Enter para usar 'localhost'): ")
    if not host:
        host = 'localhost'
    port_input = input("Digite a porta do servidor (ou pressione Enter para usar 12345): ")
    if not port_input:
        port = 12345
    else:
        port = int(port_input)
    protocol = input("Escolha o protocolo (TCP/UDP): ").strip().upper()
    
    if protocol == 'TCP':
        client_socket = connect_to_tcp_server(host, port)
        if client_socket:
            while True:
                message = input("Digite a mensagem para enviar (ou 'sair' para encerrar): ")
                if message.lower() == 'sair':
                    break
                elif message.lower().startswith('->'):
                    try:
                        n = int(message[2:].strip())
                        for i in range(n):
                            msg = f"Mensagem {i+1} enviada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            print(f"Enviando: {msg}")
                            send_tcp_message(client_socket, msg)
                            time.sleep(1)
                            continue
                    except ValueError:
                        print("Formato inválido. Use '->n' onde n é um número inteiro.")
                        continue
                send_tcp_message(client_socket, message)
            client_socket.close()
    elif protocol == 'UDP':
        client_socket = connect_to_udp_server(host, port)
        address = (host, port)
        while True:
            message = input("Digite a mensagem para enviar (ou 'sair' para encerrar): ")
            if message.lower() == 'sair':
                break
            elif message.lower().startswith('->'):
                try:
                    n = int(message[2:].strip())
                    for i in range(n):
                        msg = f"Mensagem {i+1} enviada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        print(f"Enviando: {msg}")
                        send_udp_message(client_socket, msg, address)
                        time.sleep(1)
                        continue
                except ValueError:
                    print("Formato inválido. Use '->n' onde n é um número inteiro.")
                    continue
            send_udp_message(client_socket, message, address)
        client_socket.close()
    else:
        print("Protocolo inválido. Escolha TCP ou UDP.")