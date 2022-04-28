import requests

CLIENT_ID = '7245356318a948f4bed0bd361882b36f'
CLIENT_SECRET = '206a7ffa6ef74f58b49098b71f35fad3'

AUTH_URL = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(AUTH_URL, {'grant_type': 'client_credentials',
                                        'client_id': CLIENT_ID,
                                        'client_secret': CLIENT_SECRET,
                                        })

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

print(access_token)

headers = {
    'Authorization': f'Bearer {access_token}'
}



BASE_URL = 'https://api.spotify.com/v1/'

artist_id = '36QJpDe2go2KgaRleHCDTp'

r = requests.get(BASE_URL + 'search?q=Chris%20Dea', headers=headers, params={'type': 'artist', 'limit': 4})

d = r.json()
print(d['artists']['items'][0]['uri'])

for a in d['artists']['items'][0]:
   print(d['artists']['items'][0]['name'])

# s = 'CREATE ARTIST Sam The Kid'
# print(s)
# s = s.split(' ', 2)[2].replace(' ', '%20')
# print(s)

comando = input('comando > ')
comando_split = comando.split()
print(f'http://localhost:5000/utilizadores/{comando_split[2]}/avaliacoes')