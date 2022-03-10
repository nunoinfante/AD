import socket as s, pickle, struct

#listener_socket = create_tcp_server_socket(address, port, queue_size)
def create_tcp_server_socket(address, port, queue_size):
    listener_socket = s.socket(s.AF_INET, s.SOCK_STREAM) 
    listener_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1) 
    listener_socket.bind((address, port)) 
    listener_socket.listen(queue_size)
    return listener_socket

#client_socket = create_tcp_client_socket(address, port)
def create_tcp_client_socket(address, port):
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM) 
    client_socket.connect((address, port))
    return client_socket

#dados_recebidos = receive_all(socket, length)
def receive_all(socket, length):
	dados_recebidos = socket.recv(length)
	return dados_recebidos

