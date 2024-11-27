import streamlit as st
import pandas as pd
import duckdb
import os
import plotly.express as px
from rawg_api import fetch_games_data

# Configuração inicial do Streamlit
st.title("Dashboard de Jogos")
st.sidebar.title("Filtros")

# Função para carregar dados do DuckDB
@st.cache_data
def load_duckdb_data(table_name):
    """
    Função para carregar os dados de uma tabela específica no banco DuckDB.
    """
    try:
        duckdb_path = os.path.join("duckdb", "games_relational.duckdb")
        con = duckdb.connect(duckdb_path)
        query = f"SELECT * FROM {table_name}"
        return con.execute(query).df()
    except Exception as e:
        st.error(f"Erro ao carregar dados da tabela '{table_name}' no DuckDB: {e}")
        return pd.DataFrame()

# Função para carregar dados da API RAWG
@st.cache_data
def load_rawg_data():
    """
    Função para carregar os dados da API RAWG.
    """
    api_data = fetch_games_data(page=1, page_size=10)
    if api_data and "results" in api_data:
        return pd.DataFrame(api_data["results"])
    else:
        st.error("Erro ao buscar dados da API RAWG.")
        return pd.DataFrame()

# Carregar os dados
steam_data = load_duckdb_data("steam_games")
games_data = load_duckdb_data("games")
rawg_data = load_rawg_data()

# Exibir dados da API RAWG
st.subheader("Dados da API RAWG")
if not rawg_data.empty:
    st.dataframe(rawg_data)
else:
    st.warning("Nenhum dado encontrado na API RAWG.")

# Exibir dados do Steam
st.subheader("Dados do Steam (DuckDB)")
if not steam_data.empty:
    st.dataframe(steam_data)
else:
    st.warning("Nenhum dado encontrado para a tabela 'steam_games'.")

# Exibir dados dos Jogos
st.subheader("Dados dos Jogos (DuckDB)")
if not games_data.empty:
    st.dataframe(games_data)
else:
    st.warning("Nenhum dado encontrado para a tabela 'games'.")

# Gráficos Interativos
# Gráfico 1: Receita por Jogo (Steam)
if not steam_data.empty:
    st.subheader("Receita por Jogo (Steam)")
    if "name" in steam_data.columns and "revenue" in steam_data.columns:
        fig1 = px.bar(
            steam_data, 
            x="name", 
            y="revenue", 
            title="Receita dos Jogos do Steam",
            labels={"name": "Nome do Jogo", "revenue": "Receita"},
            color="revenue",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig1)
    else:
        st.error("As colunas 'name' e 'revenue' não foram encontradas na tabela 'steam_games'.")

# Gráfico 2: Vendas Globais por Jogo
if not games_data.empty:
    st.subheader("Vendas Globais por Jogo")
    if "Name" in games_data.columns and "Global_Sales" in games_data.columns:
        fig2 = px.bar(
            games_data, 
            x="Name", 
            y="Global_Sales", 
            title="Vendas Globais (Games)",
            labels={"Name": "Nome do Jogo", "Global_Sales": "Vendas Globais"},
            color="Global_Sales",
            color_continuous_scale="Bluered"
        )
        st.plotly_chart(fig2)
    else:
        st.error("As colunas 'Name' e 'Global_Sales' não foram encontradas na tabela 'games'.")

# Filtros Interativos
if not games_data.empty:
    if "Genre" in games_data.columns:
        st.sidebar.subheader("Filtrar por Gênero (Games)")
        selected_genre = st.sidebar.selectbox(
            "Selecione o Gênero",
            games_data["Genre"].dropna().unique()
        )
        filtered_data = games_data[games_data["Genre"] == selected_genre]
        st.write(f"Jogos do gênero: {selected_genre}")
        st.dataframe(filtered_data)

        # Gráfico com os dados filtrados
        if not filtered_data.empty:
            fig3 = px.bar(
                filtered_data, 
                x="Name", 
                y="Global_Sales", 
                title=f"Vendas Globais - {selected_genre}",
                labels={"Name": "Nome do Jogo", "Global_Sales": "Vendas Globais"},
                color="Global_Sales",
                color_continuous_scale="Sunset"
            )
            st.plotly_chart(fig3)
        else:
            st.warning(f"Nenhum dado encontrado para o gênero '{selected_genre}'.")
    else:
        st.error("A coluna 'Genre' não foi encontrada na tabela 'games'.")
