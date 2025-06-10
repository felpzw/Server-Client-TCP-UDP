# Redes de Computadores - TCP & UDP

## Autores

- Felipe Winsch (23102567)
- Thomas Tavares Tomaz (23102571)

## Introdução

Este projeto, elaborado para a disciplina de Rede de Computadores na UFSC, tem como objetivo o desenvolvimento de um programa cliente servidor para comunicação usando os protocolos TCP e UDP.

Foram desenvolvidos dois *scripts* Python para comunicação em rede:

- `Server TCP&UDP.py`: servidor que aceita conexões TCP ou UDP.
- `Client TCP&UDP.py`: cliente que se conecta ao servidor via TCP ou UDP.

## Requisitos

- Python 3.x

## Servidor

Inicialmente, foi desenvoldido um menu simples para seleção do IP, da porta e do protocolo de comunicação do servidor:

```python
if __name__ == "__main__":
    opt = input("Deseja iniciar o servidor como 'localhost'? (SIM/NAO): ").strip().upper()
    if opt == 'NAO' or opt == 'N':
        host = get_local_ip()
    else:
        if opt != 'SIM' and opt != 'S':
            print("Opcao invalida. Atribuido como 'localhost'.")
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
        print("Protocolo invalido. Escolha TCP ou UDP.")
```

Para comunicação via UDP, foi desenvolvida a função `create_udp_server()`:

```python
def create_udp_server(host='localhost', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (host, port)
    sock.bind(server_address)

    print(f"Servidor UDP iniciado em {host}:{port}")

    while True:
        data, address = sock.recvfrom(1024)
        print(f"Recebeu {data.decode()} de {address}")
        sock.sendto(f"ECO DO SERVIDOR UDP: {data}", address)
```

A função acima recebe o endereço IP do host e a porta de rede. Com esses valores, um objeto do tipo `socket` é criado, com os valores: `family = AF_INET` (IPv4) e `type = SOCK_DGRAM` (UDP).

Na sequência, o método `bind()` é chamado, comunicando ao sistema operacional para receber dados no endereço de host e porta específicos (`server_address`).

Por fim, a função entra em um loop para receber os dados e enviar mensagens de eco.

Para comunicação via TCP, foi desenvolvida a função `create_tcp_server()`:

```python
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
                connection.sendall(f"ECO DO SERVIDOR TCP: {data}")
        finally:
            connection.close()
            print(f"Conexão fechada pelo cliente: {client_address}")
```

A função também recebe os mesmos dados que a anterior, mas cria um objeto `socket` com os valores: `family = AF_INET` (IPv4) e `type = SOCK_STREAM` (TCP).

Após chamar o método `bind()` com o endereço do servidor, o método `listen()` define o socket como *listener* e o loop de recepção de dados é iniciado. Dentro do loop, a função aguarda o estabelecimento de uma conexão TCP com um cliente.

Após estabelecimento da conexão, o loop interno garante o recebimento dos dados e o retorno das mensagens de eco.

## Cliente

Para a parte cliente, foi desenvolvido um *script* que permite a conexão e comunicação com um servidor previamente configurado, utilizando os protocolos TCP ou UDP. Inicialmente, é exibido um menu para entrada do IP, da porta do servidor e da escolha do protocolo desejado:

```python
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
```

Caso o protocolo escolhido seja TCP, é chamada a função `connect_to_tcp_server()`:

```python
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
```

Essa função cria um socket TCP (`SOCK_STREAM`) e tenta se conectar ao servidor especificado. Caso a conexão falhe, é retornado `None`.

Se a conexão for bem-sucedida, o cliente entra em um loop de envio de mensagens:

```python
while True:
    message = input("Digite a mensagem para enviar (ou 'sair' para encerrar): ")
    if message.lower() == 'sair':
        break
    elif message.lower().startswith('->'):
        ...  # Envio em lote
    send_tcp_message(client_socket, message)
client_socket.close()
```

A função `send_tcp_message()` é responsável por enviar e receber mensagens:

