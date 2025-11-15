


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