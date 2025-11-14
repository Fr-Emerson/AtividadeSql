#Feito por Francisco Emerson e Kaua Muniz
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
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS wishlist (
        id_usuario INTEGER NOT NULL,
        id_jogo INTEGER NOT NULL,
        data_adicionado TEXT,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
        FOREIGN KEY (id_jogo) REFERENCES jogo(id_jogo)
    );
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS amigos (
        id_usuario1 INTEGER NOT NULL,
        id_usuario2 INTEGER NOT NULL,
        data TEXT,
    FOREIGN KEY (id_usuario1) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_usuario2) REFERENCES usuario(id_usuario)
);

    """
)
connect.close()
print("A tabela foi criada")
