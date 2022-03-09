import socket as s
import sys, sock_utils

if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = '127.0.0.1'
    PORT = 9999

sock = sock_utils.create_tcp_server_socket(HOST, PORT, 1)
dict = {}
i = 0
res = ''
while True:

    (conn_sock, (addr, port)) = sock.accept()
    msg = sock_utils.receive_all(conn_sock, 1024)
    msg_split = msg.decode('utf-8').split(' ')

    if msg_split[0] == 'ADD':
        dict[i] = msg_split[1]
        i += 1
        conn_sock.sendall(b'OK')
    elif msg_split[0] == 'LIST':
        res = ''
        for string in dict.values():
            res += string + ', '
        conn_sock.sendall(res[:-2].encode('utf-8'))
    elif msg_split[0] == 'GET':
        conn_sock.sendall(dict[int(msg_split[1])].encode('utf-8'))
    elif msg_split[0] == 'REMOVE':
        dict.pop(int(msg_split[1]))
        print(dict)
        conn_sock.sendall(b'OK')
    else:
        conn_sock.sendall(b'Comando desconhecido')
    conn_sock.close()
