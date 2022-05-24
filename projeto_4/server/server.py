"""
Aplicações Distribuídas - Projeto 4 - server.py
Grupo: 50
Números de aluno: 53330, 55411
"""

from flask import Flask, request, make_response, redirect, url_for, jsonify
import sqlite3, requests, ssl, os
from requests_oauthlib import OAuth2Session
from os.path import isfile

app = Flask(__name__)

client_id = '7245356318a948f4bed0bd361882b36f'
client_secret = '206a7ffa6ef74f58b49098b71f35fad3'
redirect_uri= 'https://localhost:5000/callback'
spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)

def get_spotify_data(id_spotify, type):
    if type == 'artist':
        r = spotify.get(f'https://api.spotify.com/v1/artists/{id_spotify}')
        d = r.json()

        return d

    elif type == 'track':
        r = spotify.get(f'https://api.spotify.com/v1/tracks/{id_spotify}')
        d = r.json()

        return d


def connection():
    db_is_created = isfile('proj4.db')
    conn = sqlite3.connect('proj4.db')
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    if not db_is_created:
        with open('proj4.sql', mode='r') as db:
            cur.executescript(db.read())
            conn.commit()
    else:
        conn.execute("PRAGMA foreign_keys = ON")   
    return conn


@app.route('/login', methods=["GET"])
def login():
    authorization_base_url = 'https://accounts.spotify.com/authorize'
    authorization_url, state = spotify.authorization_url(authorization_base_url)
    return redirect(authorization_url)


@app.route('/callback', methods=["GET"])
def callback():
    token_url = 'https://accounts.spotify.com/api/token'
    spotify.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)#
    return redirect(url_for('.profile'))


@app.route('/profile', methods=["GET"])
def profile():
    protected_resource = 'https://api.spotify.com/v1/me'
    return jsonify(spotify.get(protected_resource).json()) 


