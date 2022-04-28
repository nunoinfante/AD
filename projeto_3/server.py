from flask import Flask, request, make_response 
import sqlite3
import requests

app = Flask(__name__)

def get_spotify_data_artist(search):

    search = search.replace(' ', '%20')

    BASE_URL = 'https://api.spotify.com/v1/'
    access_token = 'BQCfiJ6rWVfFijnGV5nLD3kJUdh0DVp15Jo7mB47YM1y0i4cj7a5b7czJCyVCbR5DVbqP5t03jyClKRfXR9g65D7uI8SB_WanWtWJ1a4kYCM31f9-RhNVX70FqCn0fUpL0EBDxPRu_VqW8AEzALmLBdf_zlAH3XBGQ'
    headers = {'Authorization': f'Bearer {access_token}'}

    r = requests.get(BASE_URL + f'search?q={search}', headers=headers, params={'type' : 'artist', 'limit' : 1})

    d = r.json()
    id = d['artists']['items'][0]['id']
    name = d['artists']['items'][0]['name']

    return id, name

def get_spotify_data_track(search):

    search = search.replace(' ', '%20')

    BASE_URL = 'https://api.spotify.com/v1/'
    access_token = 'BQCfiJ6rWVfFijnGV5nLD3kJUdh0DVp15Jo7mB47YM1y0i4cj7a5b7czJCyVCbR5DVbqP5t03jyClKRfXR9g65D7uI8SB_WanWtWJ1a4kYCM31f9-RhNVX70FqCn0fUpL0EBDxPRu_VqW8AEzALmLBdf_zlAH3XBGQ'
    headers = {'Authorization': f'Bearer {access_token}'}

    r = requests.get(BASE_URL + f'search?q={search}', headers=headers, params={'type' : 'track', 'limit' : 1})

    d = r.json()
    id_track = d['tracks']['items'][0]['id']
    track_name = d['tracks']['items'][0]['name']
    id_artist = d['tracks']['items'][0]['artists'][0]['id']
    artist_name = d['tracks']['items'][0]['artists'][0]['name']

    return id_track, track_name, id_artist, artist_name

def connection():
    conn = sqlite3.connect('proj3.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/utilizadores', methods=['GET','POST'])
@app.route('/utilizadores/<int:id>', methods=['GET', 'DELETE'])
@app.route('/utilizadores/all', methods=['GET', 'DELETE'])
def utilizadores(id = None):
    if request.method == 'POST':
        body = request.get_json()

        nome = body['nome']
        senha = body['senha']

        db = connection()
        query = db.execute('INSERT INTO utilizadores VALUES (NULL, ?, ?)', (nome, senha))
        db.commit()
        db.close()

        r = make_response('Utilizador criado')
        r.headers['location'] = f'utilizadores/{query.lastrowid}'
        return r

    elif request.method == 'GET':
        if id is None:
            db = connection()
            rows = db.execute('SELECT * FROM utilizadores').fetchall()
            db.close()

            if not rows:
                return 'Utilizadores inexistentes', 404
            else:
                return {'utilizadores' : [dict(row) for row in rows]}, 200
                
        else:
            db = connection()
            row = db.execute('SELECT * FROM utilizadores WHERE id = ?', (id,)).fetchone()
            db.close()

            if not row:
                return 'Utilizador inexistente', 404
            else:
                return dict(row), 200

    elif request.method == 'DELETE':
        if id is None:
            db = connection()
            db.execute('DELETE FROM utilizadores')
            db.commit()
            db.close()

            r = make_response(f'Utilizadores eliminados')
            return r
        else:
            db = connection()
            db.execute('DELETE FROM utilizadores WHERE id = ?', (id,))
            db.commit()
            db.close()

            r = make_response(f'Utilizador {id} eliminado')
            return r

@app.route('/artistas/<int:id>', methods=['GET', 'DELETE'])
@app.route('/artistas', methods=['GET','POST'])
@app.route('/artistas/all', methods=['GET', 'DELETE'])
def artistas(id = None):
    if request.method == 'POST':
        body = request.get_json()

        nome = body['nome']

        id_spotify, nome = get_spotify_data_artist(nome)

        db = connection()
        query = db.execute('INSERT INTO artistas VALUES (NULL, ?, ?)', (id_spotify, nome))
        db.commit()
        db.close()

        r = make_response('Artista criado')
        r.headers['location'] = f'artistas/{query.lastrowid}'
        return r

    elif request.method == 'GET':
        if id is None:
            db = connection()
            rows = db.execute('SELECT * FROM artistas').fetchall()
            db.close()

            if not rows:
                return 'Artistas inexistentes', 404
            else:
                return {'artistas' : [dict(row) for row in rows]}, 200
        else:
            db = connection()
            row = db.execute('SELECT * FROM artistas WHERE id = ?', (id,)).fetchone()
            db.close()

            if not row:
                return 'Utilizador inexistente', 404
            else:
                return dict(row), 200
                
    elif request.method == 'DELETE':
        if id is None:
            db = connection()
            db.execute('DELETE FROM artistas')
            db.commit()
            db.close()

            r = make_response(f'Artistas eliminados')
            return r
        else:
            db = connection()
            db.execute('DELETE FROM artistas WHERE id = ?', (id,))
            db.commit()
            db.close()

            r = make_response(f'Artista {id} eliminado')
            return r

