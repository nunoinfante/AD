import socket as s

HOST = '127.0.0.1'
PORT = 9999

sock = s.socket(s.AF_INET, s.SOCK_STREAM)

sock.connect((HOST, PORT))

sock.sendall(b'Vamos aprender isto!')
resposta = sock.recv(1024)

print('Recebi %s' % resposta)

sock.close()
