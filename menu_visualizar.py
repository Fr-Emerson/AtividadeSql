

import streamlit as st
from database import consultar

def exibir_menu_visualizar():
   
    st.header("👥 Visualizar Dados")
    
    usuarios = consultar("SELECT id_usuario, nome FROM usuario;")
    
    usuario_selecionado = st.sidebar.selectbox(
        "Selecione um usuário",
        options=usuarios["nome"].tolist() if not usuarios.empty else []
    )
    
    if not usuarios.empty:
        _exibir_biblioteca(usuario_selecionado)
        _exibir_total_gasto(usuario_selecionado)
        _exibir_amigos(usuario_selecionado)
        _exibir_wishlist(usuario_selecionado)
        _exibir_jogos_populares()

def _exibir_biblioteca(usuario_selecionado):

    st.subheader(f"🎮 Biblioteca de {usuario_selecionado}")
    
    query_biblioteca = """
        SELECT j.nome AS Jogo, 
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

def _exibir_total_gasto(usuario_selecionado):
    
    st.subheader("💰 Total gasto")
    
    try:
        totais_df = consultar("SELECT * FROM vw_compras_totais;")
        total_usuario = totais_df.loc[
            totais_df["nome_usuario"] == usuario_selecionado, 
            "total_gasto"
        ].values[0]
        st.metric("Total gasto", f"R$ {total_usuario:.2f}")
    except Exception:
        st.warning("⚠️ View 'vw_compras_totais' não encontrada.")

def _exibir_jogos_populares():
    st.subheader("📈 Jogos mais populares")
    
    top_jogos_query = """
        SELECT j.nome AS Jogo, 
               COUNT(b.id_usuario) AS 'Usuários que possuem'
        FROM Biblioteca b
        JOIN jogo j ON j.id_jogo = b.id_jogo
        GROUP BY j.id_jogo
        ORDER BY COUNT(b.id_usuario) DESC
        LIMIT 5;
    """
    
    st.dataframe(consultar(top_jogos_query))

def _exibir_amigos(usuario_selecionado):
   
    st.subheader(f"🥸 Amigos de {usuario_selecionado}")
    
    try:
        query_amigos = """
            SELECT amigo AS Amigo,
                   data_amizade AS 'Amigos desde'
            FROM vw_amigos_usuario
            WHERE usuario = ?;
        """
        
        amigos_df = consultar(query_amigos, (usuario_selecionado,))
        
        if not amigos_df.empty:
            st.dataframe(amigos_df, use_container_width=True)
        else:
            st.info("Nenhum amigo adicionado ainda.")
            
    except Exception as e:
        st.warning("⚠️ View 'vw_amigos_usuario' não encontrada.")


def _exibir_wishlist(usuario_selecionado):
    """Exibe a wishlist do usuário com total"""
    st.subheader(f"⭐ Wishlist de {usuario_selecionado}")
    
    try:
        query_wishlist = """
            SELECT jogo AS Jogo,
                   preco AS Preço,
                   data_adicionado AS 'Adicionado em'
            FROM vw_wishlist_usuario
            WHERE usuario = ?;
        """
        
        wishlist_df = consultar(query_wishlist, (usuario_selecionado,))
        
        if not wishlist_df.empty:
            # Mostra a tabela
            st.dataframe(wishlist_df, use_container_width=True, hide_index=True)
            
            # Calcula e mostra o total
            total_wishlist = wishlist_df['Preço'].sum()
            st.success(f"💰 **Valor total da Wishlist: R$ {total_wishlist:.2f}**")
        else:
            st.info("📋 Nenhum jogo na wishlist.")
            st.caption("💡 Adicione jogos na seção 'Adicionar à Wishlist'")
            
    except Exception as e:
        st.warning("⚠️ Erro ao carregar wishlist")
        st.caption(f"Detalhes: {str(e)}")