#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - lock_server.py
Grupo:
Números de aluno:
"""

# Zona para fazer importação
from itertools import count
import pickle, struct
import sys, sock_utils, time

###############################################################################

class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as propriedades do recurso para os bloqueios.
        """
        self.id = resource_id
        self.estado = 'UNLOCKED'
        self.contador = 0
        self.blockEscrita = []
        self.blockLeitura = []
        self.clienteId = None
        self.deadline = 0


    def lock(self, type, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK. O bloqueio pode ser de escrita (type=W)
        ou de leitura (type=R).
        """
        if type == 'W':
            if self.status() == 'UNLOCKED':
                self.estado = 'LOCKED-W'
                self.contador += 1
                self.clienteId = client_id
                self.deadline = time.time() + time_limit
                self.blockEscrita.append((client_id, self.deadline))
                return 'OK'
            else:
                return 'NOK'
        else:
            if self.status() == 'LOCKED-R' or self.status() == 'UNLOCKED':
                self.deadline = time.time() + time_limit
                self.blockLeitura.append((client_id, self.deadline))
                self.estado = 'LOCKED-R'
                return 'OK'
            else:
                return 'NOK'
                

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.estado = 'UNLOCKED'
        self.contador = 0
        self.blockEscrita = []
        self.blockLeitura = []
        self.deadline = 0

    def unlock(self, type, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.O desbloqueio pode ser relacionado a bloqueios 
        de escrita (type=W) ou de leitura (type=R), consoante o tipo.
        """
        if type == 'W':
            if self.status() == 'LOCKED-W' and self.clienteId == client_id:
                self.blockEscrita = [(id, deadline) for (id, deadline) in self.blockEscrita if id != client_id]
                self.estado = 'UNLOCKED'
                return 'OK'
            elif self.status() == 'UNLOCKED' or self.status() == 'DISABLED' or self.clienteId != client_id:
                return 'NOK'
        else:
            if self.status() == 'LOCKED-R' and self.clienteId == client_id:
                self.blockLeitura = [(id, deadline) for (id, deadline) in self.blockLeitura if id != client_id]
                self.estado = 'UNLOCKED'
                return 'OK'
            elif self.status() == 'UNLOCKED' or self.status() == 'DISABLED':
                return 'NOK'


    def status(self):
        """
        Obtém o estado do recurso. Retorna LOCKED-W ou LOCKED-R ou UNLOCKED 
        ou DISABLED.
        """
        return self.estado

    def stats(self):
        """
        Retorna o número de bloqueios de escrita feitos neste recurso. 
        """
        return self.contador
   
    def disable(self):
        """
        Coloca o recurso como desabilitado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.estado = 'DISABLED'

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        # Se o recurso está bloqueado para a escrita:
        # R <num do recurso> LOCKED-W <vezes bloqueios de escrita> <id do cliente> <deadline do bloqueio de escrita>
        # Se o recurso está bloqueado para a leitura:
        # R <num do recurso> LOCKED-R <vezes bloqueios de escrita> <num bloqueios de leitura atuais> <último deadline dos bloqueios de leitura>
        # Se o recurso está desbloqueado:
        # R <num do recurso> UNLOCKED
        # Se o recurso está inativo:
        # R <num do recurso> DISABLED

        return output

###############################################################################

class lock_pool:
    def __init__(self, N, K):
        """
        Define um array com um conjunto de resource_locks para N recursos. 
        Os locks podem ser manipulados pelos métodos desta classe. 
        Define K, o número máximo de bloqueios de escrita permitidos para cada 
        recurso. Ao atingir K bloqueios de escrita, o recurso fica desabilitado.
        """
        self.recursos = []
        for i in range(N):
            self.recursos.append(resource_lock(i))
        self.K = K

    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        for recurso in self.recursos:
            if recurso.status(recurso.id) == 'LOCKED-W' or recurso.status(recurso.id) == 'LOCKED-R':
                if time.time() > recurso.deadline:
                    recurso.release()

    def lock(self, type, resource_id, client_id, time_limit):
        """
        Tenta bloquear (do tipo R ou W) o recurso resource_id pelo cliente client_id, 
        durante time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id >= len(self.recursos) or resource_id < 0:
            return 'UNKNOWN RESOURCE'
        for recurso in self.recursos:
            if recurso.id == resource_id:
                return recurso.lock(type, client_id, time_limit)

    def unlock(self, type, resource_id, client_id):
        """
        Liberta o bloqueio (do tipo R ou W) sobre o recurso resource_id pelo cliente 
        client_id. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id >= len(self.recursos) or resource_id < 0:
            return 'UNKNOWN RESOURCE'
        for recurso in self.recursos:
            if recurso.id == resource_id:
                return recurso.unlock(type, client_id)

    def status(self, resource_id):
        """
        Obtém o estado de um recurso. Retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE.
        """
        if resource_id >= len(self.recursos) or resource_id < 0:
            return 'UNKNOWN RESOURCE'
        for recurso in self.recursos:
            if recurso.id == resource_id:
                return recurso.status()

    #FIX UNKNOWN RESOURCE OPTION K
    def stats(self, option, resource_id=0):
        """
        Obtém o estado do serviço de gestão de bloqueios. Se option for K, retorna <número de 
        bloqueios feitos no recurso resource_id> ou UNKNOWN RESOURCE. Se option for N, retorna 
        <número de recursos bloqueados atualmente>. Se option for D, retorna 
        <número de recursos desabilitados>
        """
        if option == 'K':
            if resource_id >= len(self.recursos) or resource_id < 0:
                return 'UNKNOWN RESOURCE'
            for recurso in self.recursos:
                if recurso.id == resource_id:
                    return recurso.stats()
        elif option == 'N':
            counter = 0
            for recurso in self.recursos:
                if recurso.status() == 'UNLOCKED':
                    counter += 1
            return counter
        else:
            counter = 0
            for recurso in self.recursos:
                if recurso.status() == 'DISABLED':
                    counter += 1
            return counter

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        #
        # Acrescentar no output uma linha por cada recurso
        #
        return output

###############################################################################

# código do programa principal

if len(sys.argv) == 5:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    lock_pool = lock_pool(int(sys.argv[3]), int(sys.argv[4]))

sock = sock_utils.create_tcp_server_socket(HOST, PORT, 1)


while True:
    (conn_sock, (addr, port)) = sock.accept()
    
    size_bytes = sock_utils.receive_all(conn_sock, 4)
    size = struct.unpack('i', size_bytes)[0]

    msg_bytes = conn_sock.recv(size)
    msg = pickle.loads(msg_bytes)

    print(msg)

    if msg[0] == 'LOCK':
        resp = lock_pool.lock((msg[1]), int(msg[2]), int(msg[4]), int(msg[3]))
    elif msg[0] == 'UNLOCK':
        resp = lock_pool.unlock(msg[1], int(msg[2]), int(msg[3]))
    elif msg[0] == 'STATUS':
        resp = lock_pool.status(int(msg[1]))
    elif msg[0] == 'STATS' and msg[1] == 'K':
        resp = lock_pool.stats(msg[1], int(msg[2]))
    elif msg[0] == 'STATS' and (msg[1] == 'N' or msg[1] == 'D'):
        resp = lock_pool.stats(msg[1])




    msg_bytes = pickle.dumps(resp, -1)
    size_bytes = struct.pack('i', len(msg_bytes))

    conn_sock.sendall(size_bytes)
    conn_sock.sendall(msg_bytes)
