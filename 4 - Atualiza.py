import sqlite3 as sq

connect = sq.connect("Steam.db")
cursor = connect.cursor()

connect.execute(
    """
    UPDATE jogo when 
    """
)

connect.commit()
print("Dados atualizados com sucesso")