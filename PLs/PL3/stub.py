import socket as s
import pickle, struct
import sock_utils

class ListStub:

    def __init__(self, host, port):
        self.conn_sock = None
        self.host = host
        self.port = port

    def connect(self):
        self.conn_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.conn_sock.connect((self.host, self.port))

    def disconnect(self):
        self.conn_sock.close()

    def send(self, command, data=None):
        msg = [command]

        if data:
            if isinstance(data, list):
                msg.append(*data)
            else:
                msg.append(data)

        self.connect()

        #serializa a mensagem
        msg_bytes = pickle.dumps(msg, -1)
        size_bytes = struct.pack('i', len(msg_bytes))

        #envia a mensagem em bytes
        self.conn_sock.sendall(size_bytes)
        self.conn_sock.sendall(msg_bytes)

        #recebe a resposta em bytes
        size_bytes = sock_utils.receive_all(self.conn_sock, 4)
        size = struct.unpack('i', size_bytes)[0]

        #desserializa a resposta
        resposta_bytes = sock_utils.receive_all(self.conn_sock, size)  
        resposta = pickle.loads(resposta_bytes)

        self.disconnect()

        return resposta

    def append(self, element):
        return self.send('APPEND', element)

    def list(self):
        return self.send('LIST')

    def clear(self):
        return self.send('CLEAR')