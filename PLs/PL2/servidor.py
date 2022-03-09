import sys, sock_utils
import pickle, struct

HOST = ''   

if len(sys.argv) > 1:   
    PORT = int(sys.argv[1])  
else:   
    PORT = 9999   
 
sock = sock_utils.create_tcp_server_socket(HOST, PORT, 1)
  
 
list = []    
while True:    
    try:  
        (conn_sock, addr) = sock.accept()

        #recebe a mensagem
        size_bytes = sock_utils.receive_all(conn_sock, 4)
        size = struct.unpack('i', size_bytes)[0]

        #desserializa a mensagem
        msg_bytes = conn_sock.recv(size)
        msg = pickle.loads(msg_bytes)
        
        resp = 'Ack'     
        
        if msg[0] == 'LIST':     
            resp = list    
        elif msg[0] == 'CLEAR':     
            list = []     
            resp = ['Lista apagada'] 
        else:     
            list.append(msg[0])      
        
        print(resp)
        #serializa a resposta
        resp_bytes = pickle.dumps(resp, -1)
        size_bytes = struct.pack('i', len(resp_bytes))

        #envia a resposta
        conn_sock.sendall(size_bytes)
        conn_sock.sendall(resp_bytes)

        print('list= %s' % list)   
        conn_sock.close()   
    except:    
        print('Vou encerrar!')   
        break