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

def executar(query, params=None):
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    cur.close()

st.set_page_config(page_title="Mini Steam", page_icon="🎮")
st.title("🎮 Mini Steam — Painel de Administração")

# 🧭 Menu lateral
menu = st.sidebar.radio(
    "📋 Menu",
    ["Visualizar Dados", "Cadastrar Usuário", "Cadastrar Jogo", "Adicionar à Biblioteca", "Deletar"]
)

# =====================================================================================
# VISUALIZAR DADOS
# =====================================================================================
if menu == "Visualizar Dados":
    st.header("👥 Visualizar Dados")

    usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
    usuario_selecionado = st.sidebar.selectbox(
        "Selecione um usuário",
        options=usuarios["nome"].tolist() if not usuarios.empty else []
    )

    if not usuarios.empty:
        # Biblioteca do usuário
        st.subheader(f"🎮 Biblioteca de {usuario_selecionado}")
        query_biblioteca = """
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
        biblioteca_df = consultar(query_biblioteca, (usuario_selecionado,))
        st.dataframe(biblioteca_df)

        # Total gasto
        st.subheader("💰 Total gasto")
        try:
            totais_df = consultar("SELECT * FROM vw_compras_totais;")
            total_usuario = totais_df.loc[
                totais_df["nome_usuario"] == usuario_selecionado, "total_gasto"
            ].values[0]
            st.metric("Total gasto", f"R$ {total_usuario:.2f}")
        except Exception:
            st.warning("⚠️ View 'vw_compras_totais' não encontrada.")

    # Jogos mais populares
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

# =====================================================================================
# CADASTRAR USUÁRIO
# =====================================================================================
elif menu == "Cadastrar Usuário":
    st.header("👤 Cadastrar Novo Usuário")
    nome = st.text_input("Nome do usuário:")
    senha = st.text_input("Senha:", type="password")

    if st.button("Cadastrar Usuário"):
        if nome and senha:
            try:
                executar("INSERT INTO usuario (nome, senha) VALUES (?, ?);", (nome, senha))
                st.success(f"✅ Usuário '{nome}' cadastrado com sucesso!")
            except sqlite3.IntegrityError:
                st.error("⚠️ Esse nome de usuário já existe!")
        else:
            st.warning("Preencha todos os campos!")

# =====================================================================================
# CADASTRAR JOGO
# =====================================================================================
elif menu == "Cadastrar Jogo":
    st.header("🎮 Cadastrar Novo Jogo")
    nome = st.text_input("Nome do jogo:")
    preco = st.number_input("Preço (R$):", min_value=0.0, step=0.1)
    ano = st.number_input("Ano de lançamento:", min_value=1970, max_value=2025, step=1)
    classificacao = st.number_input("Classificação indicativa:", min_value=0, max_value=18, step=1)
    criador = st.text_input("Criador:")
    nota = st.slider("Nota do jogo:", 0, 10, 5)

    if st.button("Cadastrar Jogo"):
        if nome and criador:
            executar(
                """
                INSERT INTO jogo (nome, preco, ano_lancamento, classificacao, criador, nota)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (nome, preco, ano, classificacao, criador, nota)
            )
            st.success(f"✅ Jogo '{nome}' cadastrado com sucesso!")
        else:
            st.warning("Preencha pelo menos o nome e o criador!")

# =====================================================================================
# ADICIONAR JOGO À BIBLIOTECA
# =====================================================================================
elif menu == "Adicionar à Biblioteca":
    st.header("📚 Adicionar Jogo à Biblioteca")

    usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
    jogos = consultar("SELECT id_jogo, nome FROM jogo;")

    if usuarios.empty or jogos.empty:
        st.warning("⚠️ Cadastre pelo menos um usuário e um jogo antes de usar esta função.")
    else:
        usuario = st.selectbox("Usuário:", usuarios["nome"])
        jogo = st.selectbox("Jogo:", jogos["nome"])

        if st.button("Adicionar à Biblioteca"):
            id_usuario = int(usuarios.loc[usuarios["nome"] == usuario, "id_usuario"].values[0])
            id_jogo = int(jogos.loc[jogos["nome"] == jogo, "id_jogo"].values[0])
            try:
                executar("INSERT INTO Biblioteca (id_usuario, id_jogo) VALUES (?, ?);", (id_usuario, id_jogo))
                st.success(f"✅ '{jogo}' adicionado à biblioteca de {usuario}!")
            except sqlite3.IntegrityError:
                st.error("⚠️ Esse jogo já está na biblioteca desse usuário!")


# =====================================================================================
# DELETAR
# =====================================================================================
elif menu == "Deletar":
    st.header("🗑️ Deletar Registros")

    tipo = st.selectbox("Selecione o tipo de registro a deletar:", ["Usuário", "Jogo", "Biblioteca"])

    if tipo == "Usuário":
        usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
        if not usuarios.empty:
            usuario = st.selectbox("Selecione o usuário:", usuarios["nome"])
            if st.button("Deletar Usuário"):
                executar("DELETE FROM usuario WHERE nome = ?;", (usuario,))
                st.success(f"✅ Usuário '{usuario}' deletado!")
        else:
            st.info("Nenhum usuário cadastrado.")

    elif tipo == "Jogo":
        jogos = consultar("SELECT id_jogo, nome FROM jogo;")
        if not jogos.empty:
            jogo = st.selectbox("Selecione o jogo:", jogos["nome"])
            if st.button("Deletar Jogo"):
                executar("DELETE FROM jogo WHERE nome = ?;", (jogo,))
                st.success(f"✅ Jogo '{jogo}' deletado!")
        else:
            st.info("Nenhum jogo cadastrado.")

    elif tipo == "Biblioteca":
        usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
        jogos = consultar("SELECT id_jogo, nome FROM jogo;")
        if usuarios.empty or jogos.empty:
            st.info("Nenhum dado encontrado.")
        else:
            usuario = st.selectbox("Usuário:", usuarios["nome"])
            jogo = st.selectbox("Jogo:", jogos["nome"])
            if st.button("Remover da Biblioteca"):
                id_usuario = usuarios.loc[usuarios["nome"] == usuario, "id_usuario"].values[0]
                id_jogo = jogos.loc[jogos["nome"] == jogo, "id_jogo"].values[0]
                executar("DELETE FROM Biblioteca WHERE id_usuario = ? AND id_jogo = ?;", (id_usuario, id_jogo))
                st.success(f"✅ '{jogo}' removido da biblioteca de {usuario}!")
