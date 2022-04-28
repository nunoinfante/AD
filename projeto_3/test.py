import requests
import urllib

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
r = requests.get(BASE_URL + 'artists/' + artist_id, headers=headers)
d = r.json()
print(d['name'])


track_id = '4KS15itaFKcYz06iEMw5GO'
r = requests.get(BASE_URL + 'tracks/' + track_id, headers=headers)
d = r.json()
print(d['name'])
# print(d['tracks']['items'][0]['name'])
# print(d['tracks']['items'][0]['id'])
# print(d['tracks']['items'][0]['artists'][0]['name'])
# print(d['tracks']['items'][0]['artists'][0]['id'])

