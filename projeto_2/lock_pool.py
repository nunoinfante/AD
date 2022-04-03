#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - lock_pool.py
Grupo: 50
Números de aluno: 53330, 55411
"""
# Zona para fazer imports
import time

class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as propriedades do recurso para os bloqueios.
        """
        self.state = 'UNLOCKED'
        self.resource_id = resource_id
        self.lock_w_count = 0
        self.lock_r = []
        self.lock_w = []
        self.deadline = 0


    def lock(self, type, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK. O bloqueio pode ser de escrita (type=W)
        ou de leitura (type=R).
        """
        if type == 'W':
            if self.status() == 'UNLOCKED':
                self.state = 'LOCKED-W'
                self.lock_w_count += 1
                self.deadline = time.time() + time_limit
                self.lock_w.append((client_id, self.deadline))
                return True
            else:
                return False
        else:
            if self.status() in ['LOCKED-R', 'UNLOCKED']:
                self.deadline = time.time() + time_limit
                self.lock_r.append((client_id, self.deadline))
                self.state = 'LOCKED-R'
                return True
            else:
                return False


    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.state = 'UNLOCKED'
        self.lock_r = []
        self.lock_w = []
        self.deadline = 0


    def unlock(self, type, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.O desbloqueio pode ser relacionado a bloqueios 
        de escrita (type=W) ou de leitura (type=R), consoante o tipo.
        """
        if type == 'W':
            if self.status() == 'LOCKED-W' and client_id == self.lock_w[0][0]:
                self.lock_w.pop(-1)
                self.state = 'UNLOCKED'
                return True
            else:
                return False
        else:
            r_id = list(map(lambda x : x[0], self.lock_r))
            if self.status() == 'LOCKED-R' and client_id in r_id:
                self.lock_r.pop(r_id.index(client_id))
                if not self.lock_r:
                    self.state = 'UNLOCKED'
                return True
            else:
                return False


    def status(self):
        """
        Obtém o estado do recurso. Retorna LOCKED-W ou LOCKED-R ou UNLOCKED 
        ou DISABLED.
        """
        return self.state


    def stats(self):
        """
        Retorna o número de bloqueios de escrita feitos neste recurso. 
        """
        return self.lock_w_count


    def disable(self):
        """
        Coloca o recurso como desabilitado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.state = 'DISABLED'
        

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = "R" + ' ' + str(self.resource_id) + ' ' + str(self.state) + ' ' + str(self.lock_w_count) + ' '
        if self.status() == 'LOCKED-W':
            output += str(self.lock_w[0][0]) + ' ' + str(round(self.deadline))
        elif self.status() == 'LOCKED-R':
            output += str(len(self.lock_r)) + ' ' + str(round(max(map(lambda x : x[1], self.lock_r))))
        
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
        for i in range(1, N + 1):
            self.recursos.append(resource_lock(i))
        self.K = K


    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        for recurso in self.recursos:
            if recurso.status() in ['LOCKED-W', 'LOCKED-R']:
                if time.time() > recurso.deadline:
                    recurso.release()

    def check_disabled_locks(self):
        """
        Verifica se existem recursos que já atingiram os K bloqueios de escrita permitidos.
        Em caso positivo, desativa esses recursos
        """
        for recurso in self.recursos:
            if recurso.stats() >= self.K:
                recurso.disable()

    def lock(self, type, resource_id, client_id, time_limit):
        """
        Tenta bloquear (do tipo R ou W) o recurso resource_id pelo cliente client_id, 
        durante time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id > len(self.recursos) or resource_id <= 0:
            return None
        for recurso in self.recursos:
            if recurso.resource_id == resource_id:
                return recurso.lock(type, client_id, time_limit)


    def unlock(self, type, resource_id, client_id):
        """
        Liberta o bloqueio (do tipo R ou W) sobre o recurso resource_id pelo cliente 
        client_id. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id > len(self.recursos) or resource_id <= 0:
            return None
        for recurso in self.recursos:
            if recurso.resource_id == resource_id:
                return recurso.unlock(type, client_id)


    def status(self, resource_id):
        """
        Obtém o estado de um recurso. Retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE.
        """
        if resource_id > len(self.recursos) or resource_id <= 0:
            return None
        for recurso in self.recursos:
            if recurso.resource_id == resource_id:
                return recurso.status()


    def stats(self, option, resource_id=0):
        """
        Obtém o estado do serviço de gestão de bloqueios. Se option for K, retorna <número de 
        bloqueios feitos no recurso resource_id> ou UNKNOWN RESOURCE. Se option for N, retorna 
        <número de recursos bloqueados atualmente>. Se option for D, retorna 
        <número de recursos desabilitados>
        """
        if option == 'K':
            if resource_id > len(self.recursos) or resource_id <= 0:
                return None
            for recurso in self.recursos:
                if recurso.resource_id == resource_id:
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
        for recurso in self.recursos:
            output += str(recurso.__repr__()) + ', '
        return output