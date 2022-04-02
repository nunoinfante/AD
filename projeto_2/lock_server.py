#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_server.py
Grupo: 50
Números de aluno: 53330, 55411
"""

# Zona para fazer importação
import sys, sock_utils, time
import lock_pool
###############################################################################

# código do programa principal

if len(sys.argv) == 5:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    lock_pool = lock_pool(int(sys.argv[3]), int(sys.argv[4]))

sock = sock_utils.create_tcp_server_socket(HOST, PORT, 1)

while True:
    try:
        (conn_sock, (addr, port)) = sock.accept()

        print('Ligado a: %s no porto %s' % (addr, port))

        lock_pool.clear_expired_locks()
        lock_pool.check_disabled_locks()

        msg = sock_utils.receive_all(conn_sock, 1024)
        msg = msg.decode('utf-8')
        msg_split = msg.replace('-', ' ', 1).split()

        if msg_split[0] == 'LOCK':
            resp = lock_pool.lock((msg_split[1]), int(msg_split[2]), int(msg_split[4]), int(msg_split[3]))
        elif msg_split[0] == 'UNLOCK':
            resp = lock_pool.unlock(msg_split[1], int(msg_split[2]), int(msg_split[3]))
        elif msg_split[0] == 'STATUS':
            resp = lock_pool.status(int(msg_split[1]))
        elif msg_split[0] == 'STATS' and msg_split[1] == 'K':
            resp = lock_pool.stats(msg_split[1], int(msg_split[2]))
        elif msg_split[0] == 'STATS' and (msg_split[1] == 'N' or msg_split[1] == 'D'):
            resp = lock_pool.stats(msg_split[1])
        elif msg_split[0] == 'PRINT':
            resp = lock_pool.__repr__()

        print(msg)
        print(resp)

        conn_sock.sendall(str(resp).encode('utf-8'))

    except ValueError:
        resp = "INVALID ARGUMENTS"
        conn_sock.sendall(resp.encode('utf-8'))