import streamlit as st
import pandas as pd
import duckdb
import mysql.connector  # Conexão com MySQL
import os
import plotly.express as px
from mysql.connector import Error

# Configuração inicial do Streamlit
st.title("Dashboard de Jogos")
st.sidebar.title("Filtros")

# 1. Carregar dados do DuckDB
@st.cache_data
def load_duckdb_data():
    duckdb_path = os.path.join("duckdb", "steam_games.duckdb")
    con = duckdb.connect(duckdb_path)
    query = "SELECT * FROM steam_games"
    return con.execute(query).df()

steam_data = load_duckdb_data()
st.subheader("Dados do Steam (DuckDB)")
st.dataframe(steam_data)

# 2. Carregar dados do MySQL
@st.cache_data
# Função para carregar dados do MySQL
def load_mysql_data():
    try:
        print("Iniciando conexão com o banco MySQL...")  # Debug
        connection = mysql.connector.connect(
            host="localhost",  # Verifique se é o correto
            user="root",       # Confirme o usuário
            password="lioup098",       # Insira a senha correta
            database="game_db"  # Verifique o nome do banco de dados
        )
        
        if connection.is_connected():
            print("Conexão estabelecida com sucesso!")  # Debug
            
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM games LIMIT 10;"  # Query de exemplo
            print(f"Executando query: {query}")  # Debug
            
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"Número de registros recuperados: {len(result)}")  # Debug
            for row in result:
                print(row)  # Debug: Ver os dados recuperados
            
            return result

    except Error as e:
        print(f"Erro durante a conexão ou execução: {e}")  # Debug
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexão com o banco MySQL foi encerrada.")  # Debug

            
games_data = load_mysql_data()
st.subheader("Dados dos Jogos (MySQL)")
st.dataframe(games_data)

# 3. Gráficos Interativos
# Gráfico 1: Receita por Jogo (DuckDB)
st.subheader("Receita por Jogo (Steam)")
fig1 = px.bar(steam_data, x="name", y="revenue", title="Receita dos Jogos do Steam")
st.plotly_chart(fig1)

# Gráfico 2: Vendas Globais por Jogo (MySQL)
st.subheader("Vendas Globais por Jogo")
fig2 = px.bar(games_data, x="name", y="global_sales", title="Vendas Globais (Games)")
st.plotly_chart(fig2)

# 4. Filtros Interativos
st.sidebar.subheader("Filtrar por Gênero (Games)")
selected_genre = st.sidebar.selectbox("Selecione o Gênero", games_data["genre"].unique())
filtered_data = games_data[games_data["genre"] == selected_genre]
st.write(f"Jogos do gênero: {selected_genre}")
st.dataframe(filtered_data)

# Gráfico com os dados filtrados
fig3 = px.bar(filtered_data, x="name", y="global_sales", title=f"Vendas Globais - {selected_genre}")
st.plotly_chart(fig3)
