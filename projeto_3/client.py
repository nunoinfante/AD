import requests
import json

while True:
    comando = input('comando > ')
    comando_split = comando.split()

    if comando_split[0] == 'EXIT':
        break

    elif comando_split[0] == 'CREATE':
        if comando_split[1] == 'UTILIZADOR' and len(comando_split) == 4:
            utilizador = {'nome' : comando_split[2], 'senha' : comando_split[3]}
            r = requests.post('http://localhost:5000/utilizadores', json = utilizador)
            print('***')
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('URL: http://localhost:5000/' + r.headers['location'])
            print('***')
            
        elif comando_split[1] == 'ARTISTA':
            name = comando.split(' ', 2)[2]
            artista = {'nome' : name}
            r = requests.post('http://localhost:5000/artistas', json = artista)
            print('***')
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('URL: http://localhost:5000/' + r.headers['location'])
            print('***')

        elif comando_split[1] == 'MUSICA':
            musica = {'id_spotify' : comando_split[2]}
            r = requests.post('http://localhost:5000/musicas', json = musica)
            print('***')
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('URL: http://localhost:5000/' + r.headers['location'])
            print('***')

        else:
            if len(comando_split) != 4:
                print('MISSING ARGUMENTS')
            else:
                avaliacao = {'id_user' : comando_split[2], 'id_musica' : comando_split[3], 'avaliacao' : comando_split[4]}
                r = requests.post(f'http://localhost:5000/utilizadores/{comando_split[2]}/avaliacoes')

    elif comando_split[0] == 'READ':
        if comando_split[1] == 'UTILIZADOR' and len(comando_split) == 3:
            r = requests.get('http://localhost:5000/utilizadores/' + comando_split[2])
            print('***')
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('***')

        elif comando_split[1] == 'ARTISTA' and len(comando_split) == 3:
            r = requests.get('http://localhost:5000/artistas/' + comando_split[2])
            print('***')    
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('***')

        elif comando_split[1] == 'MUSICA' and len(comando_split) == 3:
            r = requests.get('http://localhost:5000/musicas/' + comando_split[2])
            print('***')
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('***')

        elif comando_split[1] == 'ALL':
            if comando_split[2] == 'UTILIZADORES':
                r = requests.get('http://localhost:5000/utilizadores/all')
                print('***')
                print(f'HTTP Status: {r.status_code}') 
                print(f'Mensagem: {r.content.decode()}') 
                print('URL: http://localhost:5000/utilizadores/all')
                print('***')
            elif comando_split[2] == 'ARTISTAS':
                r = requests.get('http://localhost:5000/artistas/all')
                print('***')
                print(f'HTTP Status: {r.status_code}') 
                print(f'Mensagem: {r.content.decode()}') 
                print('URL: http://localhost:5000/artistas/all')
                print('***')
            elif comando_split[2] == 'MUSICAS':
                if len(comando_split) == 3:
                    r = requests.get('http://localhost:5000/musicas/all')
                    print('***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}') 
                    print('URL: http://localhost:5000/musicas/all')
                    print('***')
                elif len(comando_split) == 4:
                    musicas_avaliacao = {'avaliacao' : comando_split[3]}
                    #TODO
            elif comando_split[2] == 'MUSICAS_A':
                musicas_a = {'id_artista' : comando_split[3]}
                #TODO
            elif comando_split[2] == 'MUSICAS_U':
                musicas_u = {'id_user' : comando_split[3]}
                #TODO


    elif comando_split[0] == 'DELETE':
        if comando_split[1] == 'UTILIZADOR' and len(comando_split) == 3:
            r = requests.delete('http://localhost:5000/utilizadores/' + comando_split[2])
            print('***')
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('***')
        elif comando_split[1] == 'ARTISTA' and len(comando_split) == 3:
            r = requests.delete('http://localhost:5000/artistas/' + comando_split[2])
            print('***')
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('***')
        elif comando_split[1] == 'MUSICA' and len(comando_split) == 3:
            r = requests.delete('http://localhost:5000/musicas/' + comando_split[2])
            print('***')
            print(f'HTTP Status: {r.status_code}') 
            print(f'Mensagem: {r.content.decode()}') 
            print('***')
        elif comando_split[1] == 'ALL':
            if comando_split[2] == 'UTILIZADORES':
                r = requests.delete('http://localhost:5000/utilizadores/all')
                print('***')
                print(f'HTTP Status: {r.status_code}') 
                print(f'Mensagem: {r.content.decode()}') 
                print('***')
            elif comando_split[2] == 'ARTISTAS':
                r = requests.delete('http://localhost:5000/artistas/all')
                print('***')
                print(f'HTTP Status: {r.status_code}') 
                print(f'Mensagem: {r.content.decode()}') 
                print('***')
            elif comando_split[2] == 'MUSICAS':
                if len(comando_split) == 3:
                    r = requests.delete('http://localhost:5000/musicas/all')
                    print('***')
                    print(f'HTTP Status: {r.status_code}') 
                    print(f'Mensagem: {r.content.decode()}') 
                    print('***')
                elif len(comando_split) == 4:
                    musicas_avaliacao = {'avaliacao' : comando_split[3]}
                    #TODO
            elif comando_split[2] == 'MUSICAS_A':
                musicas_a = {'id_artista' : comando_split[3]}
                #TODO
            elif comando_split[2] == 'MUSICAS_U':
                musicas_u = {'id_user' : comando_split[3]}
                #TODO


    # elif comando_split[0] == 'UPDATE':
    #     if comando_split[1] == 'UTILIZADOR'  and len(comando_split) == 4:
    #         utilizador = {'id_user' : comando_split[2], 'password' : comando_split[3]}
    #         url = 'http://localhost:5000/utilizadores'
    #     elif comando_split[1] == 'MUSICA'  and len(comando_split) == 5:
    #         musica = {'id_musica' : comando_split[2], 'avaliacao' : comando_split[3], 'id_user' : comando_split[4]}
        
