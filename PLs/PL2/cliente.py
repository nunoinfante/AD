from copyreg import pickle
import sys, sock_utils
import pickle, struct
 
if len(sys.argv) > 1:    
    HOST = sys.argv[1]    
    PORT = int(sys.argv[2])  
else:    
    HOST = '127.0.0.1'    
    PORT = 9999   
 
while True:    
    msg = str(input('Mensagem: '));     
    if msg == 'EXIT':     
        break    
     
    conn_sock = sock_utils.create_tcp_client_socket(HOST, PORT) 

    msg_split = msg.split(' ')

    #serializa a mensagem
    msg_bytes = pickle.dumps(msg_split, -1)
    size_bytes = struct.pack('i', len(msg_bytes))
    
    #envia a mensagem em bytes
    conn_sock.sendall(size_bytes)
    conn_sock.sendall(msg_bytes)

    #recebe a resposta em bytes
    size_bytes = sock_utils.receive_all(conn_sock, 4)
    size = struct.unpack('i', size_bytes)[0]

    #desserializa a resposta
    resposta_bytes = sock_utils.receive_all(conn_sock,size)  
    resposta = pickle.loads(resposta_bytes)

    print('Recebi: %s' % resposta) 
    conn_sock.close()