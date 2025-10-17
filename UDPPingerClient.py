import time
from socket import *

# Endereço do servidor
# Se o servidor estiver na mesma máquina, use 'localhost' ou '127.0.0.1'
serverName = 'localhost' 
# A porta que o servidor está escutando
serverPort = 12000

# Criar o socket UDP do cliente
# AF_INET para IPv4, SOCK_DGRAM para UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Definir um tempo limite (timeout) de 1 segundo para o socket
# Se o cliente não receber uma resposta em 1 segundo, ele vai desistir
clientSocket.settimeout(1.0) 

print(f"Pinging {serverName}:{serverPort}...")

# O laboratório pede para enviar 10 pings
for sequence_number in range(1, 11):
    # Pega o tempo atual antes de enviar a mensagem
    start_time = time.time()
    
    # Formata a mensagem de acordo com a especificação do laboratório
    message = f'teste {sequence_number} {start_time}'
    
    try:
        # Envia a mensagem para o servidor.
        # A mensagem precisa ser codificada para bytes antes de ser enviada.
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        
        # Tenta receber a resposta do servidor
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        
        # Pega o tempo atual assim que a resposta é recebida
        end_time = time.time()
        
        # Calcula o RTT (Round-Trip Time)
        rtt = end_time - start_time
        
        # Decodifica a mensagem recebida de bytes para string
        print(f'Reply from {serverAddress[0]}: {modifiedMessage.decode()}')
        print(f'RTT: {rtt:.6f} seconds')
        
    except timeout:
        # Se o socket demorar mais de 1 segundo para receber uma resposta,
        print(f'Ping {sequence_number}: Request timed out')

# Fecha o socket do cliente após o loop terminar
clientSocket.close()