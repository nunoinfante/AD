import sys, socket as s  
from skeleton import *
import sock_utils

HOST = ''   

if len(sys.argv) > 1:   
    PORT = int(sys.argv[1])  
else:   
    PORT = 9999  

sock = s.socket(s.AF_INET, s.SOCK_STREAM)  
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)   
sock.bind((HOST, PORT))  
sock.listen(1)   
 
skeleton = ListSkeleton()

while True:    
    try:  
        (conn_sock, addr) = sock.accept()  

        resposta_size_bytes = sock_utils.receive_all(conn_sock, 4)
        size = struct.unpack('i', resposta_size_bytes)[0]
        
        resposta_bytes = sock_utils.receive_all(conn_sock, size)  
        resposta = skeleton.processMessage(resposta_bytes)

        size_bytes = struct.pack('i', len(resposta))
        conn_sock.sendall(size_bytes)
        conn_sock.sendall(resposta)
        
        conn_sock.close()
    except KeyboardInterrupt:
        break
    except:    
        print ('socket fechado!')   
        conn_sock.close()   
 
sock.close()