@app.route('/utilizadores', methods=['GET','POST','PUT'])
@app.route('/utilizadores/<int:id>', methods=['GET', 'DELETE'])
@app.route('/utilizadores/all', methods=['GET', 'DELETE'])
def utilizadores(id = None):
    try:
        if request.method == 'POST':   
            body = request.get_json()

            nome = body['nome']
            senha = body['senha']

            db = connection()
            rows = db.execute('SELECT * FROM utilizadores WHERE nome = ?', (nome,)).fetchall()
            if not rows:
                query = db.execute('INSERT INTO utilizadores VALUES (NULL, ?, ?)', (nome, senha))
                db.commit()
                db.close()
                r = make_response('Utilizador criado', 201)
                r.mimetype = 'application/json'
                r.headers['location'] = f'utilizadores/{query.lastrowid}'
            else:
                db.close()
                r = make_response('Nome utilizador ja existe', 404)
                r.mimetype = 'application/api-problem+json'
            return r

        elif request.method == 'GET':
            if id is None:
                db = connection()
                rows = db.execute('SELECT * FROM utilizadores').fetchall()
                db.close()

                if not rows:
                    r = make_response('Utilizadores inexistentes', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r
                else:
                    r = make_response({'utilizadores' : [dict(row) for row in rows]}, 200)
                    r.mimetype = 'application/json'
                    return r
                    
            else:
                db = connection()
                row = db.execute('SELECT * FROM utilizadores WHERE id = ?', (id,)).fetchone()
                db.close()

                if not row:
                    r = make_response('Utilizador inexistente', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r
                else:
                    r = make_response(dict(row), 200)
                    r.mimetype = 'application/json'
                    return r

        elif request.method == 'DELETE':
            if id is None:
                db = connection()

                row = db.execute('SELECT * FROM utilizadores').fetchone()

                if not row:
                    db.close()

                    r = make_response('Utilizadores inexistentes', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r

                else:
                    db.execute('DELETE FROM utilizadores')
                    db.commit()
                    db.close()

                    r = make_response(f'Utilizadores eliminados', 200)
                    r.mimetype = 'application/json'
                    return r

            else:
                db = connection()

                row = db.execute('SELECT * FROM utilizadores WHERE id = ?', (id,)).fetchone()
                
                if not row:
                    r = make_response('Utilizador inexistente', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r

                else:
                    db.execute('DELETE FROM utilizadores WHERE id = ?', (id,))
                    db.commit()
                    db.close()

                    r = make_response(f'Utilizador {id} eliminado', 200)
                    r.mimetype = 'application/json'
                    return r

        elif request.method == 'PUT':
            body = request.get_json()

            utilizador = body['id_user']
            senha = body['password']

            db = connection()
            row = db.execute('SELECT * FROM utilizadores WHERE id = ?', (utilizador,)).fetchone()

            if not row:
                db.close()

                r = make_response('Utilizador nao existente', 404)
                r.mimetype = 'application/api-problem+json'
                return r

            else:
                db.execute('UPDATE utilizadores SET senha = ? WHERE id = ?', (senha, utilizador))
                db.commit()
                db.close()

                r = make_response(f'Utilizador {utilizador} atualizado', 200)
                r.mimetype = 'application/json'
                return r
                
    except sqlite3.IntegrityError:
        r = make_response('Erro de integridade da base de dados', 500)
        r.mimetype = 'application/api-problem+json'
        return r


@app.route('/artistas/<int:id>', methods=['GET', 'DELETE'])
@app.route('/artistas', methods=['GET','POST'])
@app.route('/artistas/all', methods=['GET', 'DELETE'])
def artistas(id = None):
    try:
        if request.method == 'POST':
            body = request.get_json()

            id_spotify = body['id_spotify']

            d = get_spotify_data(id_spotify, 'artist')
            
            if list(d.keys())[0] == 'error':
                if (d['error']['status'] == 401):
                    r = make_response(d['error']['message'], 401)
                    r.mimetype = 'application/api-problem+json'
                    return r

            name = d['name']

            db = connection()
            row = db.execute('SELECT * FROM artistas WHERE id_spotify = ?', (id_spotify,)).fetchone()
            if not row:
                query = db.execute('INSERT INTO artistas VALUES (NULL, ?, ?)', (id_spotify, name))
                db.commit()
                db.close()

                r = make_response('Artista criado', 201)
                r.mimetype = 'application/json'
                r.headers['location'] = f'artistas/{query.lastrowid}'
            else:
                db.close()
                r = make_response(f'Ja existe artiste com o id: {id_spotify}', 404)
                r.mimetype = 'application/api-problem+json'
            return r

        elif request.method == 'GET':
            if id is None:
                db = connection()
                rows = db.execute('SELECT * FROM artistas').fetchall()
                db.close()

                if not rows:
                    r = make_response('Artistas inexistentes', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r
                else:
                    r = make_response({'artistas' : [dict(row) for row in rows]}, 200)
                    r.mimetype = 'application/json'
                    return r
            else:
                db = connection()
                row = db.execute('SELECT * FROM artistas WHERE id = ?', (id,)).fetchone()
                db.close()

                if not row:
                    r = make_response('Artista inexistente', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r

                else:
                    r = make_response(dict(row), 200)
                    r.mimetype = 'application/json'
                    return r
                    
        elif request.method == 'DELETE':
            if id is None:
                db = connection()

                row = db.execute('SELECT * FROM artistas').fetchone()

                if not row:
                    r = make_response('Artistas inexistente', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r

                else:
                    db.execute('DELETE FROM artistas')
                    db.commit()
                    db.close()

                    r = make_response(f'Artistas eliminados', 200)
                    r.mimetype = 'application/json'
                    return r
            else:
                db = connection()

                row = db.execute('SELECT * FROM artistas WHERE id = ?', (id,)).fetchone()

                if not row:
                    r = make_response('Artista inexistente', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r

                else:
                    db.execute('DELETE FROM artistas WHERE id = ?', (id,))
                    db.commit()
                    db.close()

                    r = make_response(f'Artista {id} eliminado', 200)
                    r.mimetype = 'application/json'
                    return r

    except sqlite3.IntegrityError:
        r = make_response('Erro de integridade da base de dados', 500)
        r.mimetype = 'application/api-problem+json'
        return r


@app.route('/musicas/all', methods=['GET', 'DELETE'])
@app.route('/musicas', methods=['GET','POST', 'PUT'])
@app.route('/musicas/all/avaliacoes/<string:id>', methods=['GET', 'DELETE'])
@app.route('/musicas/<int:id>', methods=['GET', 'DELETE'])
@app.route('/musicas/all/artistas/<int:id>', methods=['GET', 'DELETE'])
@app.route('/musicas/all/utilizadores/<int:id>', methods=['GET', 'DELETE', 'POST'])
def musicas(id = None):
    try:
        if request.method == 'POST':
            if id is None:
                body = request.get_json()

                id_spotify_track = body['id_spotify']

                d = get_spotify_data(id_spotify_track, 'track')

                if list(d.keys())[0] == 'error':
                    if (d['error']['status'] == 401):
                        r = make_response(d['error']['message'], 401)
                        r.mimetype = 'application/api-problem+json'
                        return r

                track_name = d['name']
                artist_name = d['artists'][0]['name']
                id_spotify_artist = d['artists'][0]['id']

                db = connection()
                id_artista  = db.execute('SELECT * FROM artistas WHERE id_spotify = ?', (id_spotify_artist,)).fetchone()
                row = db.execute('SELECT * FROM musicas WHERE id_spotify = ?', (id_spotify_track,)).fetchone()

                if id_artista is None:
                    query = db.execute('INSERT INTO artistas VALUES (NULL, ?, ?)', (id_spotify_artist, artist_name))
                    id_artista  = db.execute('SELECT * FROM artistas WHERE id_spotify = ?', (id_spotify_artist,)).fetchone()['id']
                    
                    if row is None:
                        query1 = db.execute('INSERT INTO musicas VALUES (NULL, ?, ?, ?)', (id_spotify_track, track_name, id_artista))
                        r = make_response('Artista e musica criadas', 201)
                        r.mimetype = 'application/json'
                        r.headers['location'] = f'musicas/{query1.lastrowid}'
                        
                    else:
                        r = make_response(f'Musica com id: {id_spotify_track} ja existe', 404)
                        r.mimetype = 'application/api-problem+json'

                else:
                    row = db.execute('SELECT * FROM musicas WHERE id_spotify = ?', (id_spotify_track,)).fetchone()
                    if row is None:
                        query = db.execute('INSERT INTO musicas VALUES (NULL, ?, ?, ?)', (id_spotify_track, track_name, id_artista['id']))
                        r = make_response('Musica criada', 201)
                        r.mimetype = 'application/json'
                        r.headers['location'] = f'musicas/{query.lastrowid}'
                    else:
                        r = make_response(f'Musica com id: {id_spotify_track} ja existe', 404)
                        r.mimetype = 'application/api-problem+json'

                db.commit()
                db.close()
                return r

            else:
                body = request.get_json()

                id_musica = body['id_musica']
                avaliacao = body['avaliacao']

                db = connection()
                id_avaliacao = db.execute('SELECT * FROM avaliacoes WHERE sigla = ?', (avaliacao,)).fetchone()
                row = db.execute('SELECT * FROM playlists WHERE id_user = ? AND id_musica = ?', (id,id_musica)).fetchone()
                if not row:
                    db.execute('INSERT INTO playlists VALUES (?, ?, ?)', (id, id_musica, id_avaliacao['id']))
                    db.commit()
                    db.close()
                    r = make_response('Avaliacao criada', 201)
                    r.mimetype = 'application/json'
                    r.headers['location'] = f'/musicas/all/utilizadores/{id}'
                else:
                    db.close()
                    r = make_response('Avaliacao ja existe', 404)
                    r.mimetype = 'application/api-problem+json'
                return r
                

        elif request.method == 'GET':
            if id is None:
                db = connection()
                rows = db.execute('SELECT * FROM musicas').fetchall()
                db.close()

                if not rows:
                    r = make_response('Musicas inexistentes', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r
                else:
                    r = make_response({'musicas' : [dict(row) for row in rows]}, 200)
                    r.mimetype = 'application/json'
                    return r
            else:
                path = request.path.split('/')
                path = list(filter(None, path))
                if len(path) == 4:
                    if path[2] == 'avaliacoes':
                        db = connection()
                        id_avaliacao = db.execute('SELECT * FROM avaliacoes WHERE sigla = ?', (id,)).fetchone()['id']
                        musicas = db.execute('SELECT musicas.id, musicas.id_spotify, musicas.nome, musicas.id_artista, avaliacoes.sigla FROM musicas, playlists, avaliacoes WHERE musicas.id = playlists.id_musica AND playlists.id_avaliacao = avaliacoes.id AND avaliacoes.id = ?', (id_avaliacao,)).fetchall()
                        db.close()

                        if not musicas:
                            r = make_response(f'Musicas avaliadas com "{id}" inexistentes', 404)
                            r.mimetype = 'application/api-problem+json'
                            return r
                        else:
                            r = make_response({'musicas' : [dict(row) for row in musicas]}, 200)
                            r.mimetype = 'application/json'
                            return r

                    elif path[2] == 'artistas':
                        db = connection()
                        artista = db.execute('SELECT * FROM artistas WHERE id = ?', (id,)).fetchone()
                        musicas_playlists = db.execute('SELECT musicas.id, musicas.id_spotify, musicas.nome, musicas.id_artista, avaliacoes.sigla FROM musicas, playlists, avaliacoes, artistas WHERE avaliacoes.id = playlists.id_avaliacao AND playlists.id_musica = musicas.id AND musicas.id_artista = artistas.id AND artistas.id = ?', (id,)).fetchall()
                        db.close()

                        if not artista:
                            r = make_response('Artista inexistente', 404)
                            r.mimetype = 'application/api-problem+json'
                            return r

                        elif not musicas_playlists:
                            r = make_response(f'Musicas avaliadas do artista "{id}" inexistentes', 404)
                            r.mimetype = 'application/api-problem+json'
                            return r

                        else:
                            r = make_response({'musicas' : [dict(row) for row in musicas_playlists]}, 200)
                            r.mimetype = 'application/json'
                            return r

                    elif path[2] == 'utilizadores':
                        db = connection()
                        user = db.execute('SELECT * FROM utilizadores WHERE id = ?', (id,)).fetchone()
                        musicas_user = db.execute('SELECT musicas.id, musicas.id_spotify, musicas.nome, musicas.id_artista, avaliacoes.sigla FROM musicas, playlists, avaliacoes WHERE musicas.id = playlists.id_musica AND playlists.id_avaliacao = avaliacoes.id AND playlists.id_user = ?', (id,)).fetchall()
                        db.close()

                        if not user:
                            r = ('Utilizador inexistente', 404)
                            r.mimetype = 'application/api-problem+json'
                            return r

                        elif not musicas_user:
                            r = make_response(f'Musicas avaliadas pelo utilizador "{id}" inexistentes', 404)
                            r.mimetype = 'application/api-problem+json'
                            return r
                            
                        else:
                            r = make_response({'musicas' : [dict(row) for row in musicas_user]}, 200)
                            r.mimetype = 'application/json'
                            return r

                else:
                    db = connection()
                    row = db.execute('SELECT * FROM musicas WHERE id = ?', (id,)).fetchone()
                    db.close()

                    if not row:
                        r = make_response('Musica inexistente', 404)
                        r.mimetype = 'application/api-problem+json'
                        return r
                    
                    else:
                        r = make_response(dict(row), 200)
                        r.mimetype = 'application/json'
                        return r

        elif request.method == 'DELETE':
            if id is None:
                db = connection()
                musicas = db.execute('SELECT * FROM musicas').fetchall()
                query = db.execute('DELETE FROM musicas')
                db.commit()
                db.close()

                if not musicas:
                    r = make_response('Musicas inexistentes', 404)
                    r.mimetype = 'application/api-problem+json'
                    return r
                else:
                    r = make_response('Todas as musicas eliminadas', 200)
                    r.mimetype = 'application/json'
                    return r

            else:
                path = request.path.split('/')
                path = list(filter(None, path))
                
                if len(path) == 4:
                    if path[2] == 'avaliacoes':
                        db = connection()
                        musica_com_avaliacaoX = db.execute('SELECT * FROM musicas WHERE musicas.id IN (SELECT playlists.id_musica FROM playlists, avaliacoes WHERE playlists.id_avaliacao = avaliacoes.id AND avaliacoes.sigla = ?)', (id,)).fetchall()
                        
                        if not musica_com_avaliacaoX:
                            db.close()
                            r = make_response(f'Nao existe musica com a avaliacao {id}', 404)
                            r.mimetype = 'application/api-problem+json'
                            return r

                        else:
                            db.execute('DELETE FROM musicas WHERE musicas.id IN (SELECT playlists.id_musica FROM playlists, avaliacoes WHERE playlists.id_avaliacao = avaliacoes.id AND avaliacoes.sigla = ?)', (id,))
                            db.commit()
                            db.close()

                            r = make_response(f'Musicas eliminadas', 200)
                            r.mimetype = 'application/json'
                            return r
                            
                    elif path[2] == 'artistas':
                        db = connection()
                        musicas_playlists = db.execute('SELECT musicas.id, musicas.id_spotify, musicas.nome, musicas.id_artista FROM musicas, playlists WHERE musicas.id_artista = ? AND musicas.id = playlists.id_musica', (id,)).fetchall()
                        if not musicas_playlists:
                            db.close()
                            r = make_response('Artista nao tem musicas avaliadas', 404)
                            r.mimetype = 'application/api-problem+json'
                            return r

                        else:
                            db.execute('DELETE FROM musicas WHERE musicas.id_artista = ? AND musicas.id IN (SELECT playlists.id_musica FROM playlists)', (id,))
                            db.commit()
                            db.close()

                            r = make_response(f'Musicas eliminadas', 200)
                            r.mimetype = 'application/json'
                            return r

                    elif path[2] == 'utilizadores':
                        db = connection()
                        musicas_user = db.execute('SELECT musicas.id, musicas.id_spotify, musicas.nome, musicas.id_artista FROM musicas, playlists WHERE musicas.id = playlists.id_musica AND playlists.id_user = ?', (id,)).fetchall()
                        if not musicas_user:
                            db.close()
                            r = make_response('Utilizador nao avaliou musicas', 404)
                            r.mimetype = 'application/api-problem+json'
                            return r

                        else:
                            db.execute('DELETE FROM musicas WHERE musicas.id IN (SELECT playlists.id_musica FROM playlists WHERE playlists.id_user = ?)', (id,))
                            db.commit()
                            db.close()

                            r = make_response(f'Musicas eliminadas', 200)
                            r.mimetype = 'application/json'
                            return r
                else:
                    db = connection()
                    row = db.execute('SELECT * FROM musicas WHERE id = ?', (id,)).fetchone()
                    if not row:
                        db.close()
                        r = make_response('Musica inexistente', 404)
                        r.mimetype = 'application/api-problem+json'
                        return r

                    else:
                        db.execute('DELETE FROM musicas WHERE id = ?', (id,))
                        db.commit()
                        db.close()

                        r = make_response(f'Musica eliminada', 200)
                        r.mimetype = 'application/json'
                        return r
                        
        
        elif request.method == 'PUT':
            body = request.get_json()
            id_musica = body['id_musica']
            avaliacao = body['avaliacao']
            id_user = body['id_user']

            db = connection()
            row = db.execute('SELECT * from playlists WHERE id_user = ? AND id_musica = ?', (id_user, id_musica)).fetchone()
            id_avaliacao = db.execute('SELECT * FROM avaliacoes WHERE sigla = ?', (avaliacao,)).fetchone()['id']

            if not row:
                db.close()

                r = make_response(f'Não existe avaliacao de {id_user} para a musica {id_musica}', 404)
                r.mimetype = 'application/api-problem+json'
                return r

            else:
                db.execute('UPDATE playlists SET id_avaliacao = ? WHERE id_musica = ? AND id_user = ?', (id_avaliacao, id_musica, id_user))
                db.commit()
                db.close()

                r = make_response(f'Avaliacao do utilizador {id_user} para a musica {id_musica} atualizada', 200)
                r.mimetype = 'application/json'
                return r

    except sqlite3.IntegrityError:
        r = make_response('Erro de integridade da base de dados', 500)
        r.mimetype = 'application/api-problem+json'
        return r


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='../certs/root.pem')
    context.load_cert_chain(certfile='../certs/serv.crt',keyfile='../certs/serv.key')
    app.run('localhost', ssl_context=context, debug = True)