import ssl
from requests_oauthlib import OAuth2Session
from flask import Flask, redirect, request
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Credenciais da app cliente registada no Spotify (https://developer.spotify.com/dashboard/applications)
client_id = 'f89747f84788a5789126ed2162ab'
client_secret = '25e6b4b519d747bb9dd575a0383df2b6'

# URIs do spotify para obtencao do authorization_code, do token, de callback e do recurso protegido
authorization_base_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'
redirect_uri = 'https://localhost:5000/callback'
protected_resource = 'https://api.spotify.com/v1/me'
spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)

# # Pedido do authorization_code ao servidor de autorização (e dono do recuro a aceder)
# authorization_url, state = spotify.authorization_url(authorization_base_url)
# print('Aceder ao link (via browser) para obter a autorizacao,', authorization_url)

# # Obter o authorization_code do servidor vindo no URL de redireccionamento
# url_response = input(' insira o URL devolvido no browser e cole aqui:')

# # Obtencao do token
# spotify.fetch_token(token_url, client_secret=client_secret,
#                     authorization_response=url_response)

# # Acesso a um recurso protegido
# r = spotify.get(protected_resource)
# print(r.content.decode())

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def login():
    authorization_url, _ = spotify.authorization_url(authorization_base_url)
    return redirect(authorization_url)


@app.route('/callback', methods=['GET'])
def login_callback():
    spotify.fetch_token(token_url, client_secret=client_secret,
                        authorization_response=request.url)
    return redirect(f'/profile?token={spotify.token["access_token"]}')


@app.route('/profile', methods=['GET'])
def profile():
    token = request.args.get('token')
    spotify.token["access_token"] = token
    return spotify.get(protected_resource).content


if __name__ == '__main__':
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='root.pem')
    context.load_cert_chain(certfile='serv.crt', keyfile='serv.key')
    app.run('localhost', ssl_context=context, debug=True)

