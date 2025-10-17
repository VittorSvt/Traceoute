import socket
import time

def main():
    # Endereço e porta do servidor
    # 'localhost' (ou '127.0.0.1')
    server_host = '127.0.0.1'
    server_port = 12000
    
    # Tempo limite de espera pela resposta (S)
    timeout_seconds = 1.0

    print(f"Iniciando 10 pings para {server_host}:{server_port}...")

    # Criar um socket UDP
    # AF_INET indica que estamos usando IPv4
    # SOCK_DGRAM indica que é um socket UDP (Datagram)
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Definir o tempo limite do socket
        # Se o socket esperar mais que 1.0 segundo por uma resposta,
        # ele levantará uma exceção socket.timeout
        client_socket.settimeout(timeout_seconds)

    except socket.error as e:
        print(f"Erro ao criar o socket: {e}")
        return

    # Loop para enviar 10 mensagens de ping
    for sequence_number in range(1, 11):
        
        # Registrar o tempo de envio (timestamp)
        start_time = time.time()
        
        # Formatar a mensagem conforme especificado
        message = f"Ping {sequence_number} {start_time}"
        
        try:
            # Enviar a mensagem para o servidor
            # .encode() converte a string em bytes, que é o formato
            # que a rede entende
            client_socket.sendto(message.encode(), (server_host, server_port))
            
            # Tentar receber a resposta do servidor
            # O buffer de 1024 bytes é o tamanho máximo da mensagem que esperamos
            response, server_address = client_socket.recvfrom(1024)
            
            # Registrar o tempo de recebimento
            end_time = time.time()
            
            # Calcular o Tempo de Ida e Volta (RTT)
            rtt = end_time - start_time
            
            # Imprimir a resposta (decodificada de bytes para string) e o RTT
            print(f"Recebido: {response.decode()} | RTT: {rtt:.6f} segundos")

        except socket.timeout:
            # A exceção socket.timeout foi levantada porque 1 segundo se passou
            # sem nenhuma resposta do servidor
            print(f"Ping {sequence_number}: Request timed out")
        
        except socket.error as e:
            # Outros erros de socket (ex: servidor não está rodando)
            print(f"Erro no Ping {sequence_number}: {e}")

    # Fechar o socket após o loop
    client_socket.close()
    print("Ping finalizado.")

if __name__ == '__main__':
    main()