#Feito por Francisco Emerson e Kaua Muniz
import sqlite3 as sq

connect = sq.connect("Steam.db")
cursor = connect.cursor()

cursor.execute(
    """
        INSERT INTO usuario(nome, senha)
        VALUES 
        ('WolfgangGrimmer','wolfgang1234'),
        ('NoobHunter', '12345678novesfora'),
        ('Carlinhos2050','cleideCavalos'),
        ('Bigm_duasFase', 'mapadeKarnaughultra'),
        ('TedK','industrial1234'),
        ('moacirBorracharia','sigmabasedincel1'),
        ('PolPot','camboja123');
    """
)


cursor.execute(
    """
        INSERT INTO jogo(nome, preco, ano_lancamento, classificacao, criador, nota)
        VALUES
        ('Hotline miami', 3.20, 2012, 100, 'Dennaton Games', 100),
        ('Katana Zero', 46.99, 2019, 14, 'Askiisoft', 83),
        ('FIFA 25', 400.30, 2024, 12, 'EA', 30),
        ('Ultrakill', 59.99, 2020, 12, 'Arsi Patala', 100),
        ('Hotline Miami 2: Wrong Number', 7.00, 2015, 18, 'Dennaton Games', 100),
        ('Dead Cells', 23.45, 2018, 14, 'Motion Twin', 95),
        ('Devil May Cry HD Collection', 59.99, 2018, 14, 'Capcom', 95),
        ('GTA V', 80.00, 2013, 18, 'Rockstar Games', 99),
        ('Far Cry 3', 50.00, 2012, 16, 'Ubisoft', 95);
    """
)
cursor.execute(
    """
        INSERT INTO Biblioteca (id_usuario, id_jogo) VALUES
        (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 2), (2, 3), (2, 4), (2, 5),
        (3, 3), (3, 4), (3, 5), (3, 6),
        (4, 4), (4, 5), (4, 6), (4, 7),
        (5, 5), (5, 6), (5, 7), (5, 8),
        (6, 6), (6, 7), (6, 8), (6, 9),
        (7, 1), (7, 7), (7, 8), (7, 9);
    """
)
connect.commit()
connect.close()

print("Dados inseridos na tabela")
