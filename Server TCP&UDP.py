import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa ser alcançavel
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = 'localhost'
    finally:
        s.close()
    return IP

def create_tcp_server(host='localhost', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (host, port)
    sock.bind(server_address)

    sock.listen(1)

    print(f"Servidor TCP iniciado em {host}:{port}")

    while True:
        connection, client_address = sock.accept()
        try:
            print(f"Conexão de {client_address}")
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Recebido: {data.decode()}")
                connection.sendall(f"ECO DO SERVIDOR TCP: {data.decode()}".encode())
        finally:
            connection.close()
            print(f"Conexão fechada pelo cliente: {client_address}")    

def create_udp_server(host='localhost', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (host, port)
    sock.bind(server_address)

    print(f"Servidor UDP iniciado em {host}:{port}")

    while True:
        data, address = sock.recvfrom(1024)
        print(f"Recebeu {data.decode()} de {address}")
        sock.sendto(f"ECO DO SERVIDOR UDP: {data.decode()}".encode(), address)

if __name__ == "__main__":
    opt = input("Deseja iniciar o servidor como 'localhost'? (SIM/NAO): ").strip().upper()
    if opt == 'NAO' or opt == 'N':
        host = get_local_ip()
    else:
        if opt != 'SIM' and opt != 'S':
            print("Opcao invalida. Atribuido como 'localhost'.")
        host = 'localhost'
    while True:
        port_input = input("Digite a porta do servidor (ou pressione Enter para usar 12345): ")
        if not port_input:
            port = 12345
            break
        try:
            port = int(port_input)
            break
        except ValueError:
            print("Porta inválida. Digite um número inteiro ou pressione Enter para o padrão.")
    protocol = input("Escolha o protocolo (TCP/UDP): ").strip().upper()
    if protocol == 'TCP':
        create_tcp_server(host, port)
    elif protocol == 'UDP':
        create_udp_server(host, port)
    else:
        print("Protocolo invalido. Escolha TCP ou UDP.")
