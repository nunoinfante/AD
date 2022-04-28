from flask import Flask, request, make_response 
import sqlite3
import requests

app = Flask(__name__)

def get_spotify_data(search, type):

    search = search.replace(' ', '%20')

    BASE_URL = 'https://api.spotify.com/v1/'
    access_token = 'BQAIYMy6I7zCdrTZNGSL-3Mw-62OehO1GmRKQIlkbCcfiTF0N1l_PIWKmNGjfSFmcVrioyVBVv4RLxl3mtGTb72usbiOF6hodTAtXe7ChwV0cs_W7OQ9RSKEN2YKpVb6f1MR9DawkOypBumRyr5DcGiTs2RG7BIfHw'
    headers = {'Authorization': f'Bearer {access_token}'}

    r = requests.get(BASE_URL + f'search?q={search}', headers=headers, params={'type' : type, 'limit' : 1})

    d = r.json()
    id = d['artists']['items'][0]['id']
    name = d['artists']['items'][0]['name']

    return id, name

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

        id_spotify, nome = get_spotify_data(nome, 'artist')

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


if __name__ == '__main__': 
    app.run(host="localhost", port=5000, debug=True)