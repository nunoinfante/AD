#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_server.py
Grupo: 50
Números de aluno: 53330, 55411
"""

# Zona para fazer importação
import sys, sock_utils, struct, pickle, select as sel
from lock_skel import lock_skel

###############################################################################

# código do programa principal

if len(sys.argv) == 5:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    skel = lock_skel(int(sys.argv[3]), int(sys.argv[4]))

sock = sock_utils.create_tcp_server_socket(HOST, PORT, 1)
socket_list = [sock, sys.stdin]

while True:
    try:
        R, W, X = sel.select(socket_list, [], [])
        for sckt in R:
            if sckt is sock:
                conn_sock, addr = sckt.accept()
                addr, port = conn_sock.getpeername()
                print('Novo cliente ligado desde %s:%d' % (addr, port))
                socket_list.append(conn_sock)
            elif sckt is sys.stdin:
                msg = sckt.readline().strip()
                if msg == "EXIT":
                    exit()
            else:
                size_bytes = sock_utils.receive_all(sckt, 4)
                if size_bytes is not None:
                    size = struct.unpack('i', size_bytes)[0]
                    msg_split = sock_utils.receive_all(sckt, size)
                    
                    send_msg = skel.process_msg(msg_split)
                    
                    send_size = struct.pack('i', len(send_msg))
                    sckt.sendall(send_size)
                    sckt.sendall(send_msg)

    except KeyboardInterrupt:
        break
    except ValueError:
        resp = "INVALID ARGUMENTS"
        conn_sock.sendall(resp.encode('utf-8'))