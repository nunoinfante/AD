import sys, socket as s 
import socketserver 

HOST = 'localhost' 
if len(sys.argv) > 1: 
  PORT = int(sys.argv[1]) 
else: 
  PORT = 9999 
 
lista = [] 
 
class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        print('ligado a ', self.client_address)
        
        decoded = data.decode('utf-8')
        resp = 'Ack'
        if decoded == 'LIST':
            resp = str(lista)
        elif decoded == 'CLEAR':
            lista.clear()
            resp = 'Lista apagada'
        else:
            lista.append(decoded)

        self.request.sendall(resp.encode('utf-8'))

server = socketserver.ThreadingTCPServer((HOST, PORT), MyHandler)
server.serve_forever(2.0)