@app.route('/musicas/all', methods=['GET', 'DELETE'])
@app.route('/musicas', methods=['GET','POST'])
@app.route('/musicas/<int:id>', methods=['GET', 'DELETE'])
def musicas(id = None):
    if request.method == 'POST':
        body = request.get_json()

        nome = body['nome']

        id_spotify_track, track_name, id_spotify_artist, artist_name = get_spotify_data_track(nome)

        db = connection()
        id_artista  = db.execute('SELECT * FROM artistas WHERE id_spotify = ?', (id_spotify_artist,)).fetchone()
        
        if id_artista is None:
            query = db.execute('INSERT INTO artistas VALUES (NULL, ?, ?)', (id_spotify_artist, artist_name))
            id_artista  = db.execute('SELECT * FROM artistas WHERE id_spotify = ?', (id_spotify_artist,)).fetchone()['id_spotify']
            query1 = db.execute('INSERT INTO musicas VALUES (NULL, ?, ?, ?)', (id_spotify_track, track_name, id_artista))
            r = make_response('Artista e musica criadas')
            r.headers['location'] = f'musicas/{query1.lastrowid}'
        else:
            query = db.execute('INSERT INTO musicas VALUES (NULL, ?, ?, ?)', (id_spotify_track, track_name, id_artista['id_spotify']))
            r = make_response('Musica criada')
            r.headers['location'] = f'musicas/{query.lastrowid}'

        db.commit()
        db.close()

        return r

    elif request.method == 'GET':
        if id is None:
            db = connection()
            rows = db.execute('SELECT * FROM musicas').fetchall()
            db.close()

            if not rows:
                return 'Musicas inexistentes', 404
            else:
                return {'musicas' : [dict(row) for row in rows]}, 200
        else:
            db = connection()
            row = db.execute('SELECT * FROM musicas WHERE id = ?', (id,)).fetchone()
            db.close()

            if not row:
                return 'Musica inexistente', 404
            else:
                return dict(row), 200

@app.route('/utilizadores/<int:id>/avaliacoes', methods=['GET', 'POST'])
@app.route('/musicas/avaliacoes', methods=['GET'])
def avaliacoes(id = None):
    if request.method == 'POST':
        body = request.get_json()

        id_user = body['id_user']
        id_musica = body['id_musica']
        avaliacao = body['avaliacao']

        db = connection()
        id_avaliacao = db.execute('SELECT * FROM avaliacoes WHERE sigla = ?', (avaliacao,)).fetchone()
        db.execute('INSERT INTO playlists VALUES (?, ?, ?)', (id_user, id_musica, id_avaliacao['id']))
        db.commit()
        db.close()

        r = make_response('Avaliacao criada')
        r.headers['location'] = f'utilizadores/{id_user}/avaliacoes'
        return r

    elif request.method == 'GET':
        if id is None:
            body = request.get_json()

            avaliacao = body['avaliacao']

            db = connection()
            id_avaliacao = db.execute('SELECT * FROM avaliacoes WHERE sigla = ?', (avaliacao,)).fetchone()['id']
            musicas_avaliadas = db.execute('SELECT * FROM playlists WHERE id_avaliacao = ?', (id_avaliacao,)).fetchall()
            ids_musicas = [row['id_musica'] for row in musicas_avaliadas]
            musicas = db.execute(f'SELECT * FROM musicas WHERE id IN {tuple(ids_musicas)}').fetchall()
            db.close()

            if not musicas:
                return f'Musicas avaliadas com "{avaliacao}" inexistentes', 404
            else:
                return {'musicas' : [dict(row) for row in musicas]}, 200
        else:
            db = connection()
            rows = db.execute('SELECT * FROM playlists WHERE id_user = ?', (id,)).fetchall()
            db.close()

            if not rows:
                return 'Musicas inexistentes', 404
            else:
                return {'musicas' : [dict(row) for row in rows]}, 200


if __name__ == '__main__': 
    app.run(host="localhost", port=5000, debug=True)