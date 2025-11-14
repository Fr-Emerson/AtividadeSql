#Feito por Francisco Emerson e Kaua Muniz
import sqlite3 as sq

connect = sq.connect("Steam.db")
cursor = connect.cursor()


cursor.execute(
        """
        Create VIEW IF NOT EXISTS vw_nomeUsuario_jogo_e_preco AS
        SELECT
            u.nome AS usuario,
            j.nome AS jogo,
            j.preco AS preco
            FROM Biblioteca b
            JOIN usuario u ON b.id_usuario = u.id_usuario
            JOIN jogo j ON b.id_jogo = j.id_jogo;
        """
    )

cursor.execute(
    """
    Create VIEW IF NOT EXISTS vw_Jogo_preco_Classificacao_nota as
    select
        j.nome as Jogo,
        j.preco as Preco,
        j.classificacao as Classificacao,
        j.nota as Nota
    from jogo j
    """
)
cursor.execute(
    """
    CREATE VIEW IF NOT EXISTS vw_compras_totais AS
    SELECT 
        u.nome AS nome_usuario,
        ROUND(SUM(j.preco), 2) AS total_gasto
    FROM Biblioteca b
    JOIN usuario u ON u.id_usuario = b.id_usuario
    JOIN jogo j ON j.id_jogo = b.id_jogo
    GROUP BY u.id_usuario
    ORDER BY total_gasto DESC;
    """
)
cursor.execute(
    """
    CREATE VIEW IF NOT EXISTS vw_amigos_usuario AS
    SELECT
        u1.nome AS usuario,
        u2.nome AS amigo,
        a.data AS data_amizade
    FROM amigos a
    JOIN usuario u1 ON a.id_usuario1 = u1.id_usuario
    JOIN usuario u2 ON a.id_usuario2 = u2.id_usuario;
    """
)