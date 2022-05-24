EXECUTAR SERVIDOR:
  python3 server.py

EXECUTAR CLIENTE:
  python3 client.py

OBSERVACOES:
- Necessário o ficheiro proj4.sql
- Os comandos são case-sensitive

COMANDOS:
    CREATE:
        1) CREATE UTILIZADOR <nome> <senha> 
        2) CREATE ARTISTA <id_spotify>
        3) CREATE MUSICA <id_spotify>
        4) CREATE <id_user> <id_musica> <avaliacao> (avaliacao = M | m | S | B | MB)

    READ/DELETE:
        1) READ/DELETE UTILIZADOR
        2) READ/DELETE ARTISTA
        3) READ/DELETE MUSICA
        4) READ/DELETE ALL <UTILIZADORES | ARTISTAS | MUSICAS>
        5) READ/DELETE ALL MUSICAS_A <id_artista>
        6) READ/DELETE ALL MUSICAS_U <id_user> 
        7) READ/DELETE ALL MUSICAS <avaliacao> (avaliacao = M | m | S | B | MB)

    UPDATE:
        1) UPDATE MUSICA <id_musica> <avaliacao> <id_user> (avaliacao = M | m | S | B | MB)
        2) UPDATE UTILIZADOR <id_user> <password>

