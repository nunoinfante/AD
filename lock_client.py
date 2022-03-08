#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_client.py
Grupo:
Números de aluno:
"""
# Zona para fazer imports
import sys, socket as s
from net_client import server_connection

# Programa principal
if len(sys.argv) == 4:
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])

    clientId = sys.argv[1]

    sock = server_connection(HOST, PORT)

    while True:
        comando = input('comando > ')
        comando_split = comando.replace('-', ' ').split(' ')
        print(comando_split)

        if comando_split[0] == 'EXIT':
            if len(comando_split) != 1:
                print('Sintaxe incorreta')
            else:
                break

        elif (comando_split[0] == 'LOCK' or comando_split[0] == 'UNLOCK') and (comando_split[1] == 'R' or comando_split[1] == 'W'):
            if len(comando_split) != 4:
                print('Sintaxe incorreta')
            else:
                comando += ' ' + clientId
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))
        
        elif comando_split[0] == 'STATUS' or comando_split[0] == 'SLEEP':
            if len(comando_split) != 2:
                print('Sintaxe incorreta')
            else:
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))

        elif comando_split[0] == 'STATS' and (comando_split[1] == 'N' or comando_split[1] == 'D' or comando_split[1] == 'K'):
            if comando_split[1] == 'K' and len(comando_split) != 3:
                print('Sintaxe incorreta')
            elif (comando_split[1] == 'N' or comando_split[1] == 'D') and len(comando_split) != 2:
                print('Sintaxe incorreta')
            else:
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))
        
        elif comando_split[0] == 'PRINT':
            if len(comando_split) != 1:
                print('Sintaxe incorreta')
            else:
                sock.connect()
                resposta = sock.send_receive(comando.encode('utf-8'))
                sock.close()
                print(resposta.decode('utf-8'))
        else:
            print('Comando desconhecido')

else:
    print('Sintaxe incorreta')



