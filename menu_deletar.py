import streamlit as st
from database import consultar, executar

def exibir_menu_deletar():
    st.header("🗑️ Deletar Registros")
    
    tipo = st.selectbox(
        "Selecione o tipo de registro a deletar:", 
        ["Usuário", "Jogo", "Biblioteca"]
    )
    
    if tipo == "Usuário":
        _deletar_usuario()
    elif tipo == "Jogo":
        _deletar_jogo()
    elif tipo == "Biblioteca":
        _deletar_da_biblioteca()

def _deletar_usuario():
   
    usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
    
    if not usuarios.empty:
        usuario = st.selectbox("Selecione o usuário:", usuarios["nome"])
        
        if st.button("Deletar Usuário"):
            executar("DELETE FROM usuario WHERE nome = ?;", (usuario,))
            st.success(f"✅ Usuário '{usuario}' deletado!")
    else:
        st.info("Nenhum usuário cadastrado.")

def _deletar_jogo():

    jogos = consultar("SELECT id_jogo, nome FROM jogo;")
    
    if not jogos.empty:
        jogo = st.selectbox("Selecione o jogo:", jogos["nome"])
        
        if st.button("Deletar Jogo"):
            executar("DELETE FROM jogo WHERE nome = ?;", (jogo,))
            st.success(f"✅ Jogo '{jogo}' deletado!")
    else:
        st.info("Nenhum jogo cadastrado.")

def _deletar_da_biblioteca():

    usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
    jogos = consultar("SELECT id_jogo, nome FROM jogo;")
    
    if usuarios.empty or jogos.empty:
        st.info("Nenhum dado encontrado.")
        return
    
    usuario = st.selectbox("Usuário:", usuarios["nome"])
    jogo = st.selectbox("Jogo:", jogos["nome"])
    
    if st.button("Remover da Biblioteca"):
        id_usuario = usuarios.loc[usuarios["nome"] == usuario, "id_usuario"].values[0]
        id_jogo = jogos.loc[jogos["nome"] == jogo, "id_jogo"].values[0]
        
        executar(
            "DELETE FROM Biblioteca WHERE id_usuario = ? AND id_jogo = ?;", 
            (id_usuario, id_jogo)
        )
        st.success(f"✅ '{jogo}' removido da biblioteca de {usuario}!")