import streamlit as st
import sqlite3
import pandas as pd

# 🧠 Função auxiliar para conectar ao banco
@st.cache_data
def conectar_banco():
    return sqlite3.connect("Steam.db")

# 🧠 Função para rodar consultas e retornar DataFrame
def consultar(query):
    conn = conectar_banco()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 🎨 Título da aplicação
st.set_page_config(page_title="Mini Steam", page_icon="🎮")
st.title("🎮 Mini Steam — Visualização de Dados")

# 🧑 Lista de usuários
st.sidebar.header("👥 Usuários")
usuarios = consultar("SELECT id_usuario, nome FROM usuario;")

usuario_selecionado = st.sidebar.selectbox(
    "Selecione um usuário",
    options=usuarios["nome"].tolist()
)

# 📊 Exibir biblioteca do usuário selecionado
st.subheader(f"🎮 Biblioteca de {usuario_selecionado}")

query_biblioteca = f"""
SELECT 
    j.nome AS Jogo,
    j.preco AS Preço,
    j.ano_lancamento AS 'Ano de Lançamento',
    j.criador AS Criador
FROM Biblioteca b
JOIN usuario u ON u.id_usuario = b.id_usuario
JOIN jogo j ON j.id_jogo = b.id_jogo
WHERE u.nome = '{usuario_selecionado}';
"""

biblioteca_df = consultar(query_biblioteca)
st.dataframe(biblioteca_df)

# 💰 Exibir total gasto (usando view se existir)
st.subheader("💰 Total gasto")

try:
    totais_df = consultar("SELECT * FROM vw_compras_totais;")
    total_usuario = totais_df.loc[
        totais_df["nome_usuario"] == usuario_selecionado, "total_gasto"
    ].values[0]
    st.metric("Total gasto", f"R$ {total_usuario:.2f}")
except Exception:
    st.warning("A view 'vw_compras_totais' não foi encontrada. Execute o script SQL para criá-la.")

# 🏆 Estatísticas gerais
st.subheader("📈 Jogos mais populares")
top_jogos_query = """
SELECT 
    j.nome AS Jogo,
    COUNT(b.id_usuario) AS 'Usuários que possuem'
FROM Biblioteca b
JOIN jogo j ON j.id_jogo = b.id_jogo
GROUP BY j.id_jogo
ORDER BY COUNT(b.id_usuario) DESC
LIMIT 5;
"""
st.dataframe(consultar(top_jogos_query))
