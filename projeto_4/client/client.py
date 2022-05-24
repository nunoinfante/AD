"""
Aplicações Distribuídas - Projeto 4 - client.py
Grupo: 50
Números de aluno: 53330, 55411
"""

from http import client
import requests, json
import os

while True:
    try:
        comando = input('comando > ')
        comando_split = comando.split()
        
        if comando_split[0] == 'EXIT':
            break

        elif comando_split[0] == 'CREATE':
            if comando_split[1] == 'UTILIZADOR':
                if len(comando_split) == 4:
                    utilizador = {'nome' : comando_split[2], 'senha' : comando_split[3]}
                    r = requests.post('https://localhost:5000/utilizadores', json = utilizador, verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}') 
                    print('URL: https://localhost:5000/' + r.headers['location'])
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')
                
            elif comando_split[1] == 'ARTISTA':
                if len(comando_split) == 3:
                    artista = {'id_spotify' : comando_split[2]}
                    r = requests.post('https://localhost:5000/artistas', json = artista, verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}') 
                    print('URL: https://localhost:5000/' + r.headers['location'])
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')

            elif comando_split[1] == 'MUSICA':
                if len(comando_split) == 3:
                    musica = {'id_spotify' : comando_split[2]}
                    r = requests.post('https://localhost:5000/musicas', json = musica, verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}') 
                    print('URL: https://localhost:5000/' + r.headers['location'])
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')
            
            else:
                if len(comando_split) == 4:
                    avaliacao = {'id_musica' : comando_split[2], 'avaliacao' : comando_split[3]}
                    r = requests.post(f'https://localhost:5000/musicas/all/utilizadores/{comando_split[1]}', json = avaliacao, verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))

                    if r.status_code == 404:
                        print('Comando desconhecido ')

                    else:
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}') 
                        print(f'Mensagem: {r.content.decode()}') 
                        print('URL: https://localhost:5000' + r.headers['location'])
                        print(r.headers['Content-Type'])
                        print('***\n')
                
                else:
                    print('Argumentos em falta')

        elif comando_split[0] == 'READ':
            if comando_split[1] == 'UTILIZADOR':
                if len(comando_split) == 3:
                    r = requests.get(f'https://localhost:5000/utilizadores/{comando_split[2]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}')
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')

            elif comando_split[1] == 'ARTISTA':
                if len(comando_split) == 3:
                    r = requests.get(f'https://localhost:5000/artistas/{comando_split[2]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')    
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}')
                    print(r.headers['Content-Type'])
                    print('***\n')
                    
                else:
                    print('Argumentos em falta')

            elif comando_split[1] == 'MUSICA':
                if len(comando_split) == 3:
                    r = requests.get(f'https://localhost:5000/musicas/{comando_split[2]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}') 
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')

            elif comando_split[1] == 'ALL':
                if comando_split[2] == 'UTILIZADORES':
                    if len(comando_split) == 3:
                        r = requests.get('https://localhost:5000/utilizadores/all', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}') 
                        print(f'Mensagem: {r.content.decode()}') 
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta')

                elif comando_split[2] == 'ARTISTAS':
                    if len(comando_split) == 3:
                        r = requests.get('https://localhost:5000/artistas/all', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}') 
                        print(f'Mensagem: {r.content.decode()}')
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta')

                elif comando_split[2] == 'MUSICAS':
                    if len(comando_split) == 3:
                        r = requests.get('https://localhost:5000/musicas/all', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}') 
                        print(f'Mensagem: {r.content.decode()}')
                        print(r.headers['Content-Type'])
                        print('***\n')

                    elif len(comando_split) == 4:
                        r = requests.get(f'https://localhost:5000/musicas/all/avaliacoes/{comando_split[3]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}')
                        print(f'Mensagem: {r.content.decode()}')
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta') 

                elif comando_split[2] == 'MUSICAS_A':
                    if len(comando_split) == 4:
                        r = requests.get(f'https://localhost:5000/musicas/all/artistas/{comando_split[3]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}')
                        print(f'Mensagem: {r.content.decode()}')
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta') 

                elif comando_split[2] == 'MUSICAS_U':
                    if len(comando_split) == 4:
                        r = requests.get(f'https://localhost:5000/musicas/all/utilizadores/{comando_split[3]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}')
                        print(f'Mensagem: {r.content.decode()}')
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta') 

                else:
                    print('Comando desconhecido')

            else:
                print('Comandos desconhecidos')
        
        elif comando_split[0] == 'DELETE':
            if comando_split[1] == 'UTILIZADOR':
                if len(comando_split) == 3:
                    r = requests.delete(f'https://localhost:5000/utilizadores/{comando_split[2]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}') 
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta') 

            elif comando_split[1] == 'ARTISTA':
                if len(comando_split) == 3:
                    r = requests.delete(f'https://localhost:5000/artistas/{comando_split[2]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}')
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')

            elif comando_split[1] == 'MUSICA':
                if len(comando_split) == 3:
                    r = requests.delete(f'https://localhost:5000/musicas/{comando_split[2]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}')
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')

            elif comando_split[1] == 'ALL':
                if comando_split[2] == 'UTILIZADORES':
                    if len(comando_split) == 3:
                        r = requests.delete('https://localhost:5000/utilizadores/all', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}') 
                        print(f'Mensagem: {r.content.decode()}') 
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta')

                elif comando_split[2] == 'ARTISTAS':
                    if len(comando_split) == 3:
                        r = requests.delete('https://localhost:5000/artistas/all', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}') 
                        print(f'Mensagem: {r.content.decode()}') 
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                     print('Argumentos em falta')

                elif comando_split[2] == 'MUSICAS':
                    if len(comando_split) == 3:
                        r = requests.delete('https://localhost:5000/musicas/all', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}') 
                        print(f'Mensagem: {r.content.decode()}') 
                        print(r.headers['Content-Type'])
                        print('***\n')

                    elif len(comando_split) == 4:
                        r = requests.delete(f'https://localhost:5000/musicas/all/avaliacoes/{comando_split[3]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}')
                        print(f'Mensagem: {r.content.decode()}')
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta')

                elif comando_split[2] == 'MUSICAS_A':
                    if len(comando_split) == 4:
                        r = requests.delete(f'https://localhost:5000/musicas/all/artistas/{comando_split[3]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}')
                        print(f'Mensagem: {r.content.decode()}')
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta')

                elif comando_split[2] == 'MUSICAS_U':
                    if len(comando_split) == 4:
                        r = requests.delete(f'https://localhost:5000/musicas/all/utilizadores/{comando_split[3]}', verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                        print('\n***')
                        print(f'HTTP Status: {r.status_code}')
                        print(f'Mensagem: {r.content.decode()}')
                        print(r.headers['Content-Type'])
                        print('***\n')

                    else:
                        print('Argumentos em falta')

            else:   
                print('Comando desconhecido')

        elif comando_split[0] == 'UPDATE':
            if comando_split[1] == 'UTILIZADOR':
                if len(comando_split) == 4:
                    utilizador = {'id_user' : comando_split[2], 'password' : comando_split[3]}
                    r = requests.put(f'https://localhost:5000/utilizadores', json=utilizador, verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}')
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')

            elif comando_split[1] == 'MUSICA':
                if len(comando_split) == 5:
                    musica = {'id_musica' : comando_split[2], 'avaliacao' : comando_split[3], 'id_user' : comando_split[4]}
                    r = requests.put(f'https://localhost:5000/musicas', json = musica, verify = '../certs/root.pem', cert = ('../certs/cli.crt', '../certs/cli.key'))
                    print('\n***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}')
                    print(r.headers['Content-Type'])
                    print('***\n')

                else:
                    print('Argumentos em falta')
                    
            else:
                print('Comando desconhecido')

        else:
            print('Comando desconhecido')

    except requests.exceptions.ConnectionError:
        print('Servidor desligado')
    except IndexError:
        print('Argumentos em falta')
    except (KeyError):
        pass