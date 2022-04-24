from kazoo.client import KazooClient
import time

def critical_zone():
    print('Comecei a executar a zona crítica')
    time.sleep(10)
    print('Terminei a execução da zona crítica')

zh = KazooClient()
zh.start()

zh.ensure_path('/LOCKS')
zid = zh.create('/LOCKS/L-', ephemeral=True, sequence=True)

while True:
    children = zh.get_children('/LOCKS')
    min_id = f'/LOCKS/{min(children)}'

    if min_id == zid:
        critical_zone()
        zh.delete(zid)
        break
    else:
        print('Children: ', children)
        time.sleep(1)
        
zh.stop()
zh.close()