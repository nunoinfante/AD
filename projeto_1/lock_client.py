#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_client.py
Grupo: 50
Números de aluno: 53330, 55411
"""
# Zona para fazer imports
import sys
import time
from net_client import server_connection

# Programa principal
if len(sys.argv) == 4:
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])

    client_id = sys.argv[1]

    sock = server_connection(HOST, PORT)

    while True:
        comando = input('comando > ')
        comando_split = comando.split()

        print(comando)
            
        if comando_split[0] == 'EXIT':
            if len(comando_split) != 1:
                print('MISSING ARGUMENTS')
            else:
                break

        elif (comando_split[0] == 'LOCK' or comando_split[0] == 'LOCK') and (comando_split[1] == 'R' or comando_split[1] == 'W'):
            if len(comando_split) != 4:
                print('MISSING ARGUMENTS')
            else:
                comando += ' ' + client_id
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))
        
        elif (comando_split[0] == 'UNLOCK' or comando_split[0] == 'UNLOCK') and (comando_split[1] == 'R' or comando_split[1] == 'W'):
            if len(comando_split) != 3:
                print('MISSING ARGUMENTS')
            else:
                comando += ' ' + client_id
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))

        elif comando_split[0] == 'STATUS':
            if len(comando_split) != 2:
                print('MISSING ARGUMENTS')
            else:
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))

        elif comando_split[0] == 'SLEEP':
            if len(comando_split) != 2:
                print('MISSING ARGUMENTS')
            else:
                time.sleep(int(comando_split[1]))

        elif comando_split[0] == 'STATS' and (comando_split[1] == 'N' or comando_split[1] == 'D' or comando_split[1] == 'K'):
            if comando_split[1] == 'K' and len(comando_split) != 3:
                print('MISSING ARGUMENTS')
            elif (comando_split[1] == 'N' or comando_split[1] == 'D') and len(comando_split) != 2:
                print('MISSING ARGUMENTS')
            else:
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))
        
        elif comando_split[0] == 'PRINT':
            if len(comando_split) != 1:
                print('MISSING ARGUMENTS')
            else:
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))
        else:
            print('UNKNOWN COMMAND')

else:
    print('MISSING ARGUMENTS')