```python
def send_tcp_message(client_socket, message):
    try:
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        print(f"Servidor respondeu: {response}")
    except socket.timeout:
        print("Timeout: No response from server (1 seconds)")
    except socket.error as e:
        print(f"Socket error: {e}")
```

Caso o protocolo escolhido seja UDP, é chamada a função `connect_to_udp_server()`:

```python
def connect_to_udp_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)
    print("Cliente UDP criado.")
    return client_socket
```

Essa função cria um socket UDP (`SOCK_DGRAM`) com timeout de 1 segundo. Após a criação, é iniciado o loop de envio de mensagens:

```python
while True:
    message = input("Digite a mensagem para enviar (ou 'sair' para encerrar): ")
    if message.lower() == 'sair':
        break
    elif message.lower().startswith('->'):
        ...  # Envio em lote
    send_udp_message(client_socket, message, address)
client_socket.close()
```

A função `send_udp_message()` envia uma mensagem ao servidor e tenta receber a resposta:

```python
def send_udp_message(client_socket, message, address):
    try:
        client_socket.sendto(message.encode(), address)
        data, server = client_socket.recvfrom(1024)
        print(f"Servidor respondeu: {data.decode()}")
    except socket.timeout:
        print("Timeout: No response from server (1 second)")
    except socket.error as e:
        print(f"Socket error: {e}")
```

Tanto no modo TCP quanto no modo UDP, o cliente possui um recurso adicional: ao digitar `->n`, o cliente envia `n` mensagens sequenciais contendo a data e hora atual, com um intervalo de 1 segundo entre cada envio.

## Guia de Utilização

### 1. Inicie o Servidor

No terminal, execute:

```bash
python3 "Server TCP&UDP.py"
```

Você será solicitado a informar:
- A porta do servidor (pressione Enter para usar `12345`)
- O protocolo (`TCP` ou `UDP`)

Exemplo:
```
Deseja iniciar o servidor como 'localhost'? (SIM/NAO): S
Digite a porta do servidor (ou pressione Enter para usar 12345):
Escolha o protocolo (TCP/UDP): TCP
```

### 2. Inicie o Cliente

Em outro terminal, execute:

```bash
python3 "Client TCP&UDP.py"
```

Informe os mesmos dados do servidor:
- Endereço IP do servidor
- Porta do servidor
- Protocolo (`TCP` ou `UDP`)

Exemplo:
```
Digite o endereço IP do servidor (ou pressione Enter para usar 'localhost'):
Digite a porta do servidor (ou pressione Enter para usar 12345):
Escolha o protocolo (TCP/UDP): TCP
```

### 3. Enviando Mensagens

Digite mensagens para enviar ao servidor. Para enviar várias mensagens automaticamente, use o formato `->n`, onde `n` é o número de mensagens.

Exemplo:
```
->5
```
Envia 5 mensagens sequenciais.

Para sair, digite:
```
sair
```

## Observações

- O servidor e o cliente funcionam tanto para TCP quanto para UDP.
- O servidor responde com um eco da mensagem recebida.
- Certifique-se de que a porta escolhida esteja livre e não bloqueada por firewall.

## Possíveis Problemas Corrigidos

- **Conversão de porta:** Nos scripts, ao pressionar Enter para usar o valor padrão da porta, pode ocorrer erro ao converter uma string vazia para inteiro. O código foi ajustado para garantir que o valor padrão seja usado corretamente.

## Referências

- UdpCommunication - Python Wiki. Disponível em: <https://wiki.python.org/moin/UdpCommunication>
- TcpCommunication - Python Wiki. Disponível em: <https://wiki.python.org/moin/TcpCommunication>
- PYTHON. socket — Low-level networking interface — Python 3.8.1 documentation. Disponível em: <https://docs.python.org/3/library/socket.html>
- UNKWNTECH. Finding local IP addresses using Python’s stdlib. Disponível em: <https://stackoverflow.com/a/28950776>
