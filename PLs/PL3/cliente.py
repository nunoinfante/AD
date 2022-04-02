import sys, socket as s   
from stub import *

if len(sys.argv) > 1:    
    HOST = sys.argv[1]    
    PORT = int(sys.argv[2])  
else:    
    HOST = '127.0.0.1'    
    PORT = 9999   
 
stub = ListStub(HOST,PORT)

while True:    
    msg = input('Mensagem: ');     
    if msg == 'EXIT':     
        exit()    
     
    command, *element = msg.split()

    result = []
    if command == 'APPEND':
        result = stub.append(element)
    elif command == 'LIST':
        result = stub.list()
    elif command == 'CLEAR':
        result = stub.clear()

    print(f'Recebi: {", ".join(result)}')