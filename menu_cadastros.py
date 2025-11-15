# menu_cadastros.py
# Módulo com as funcionalidades de cadastro

import streamlit as st
import sqlite3
from database import executar

def exibir_menu_cadastrar_usuario():
    """Exibe o menu de cadastro de usuário"""
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

def exibir_menu_cadastrar_jogo():
    """Exibe o menu de cadastro de jogo"""
    st.header("🎮 Cadastrar Novo Jogo")
    
    nome = st.text_input("Nome do jogo:")
    preco = st.number_input("Preço (R$):", min_value=0.0, step=0.1)
    ano = st.number_input("Ano de lançamento:", min_value=1970, max_value=2025, step=1)
    classificacao = st.number_input("Classificação indicativa:", min_value=0, max_value=18, step=1)
    criador = st.text_input("Criador:")
    nota = st.slider("Nota do jogo:", 0, 100, 50)
    
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

def exibir_menu_adicionar_biblioteca():
    """Exibe o menu para adicionar jogos à biblioteca de um usuário"""
    st.header("📚 Adicionar Jogo à Biblioteca")
    
    from database import consultar
    
    usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
    jogos = consultar("SELECT id_jogo, nome FROM jogo;")
    
    if usuarios.empty or jogos.empty:
        st.warning("⚠️ Cadastre pelo menos um usuário e um jogo antes de usar esta função.")
        return
    
    usuario = st.selectbox("Usuário:", usuarios["nome"])
    jogo = st.selectbox("Jogo:", jogos["nome"])
    
    if st.button("Adicionar à Biblioteca"):
        id_usuario = int(usuarios.loc[usuarios["nome"] == usuario, "id_usuario"].values[0])
        id_jogo = int(jogos.loc[jogos["nome"] == jogo, "id_jogo"].values[0])
        
        try:
            executar(
                "INSERT INTO Biblioteca (id_usuario, id_jogo) VALUES (?, ?);", 
                (id_usuario, id_jogo)
            )
            st.success(f"✅ '{jogo}' adicionado à biblioteca de {usuario}!")
        except sqlite3.IntegrityError:
            st.error("⚠️ Esse jogo já está na biblioteca desse usuário!")

def exibir_menu_adicionar_wishlist():
    """Exibe o menu para adicionar jogos à wishlist de um usuário"""
    st.header("⭐ Adicionar Jogo à Wishlist")
    
    from database import consultar
    from datetime import datetime
    
    usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
    jogos = consultar("SELECT id_jogo, nome FROM jogo;")
    
    if usuarios.empty or jogos.empty:
        st.warning("⚠️ Cadastre pelo menos um usuário e um jogo antes de usar esta função.")
        return
    
    usuario = st.selectbox("Usuário:", usuarios["nome"])
    jogo = st.selectbox("Jogo:", jogos["nome"])
    
    if st.button("Adicionar à Wishlist"):
        id_usuario = int(usuarios.loc[usuarios["nome"] == usuario, "id_usuario"].values[0])
        id_jogo = int(jogos.loc[jogos["nome"] == jogo, "id_jogo"].values[0])
        data_atual = datetime.now().strftime("%Y-%m-%d")
        
        try:
            executar(
                "INSERT INTO wishlist (id_usuario, id_jogo, data_adicionado) VALUES (?, ?, ?);", 
                (id_usuario, id_jogo, data_atual)
            )
            st.success(f"✅ '{jogo}' adicionado à wishlist de {usuario}!")
        except sqlite3.IntegrityError:
            st.error("⚠️ Esse jogo já está na wishlist desse usuário!")

def exibir_menu_adicionar_amigo():

    st.header("👥 Adicionar Amizade")
    
    from database import consultar
    from datetime import datetime
    
    usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
    
    if usuarios.empty or len(usuarios) < 2:
        st.warning("⚠️ Cadastre pelo menos dois usuários antes de usar esta função.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        usuario1 = st.selectbox("Primeiro usuário:", usuarios["nome"], key="user1")
    
    with col2:
        # Filtrar para não mostrar o mesmo usuário
        usuarios_filtrados = usuarios[usuarios["nome"] != usuario1]["nome"].tolist()
        usuario2 = st.selectbox("Segundo usuário:", usuarios_filtrados, key="user2")
    
    if st.button("Adicionar Amizade"):
        id_usuario1 = int(usuarios.loc[usuarios["nome"] == usuario1, "id_usuario"].values[0])
        id_usuario2 = int(usuarios.loc[usuarios["nome"] == usuario2, "id_usuario"].values[0])
        data_atual = datetime.now().strftime("%Y-%m-%d")
        
        try:
            executar(
                "INSERT INTO amigos (id_usuario1, id_usuario2, data) VALUES (?, ?, ?);", 
                (id_usuario1, id_usuario2, data_atual)
            )
            st.success(f"✅ {usuario1} e {usuario2} agora são amigos!")
        except sqlite3.IntegrityError:
            st.error("⚠️ Essa amizade já existe!")