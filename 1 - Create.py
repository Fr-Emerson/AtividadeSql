import sqlite3 as sq

connect = sq.connect("Steam.db")
cursor = connect.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS usuario(
        id_usuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    );
    """   
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS jogo(
        id_jogo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL,
        ano_lancamento INTEGER,
        classificacao INTEGER,
        criador TEXT NOT NULL,
        nota INTEGER
    );
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Biblioteca(
        id_usuario INTEGER,
        id_jogo INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
        FOREIGN KEY (id_jogo) REFERENCES jogo(id_jogo)
    )
    """
)

connect.close()
print("A tabela foi criada")
