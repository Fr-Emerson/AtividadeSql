#Feito por Francisco Emerson e Kaua Muniz
import sqlite3 as sq


connect = sq.connect("Steam.db")
cursor = connect.cursor()

cursor.execute(
    """
    DELETE FROM jogo
    WHERE nome = 'FIFA 25'
    """
)

connect.commit()
print("Jogo excluido com sucesso!")