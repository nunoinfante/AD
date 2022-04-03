#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_stub.py
Grupo: 50
Números de aluno: 53330, 55411
"""
# Zona para fazer imports
from net_client import server_connection

class lock_stub:
    def __init__(self, host, port):
        self.conn_sock = server_connection(host, port)

    def connect(self):
        self.conn_sock.connect()

    def disconnect(self):
        self.conn_sock.close()

    def lock(self, opcao, recurso, tempo, client_id):
        return self.send_to_server(10, opcao, recurso, tempo, client_id)

    def unlock(self, opcao, recurso, client_id):
        return self.send_to_server(20, opcao, recurso, client_id)

    def status(self, recurso):
        return self.send_to_server(30, recurso)

    def stats(self, opcao, recurso=None):
        if opcao == 'K':
            return self.send_to_server(40, recurso)
        elif opcao == 'N':
            return self.send_to_server(50)
        else:
            return self.send_to_server(60)

    def print(self):
        return self.send_to_server(70)

    def send_to_server(self, command, *args):
        msg = [command]
        msg.extend(args)

        resposta =  self.conn_sock.send_receive(msg)
    
        return resposta
