import http.client 

while True:
    command = input('comando > ')

    command_split = command.split()

    operation = None
    resource = None
    body = None

    if command_split[0] == 'EXIT':
        break
    elif command_split[0] == 'LIST':
        operation = 'GET'
        resource = '/lista/list'
    elif command_split[0] == 'APPEND':
        operation = 'POST'
        resource = f'/lista/append/{command_split[1]}'
    elif command_split[0] == 'CLEAR':
        operation = 'POST'
        resource = '/lista/clear'
    elif command_split[0] == 'CONTAINS':
        operation = 'GET'
        resource = f'/lista/contains/{command_split[1]}'
    elif command_split[0] == 'UPDATE':
        operation = 'PUT'
        resource = f'/lista/update/{command_split[1]}'
        body = command_split[2]
    elif command_split[0] == 'REMOVE':
        operation = 'DELETE'
        resource = f'/lista/remove/{command_split[1]}'

    if operation is not None and resource is not None:
        connection = http.client.HTTPConnection('localhost', 8888)
        connection.request(operation, resource, body)

        response = connection.getresponse()

        print(f'{response.status}, {response.reason} \n{response.read().decode()}')