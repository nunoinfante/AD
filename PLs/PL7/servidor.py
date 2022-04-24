from flask import Flask, request, make_response 
import sqlite3

app = Flask(__name__) 

def connection():
    conn = sqlite3.connect('notas.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/aluno', methods = ["PUT"]) 
@app.route('/aluno/<int:id>', methods = ["GET"]) 
def aluno(id = None): 
    if request.method == "GET": 
        db = connection()
        row = db.execute('SELECT * FROM aluno WHERE numero = ?', (numero,)).fetchone()
        db.close()

        if not row:
            return {}, 404
        else:
            return {'data': dict(row)}, 200

    elif request.method == "PUT": 
        body = request.get_json()
        if 'numero' not in body:
            return {'message': 'numero is required'}, 400
        elif not isinstance(body['numero'], int):
            return {'message': 'numero is not an int'}, 400
        elif 'nome' not in body:
            return {'message': 'nome is required'}, 400

        numero = body['numero']
        nome = body['nome']

        db = connection()
        db.execute("INSERT INTO aluno (numero, nome) VALUES (?, ?)", (numero, nome))
        db.commit()
        db.close()

        r = make_response()
        r.headers['location'] = f'/alunos/{body["numero"]}'
        return r
 
@app.route('/notas', methods = ["POST", "GET"]) 
def notas(): 
    if request.method == "POST": 
        body = request.get_json()

        if 'numero_aluno' not in body:
            return {'message': 'numero_aluno is required'}, 400
        elif not isinstance(body['numero_aluno'], int):
            return {'message': 'numero_aluno is not an int'}, 400
        elif 'ano' not in body:
            return {'message': 'ano is required'}, 400
        elif 'cadeira' not in body:
            return {'message': 'cadeira is required'}, 400
        elif 'nota' not in body:
            return {'message': 'nota is required'}, 400
        elif not isinstance(body['nota'], int):
            return {'message': 'nota is not an int'}, 400

        numero_aluno = body['numero_aluno']
        ano = body['ano']
        cadeira = body['cadeira']
        nota = body['nota']

        db = connection()
        db.execute("INSERT INTO notas (numero_aluno, ano, cadeira, nota) VALUES (?, ?, ?, ?)", (numero_aluno, ano, cadeira, nota))
        db.commit()
        db.close()

        return 201

    elif request.method == "GET": 
        #ler campos no pedido e fazer query de acordo 
        r = make_response(request.data) #Devolve os dados no pedido 
        return r 

if __name__ == '__main__': 
    app.run(debug = True)