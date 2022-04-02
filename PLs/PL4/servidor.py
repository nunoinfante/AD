import sys, socket as s
import select

HOST = 'localhost'
if len(sys.argv) > 1:
	PORT = int(sys.argv[1])
else:
	PORT = 9999

listen_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
listen_sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
listen_sock.bind((HOST, PORT))
listen_sock.listen(1)

socket_list = [listen_sock, sys.stdin]
lista = []

while True:
	try:
		R, W, X = select.select(socket_list, [], [])
		for sckt in R:
			if sckt is sys.stdin:
				msg = sys.stdin.readline().strip()
				if msg == 'EXIT':
					raise SystemExit()
			elif sckt is listen_sock:
				conn_sock, addr = listen_sock.accept()
				addr, port = conn_sock.getpeername()
				print(f'Novo cliente ligado por {addr}:{port}')
				socket_list.append(conn_sock)
			else:
				msg = sckt.recv(1024)
				decoded = msg.decode('utf-8')

				if decoded:
					resp = 'Ack'

					if decoded == 'LIST':
						resp = str(lista)
					elif decoded == 'CLEAR':
						lista = []
						resp = 'Lista apagada'
					elif decoded == 'CLIENTS':
						resp = socket_list
					else:
						lista.append(decoded)
					sckt.sendall(resp.encode('utf-8'))
				else:
					sckt.close()
					socket_list.remove(sckt)
					print('Cliente fechou ligação')
					
	except (KeyboardInterrupt, SystemExit):
		break
	except:
		print(sys.exc_info())
		conn_sock.close()

listen_sock.close()

