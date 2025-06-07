import socket


def create_tcp_server(host='localhost', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (host, port)
    sock.bind(server_address)

    sock.listen(1)

    print(f"Servidor TCP iniciado por {host}:{port}")

    while True:
        connection, client_address = sock.accept()
        try:
            print(f"Conexão de {client_address}")
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Recebido: {data.decode()}")
                connection.sendall(f"ECO DO SERVIDOR TCP: {data}")
        finally:
            connection.close()
            print(f"Conexão fechada pelo cliente: {client_address}")    

def create_udp_server(host='localhost', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (host, port)
    sock.bind(server_address)

    print(f"UDP server iniciado em {host}:{port}")

    while True:
        data, address = sock.recvfrom(1024)
        print(f"Recebeu {data.decode()} de {address}")
        sock.sendto(f"ECO DO SERVIDOR UDP: {data}", address)




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
        create_tcp_server(host, port)
    elif protocol == 'UDP':
        create_udp_server(host, port)
    else:
        print("Protocolo inválido. Escolha TCP ou UDP.")
