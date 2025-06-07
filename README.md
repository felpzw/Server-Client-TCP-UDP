# Redes de Computadores - TCP & UDP

## Autores

- Felipe Winsch (23102567)
- Thomas Tavares Tomaz (23102571)

## Introdução

Este projeto, elaborado para a disciplina de Rede de Computadores na UFSC, tem como objetivo o desenvolvimento de um programa cliente servidor para comunicação usando os protocolos TCP e UDP.

Foram desenvolvidos dois scripts Python para comunicação em rede:

- `Server TCP&UDP.py`: servidor que aceita conexões TCP ou UDP.
- `Client TCP&UDP.py`: cliente que se conecta ao servidor via TCP ou UDP.

## Requisitos

- Python 3.x

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

## Possíveis problemas corrigidos

- **Conversão de porta:** Nos scripts, ao pressionar Enter para usar o valor padrão da porta, pode ocorrer erro ao converter uma string vazia para inteiro. O código foi ajustado para garantir que o valor padrão seja usado corretamente.
