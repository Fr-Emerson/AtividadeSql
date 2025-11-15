# Feito por Francisco Emerson e Kaua Muniz

import streamlit as st
from menu_visualizar import exibir_menu_visualizar
from menu_cadastros import (
    exibir_menu_cadastrar_usuario,
    exibir_menu_cadastrar_jogo,
    exibir_menu_adicionar_biblioteca,
    exibir_menu_adicionar_amigo,
    exibir_menu_adicionar_wishlist,
    
)
from menu_deletar import exibir_menu_deletar

st.set_page_config(page_title="Mini Steam", page_icon="🎮")
st.title("🎮 Mini Steam — Painel de Administração")

menu = st.sidebar.radio(
    "📋 Menu",
    [
        "Visualizar Dados",
        "Cadastrar Usuário",
        "Cadastrar Jogo",
        "Adicionar à Biblioteca",
        "Adicionar Amigo",
        "Lista de Compras",
        "Deletar"
    ]
)

if menu == "Visualizar Dados":
    exibir_menu_visualizar()

elif menu == "Cadastrar Usuário":
    exibir_menu_cadastrar_usuario()

elif menu == "Cadastrar Jogo":
    exibir_menu_cadastrar_jogo()

elif menu == "Adicionar à Biblioteca":
    exibir_menu_adicionar_biblioteca()
elif menu == "Adicionar Amigo":
   exibir_menu_adicionar_amigo()

elif menu == "Lista de Compras":
    exibir_menu_adicionar_wishlist()
elif menu == "Deletar":
    exibir_menu_deletar()