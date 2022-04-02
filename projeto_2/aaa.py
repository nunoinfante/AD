def lock(option, recurso, tempo, client_id):
    send('LOCK', option, recurso, tempo, client_id)

def send(command, *args):
    msg = [command]
    msg.extend(args)
    print(msg)

send('LOCK', 'W')