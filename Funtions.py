import streamlit as st
import sqlite3
import pandas as pd


@st.cache_resource
def conectar_banco():
    return sqlite3.connect("Steam.db", check_same_thread=False)

def consultar(query, params=None):
    conn = conectar_banco()
    df = pd.read_sql_query(query, conn, params=params)
    return df

def obter_usuarios():
    return consultar("SELECT id_usuario, nome FROM usuario;")


def obter_biblioteca(nome_usuario):
    query = """
    SELECT 
        j.nome AS Jogo,
        j.preco AS Preço,
        j.ano_lancamento AS 'Ano de Lançamento',
        j.criador AS Criador
    FROM Biblioteca b
    JOIN usuario u ON u.id_usuario = b.id_usuario
    JOIN jogo j ON j.id_jogo = b.id_jogo
    WHERE u.nome = ?;
    """
    return consultar(query, params=(nome_usuario,))


def obter_total_gasto(nome_usuario):
    try:
        totais_df = consultar("SELECT * FROM vw_compras_totais;")
        total = totais_df.loc[
            totais_df["nome_usuario"] == nome_usuario, "total_gasto"
        ].values
        return total[0] if len(total) > 0 else 0.0
    except Exception:
        return None


def obter_jogos_populares(limite=5):
    query = f"""
    SELECT 
        j.nome AS Jogo,
        COUNT(b.id_usuario) AS 'Usuários que possuem'
    FROM Biblioteca b
    JOIN jogo j ON j.id_jogo = b.id_jogo
    GROUP BY j.id_jogo
    ORDER BY COUNT(b.id_usuario) DESC
    LIMIT {limite};
    """
    return consultar(query)