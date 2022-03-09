#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_client.py
Grupo:
Números de aluno:
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
        comando = comando.replace('-', ' ').split()

        if comando[0] == 'EXIT':
            if len(comando) != 1:
                print('Sintaxe incorreta')
            else:
                break

        elif (comando[0] == 'LOCK') and (comando[1] == 'R' or comando[1] == 'W'):
            if len(comando) != 4:
                print('Sintaxe incorreta')
            else:
                comando.append(client_id)
                sock.connect()
                resposta = sock.send_receive(comando)
                sock.close()
                print(resposta)
        
        elif (comando[0] == 'UNLOCK') and (comando[1] == 'R' or comando[1] == 'W'):
            if len(comando) != 3:
                print('Sintaxe incorreta')
            else:
                comando.append(client_id)
                sock.connect()
                resposta = sock.send_receive(comando)
                sock.close()
                print(resposta)

        elif comando[0] == 'STATUS':
            if len(comando) != 2:
                print('Sintaxe incorreta')
            else:
                sock.connect()
                resposta = sock.send_receive(comando)
                sock.close()
                print(resposta)

        elif comando[0] == 'SLEEP':
            if len(comando) != 2:
                print('Sintaxe incorreta')
            else:
                time.sleep(int(comando[1]))

        elif comando[0] == 'STATS' and (comando[1] == 'N' or comando[1] == 'D' or comando[1] == 'K'):
            if comando[1] == 'K' and len(comando) != 3:
                print('Sintaxe incorreta')
            elif (comando[1] == 'N' or comando[1] == 'D') and len(comando) != 2:
                print('Sintaxe incorreta')
            else:
                sock.connect()
                resposta = sock.send_receive(comando)
                sock.close()
                print(resposta)
        
        elif comando[0] == 'PRINT':
            if len(comando) != 1:
                print('Sintaxe incorreta')
            else:
                sock.connect()
                resposta = sock.send_receive(comando)
                sock.close()
                print(resposta)
        else:
            print('Comando desconhecido')

else:
    print('Sintaxe incorreta')



