#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_skel.py
Grupo: 50
Números de aluno: 53330, 55411
"""
# Zona para fazer imports
import pickle
from lock_pool import lock_pool

class lock_skel:

    def __init__(self, N, K):
        self.pool = lock_pool(N, K)
    
    def process_msg(self, msg_bytes):
        pedido = self.bytesToList(msg_bytes)
        resposta = []

        if pedido == None or len(pedido) == 0 :
            resposta.append('INVALID MESSAGE')
        else:
            self.pool.clear_expired_locks()
            self.pool.check_disabled_locks()

            if pedido[0] == 10:
                resposta.append(11)
                resposta.append(self.pool.lock(pedido[1], int(pedido[2]), int(pedido[4]), int(pedido[3])))
            
            elif pedido[0] == 20:
                resposta.append(21)
                resposta.append(self.pool.unlock(pedido[1], int(pedido[2]), int(pedido[3])))
            
            elif pedido[0] == 30:
                resposta.append(31)
                resposta.append(self.pool.status(int(pedido[1])))
            
            elif pedido[0] == 40:
                resposta.append(41)
                resposta.append(self.pool.stats('K', int(pedido[1])))
            
            elif pedido[0] == 50:
                resposta.append(51)
                resposta.append(self.pool.stats('N'))

            elif pedido[0] == 60:
                resposta.append(61)
                resposta.append(self.pool.stats('D'))
            
            elif pedido[0] == 70:
                resposta.append(71)
                resposta.append(self.pool.__repr__())
            
            else:
                resposta.append('Erro')
                
        print(resposta)
        return self.listToBytes(resposta)

    def bytesToList(self, msg_bytes):
        return pickle.loads(msg_bytes)

    def listToBytes(self, resposta):
        return pickle.dumps(resposta)