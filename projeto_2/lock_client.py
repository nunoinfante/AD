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
from lock_stub import Stub

# Programa principal
if len(sys.argv) == 4:
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])

    client_id = sys.argv[1]

    stub = Stub(HOST, PORT)

    stub.connect()

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
                resposta = stub.lock(comando_split[1], comando_split[2], comando_split[3], client_id)
        
        elif (comando_split[0] == 'UNLOCK' or comando_split[0] == 'UNLOCK') and (comando_split[1] == 'R' or comando_split[1] == 'W'):
            if len(comando_split) != 3:
                print('MISSING ARGUMENTS')
            else:
                resposta = stub.unlock(comando_split[1], comando_split[2], comando_split[3], client_id)

        elif comando_split[0] == 'STATUS':
            if len(comando_split) != 2:
                print('MISSING ARGUMENTS')
            else:
                resposta = stub.status(comando_split[1])

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
                if comando_split[1] == 'K':
                    resposta = stub.stats(comando_split[1], comando_split[2])
                else:
                    resposta = stub.stats(comando_split[1])

        elif comando_split[0] == 'PRINT':
            if len(comando_split) != 1:
                print('MISSING ARGUMENTS')
            else:
                resposta = stub.print()
        else:
            print('UNKNOWN COMMAND')
else:
    print('MISSING ARGUMENTS')

stub.disconnect()

