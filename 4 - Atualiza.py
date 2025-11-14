#Feito por Francisco Emerson e Kaua Muniz
import sqlite3 as sq

connect = sq.connect("Steam.db")
cursor = connect.cursor()

connect.execute(
    """
    UPDATE jogo 
    SET preco = 47.99
    WHERE nome = 'Far Cry 3'
    """
    
)

connect.execute(
    """
    UPDATE jogo
    SET preco = 95.59
    WHERE nome = 'GTA V'
    """
)

connect.execute(
    """
    UPDATE jogo
    SET preco = 7.49
    WHERE nome = 'Hotline Miami 2: Wrong Number'
    """
)



connect.commit()
print("Preços atualizados com sucesso!")