#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_client.py
Grupo: 50
Números de aluno: 53330, 55411
"""
# Zona para fazer imports
import sys
import time
from lock_stub import lock_stub

# Programa principal
if len(sys.argv) == 4:
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])

    client_id = sys.argv[1]

    stub = lock_stub(HOST, PORT)

    stub.connect()

    while True:
        try:
            comando = input('comando > ')
            comando_split = comando.split()
            
            if len(comando_split) != 0:   
                if comando_split[0] == 'EXIT':
                    if len(comando_split) != 1:
                        print('MISSING ARGUMENTS')
                    else:
                        exit()

                elif comando_split[0] == 'LOCK' and (comando_split[1] == 'R' or comando_split[1] == 'W'):
                    if len(comando_split) != 4:
                        print('MISSING ARGUMENTS')
                    else:
                        resposta = stub.lock(comando_split[1], comando_split[2], comando_split[3], client_id)
                        print(resposta)

                elif comando_split[0] == 'UNLOCK' and (comando_split[1] == 'R' or comando_split[1] == 'W'):
                    if len(comando_split) != 3:
                        print('MISSING ARGUMENTS')
                    else:
                        resposta = stub.unlock(comando_split[1], comando_split[2], client_id)
                        print(resposta)

                elif comando_split[0] == 'STATUS':
                    if len(comando_split) != 2:
                        print('MISSING ARGUMENTS')
                    else:
                        resposta = stub.status(comando_split[1])
                        print(resposta)

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
                            print(resposta)
                        else:
                            resposta = stub.stats(comando_split[1])
                            print(resposta)

                elif comando_split[0] == 'PRINT':
                    if len(comando_split) != 1:
                        print('MISSING ARGUMENTS')
                    else:
                        resposta = stub.print()
                        print(resposta)
                else:
                    print('UNKNOWN COMMAND')

        except KeyboardInterrupt:
            break
    stub.disconnect()
else:
    print('MISSING ARGUMENTS')