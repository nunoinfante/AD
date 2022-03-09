import socket as s
import sys, sock_utils

if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = '127.0.0.1'
    PORT = 9999

while True:
    sock = sock_utils.create_tcp_client_socket(HOST, PORT)
    msg = input('comando > ')

    if msg == 'EXIT':
        break

    sock.sendall(msg.encode('utf-8'))
    resposta = sock_utils.receive_all(sock, 1024)
    print(resposta.decode('utf-8'))
sock.close()
