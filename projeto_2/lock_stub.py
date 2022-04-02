from net_client import server_connection

class Stub:
    def __init__(self, host, port):
        self.conn_sock = server_connection(host, port)

    def connect(self):
        self.conn_sock.connect()

    def disconnect(self):
        self.conn_sock.close()

    def send_to_server(self, command, *args):
        msg = [command]
        if isinstance(args, list):
            msg.extend(args)
        else:
            msg.append(args)

        return server_connection.send_receive(msg)

    def lock(self, opcao, recurso, tempo, client_id):
        return self.send(10, opcao, recurso, tempo, client_id)

    def unlock(self, opcao, recurso, tempo, client_id):
        return self.send(20, opcao, recurso, tempo, client_id)

    def status(self, recurso):
        return self.send(30, recurso)

    def stats(self, opcao, recurso=None):
        if opcao == 'K':
            return self.send(40, recurso)
        elif opcao == 'N':
            return self.send(50)
        else:
            return self.send(60)

    def print(self):
        return self.send(70)
