from requests_oauthlib import OAuth2Session
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Credenciais da app cliente registada no Github (https://github.com/settings/applications/new)
client_id = 'bla'
client_secret = 'bla'

# URIs do github para obtencao do authorization_code, do token, de callback e do recurso protegido
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
redirect_uri = 'http://localhost'
protected_resource = 'https://api.github.com/user'
github = OAuth2Session(client_id, redirect_uri=redirect_uri)

# Pedido do authorization_code ao servidor de autorização (e dono do recuro a aceder)
authorization_url, state = github.authorization_url(authorization_base_url)
print('Aceder ao link (via browser) para obter a autorizacao,', authorization_url)

# Obter o authorization_code do servidor vindo no URL de redireccionamento
url_response = input(' insira o URL devolvido no browser e cole aqui:')

# Obtencao do token
github.fetch_token(token_url, client_secret=client_secret,
                   authorization_response=url_response)

# Acesso a um recurso protegido
r = github.get(protected_resource)
print(r.content.decode())
