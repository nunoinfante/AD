README

O objetivo geral do programa e concretizar um gestor de bloqueios a recursos para leituras e escritas, onde o seu propósito e controlar o acesso a um conjunto de recursos partilhados  num  sistema  distribuido.

EXECUTAR SERVIDOR:

lock_server.py <IP/hostname> <porto> <tempo de concessão (segundos)> <N recursos> <K bloqueios maximos>
IP/hostname - IP ou hostname onde o servidor fornecera os recursos
porto - porto TCP onde escutara por pedidos de ligacao
N recursos - número de recursos que serão geridos pelo servido
K bloqueios maximos - número de bloqueios permitidos em cada recurso
Exemplo de utilizacao - "python3 lock_server.py localhost 9999 4 3"

EECUTAR CLIENTE:

lock_client.py <id> <IP/hostname> <port>
id - o id unico do cliente
IP/hostname . o IP ou hostname do servidor que fornece os recursos
port - o porto TCP onde o servidor recebe pedidos de ligacao
Exemplo de utilizacao - "python3 lock_client.py 1 localhost 9999"

Comandos disponiveis:

"LOCK" - Bloqueia o recurso escolhido atraves do seu id para escrita(opcao "W") ou leitura(opcao "R") por um tempo limite especificado.
Devolve "OK" se bloquear o recurso, "NOK" caso não bloqueie e "UNKNOWN RESOURCE" caso o recurso nao exista.
Exemplo de utilizacao - "LOCK W 0 30"

"UNLOCK" - Remove um bloqueio de leitura (opcao "R") ou escrita (opcao "W") registado num determinado recurso para o cliente que está a enviar o pedido. 
Devolve "OK" se desbloquear o recurso, "NOK" caso não desbloqueie e "UNKNOWN RESOURCE" caso o recurso nao exista.
Exemplo de utilizacao - "UNLOCK W 1"

"STATUS" - O servidor retorna o estado do recurso solicitado (estados possiveis: UNLOCKED, LOCKED-W, LOCKED-R, DISABLED)
Exemplo de utilizacao - "STATUS 1"

"STATS" - e utilizado para obter outras informacoes sobre o servidor de bloqueios e possui 3 formas dependendo da opcao("K", "N" ou "D").
"K"-> o servidor retorna o número de bloqueios de escrita realizados no recurso especificado
"N"-> o servidor retorna o número total de recursos que se encontram disponiveis atualmente
"D"-> o servidor retorna o número total de recursos quese encontram desabilitados atualmente
Exemplo de utilizacao - "STATS N"

"PRINT" - Representacao do estado de todos os recursos.
Utilizacao - "PRINT"

"SLEEP" - faz com que o cliente "adormeca" durante um determinado tempo (em segundos). Ou seja, o cliente esperará este tempo antes de interpretar o próximo comando.
Exemplo de utilizacão - "SLEEP 3"

"EXIT" - permite ao utilizador terminar o cliente.
Utilizacão - "EXIT"


