import pickle

class ListSkeleton:

    def __init__(self):
        self.servicoLista = []

    def processMessage(self, msg_bytes):
        pedido = self.bytesToList(msg_bytes)
        resposta = []
        
        if pedido is None or len(pedido) == 0:
            resposta.append('INVALID MESSAGE')
        else:
            if pedido[0] == 'APPEND' and len(pedido) > 1:
                self.servicoLista.append(pedido[1])
                resposta.append('OK')
            elif pedido[0] == 'LIST':
                resposta = self.servicoLista
            elif pedido[0] == 'CLEAR':
                self.servicoLista = []
                resposta.append('OK')
            else:
                resposta.append('INVALID MESSAGE')
        return self.listToBytes(resposta)
        
    def bytesToList(self, msg_bytes):
        return pickle.loads(msg_bytes)

    def listToBytes(self, msg):
        return pickle.dumps(msg)