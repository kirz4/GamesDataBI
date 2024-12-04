import streamlit as st
import pandas as pd
import duckdb
import os
import plotly.express as px
from fetch_rawg_data import fetch_games_data
from process_rawg_data import process_rawg_data  # Importando a função de tratamento

# Função para formatar os valores de vendas
def format_sales(value):
    """Formata os valores de vendas em milhões ou milhares de forma compacta"""
    try:
        value = float(value)
    except ValueError:
        return "N/A"  # Caso o valor não seja numérico, retorna "N/A"
    
    if value >= 1e6:
        return f"{value / 1e6:.1f}M"  # Exibe em milhões
    elif value >= 1e3:
        return f"{value / 1e3:.1f}k"  # Exibe em milhares
    else:
        return f"{value:.0f}"  # Exibe o valor sem arredondamento se for menor que 1.000

# Configuração inicial do Streamlit
st.set_page_config(layout="wide")  # Define o layout como "wide" para maior aproveitamento da tela

st.sidebar.title("Filtros")

# Função para carregar dados do DuckDB
@st.cache_data
def load_duckdb_data(table_name):
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
    api_data = fetch_games_data(page=1, page_size=500)
    if api_data and "results" in api_data:
        return pd.DataFrame(api_data["results"])
    else:
        st.error("Erro ao buscar dados da API RAWG.")
        return pd.DataFrame()

    
# Carregar os dados
steam_data = load_duckdb_data("steam_games")
games_data = load_duckdb_data("games")
rawg_data = load_rawg_data()

# Tratar os dados da RAWG
if not rawg_data.empty:
    rawg_data = process_rawg_data(rawg_data)  # Processar os dados

# Filtros para os gráficos de vendas regionais e gráficos de pizza
region_filter = st.sidebar.selectbox("Escolha a região para o gráfico de vendas", ["NA_Sales", "EU_Sales", "JP_Sales", "Global_Sales"])
game_filter = st.sidebar.selectbox("Escolha um jogo para o gráfico de pizza", rawg_data["name"].unique())

# Certificando-se de que o DataFrame não está vazio
if not steam_data.empty:
    # 1. Maior Nota de Avaliação - Usando a coluna 'reviewScore' de steam_data
    highest_rating = steam_data["reviewScore"].max()

    # 2. Percentual de Jogos Com Avaliação Acima de 8 - Usando a coluna 'reviewScore'
    above_8 = (steam_data["reviewScore"] > 8).sum()
    total_games = len(steam_data)
    percent_above_8 = (above_8 / total_games) * 100 if total_games > 0 else 0

    # 3. Total de Vendas Globais (em milhões) - Calculando baseado em 'copiesSold' e 'price'
    steam_data['calculated_revenue'] = steam_data['copiesSold'] * steam_data['price']
    total_revenue = steam_data['calculated_revenue'].sum() / 1e6  # Convertendo para milhões

    # 4. Jogo Mais Avaliado - Usando o dataset da API Rawg
    if 'ratings_count' in rawg_data.columns:
        most_reviewed_game = rawg_data.loc[rawg_data["ratings_count"].idxmax()]
        most_reviewed_game_name = most_reviewed_game["name"]
        most_reviewed_game_reviews = most_reviewed_game["ratings_count"]
    else:
        most_reviewed_game_name = "Não encontrado"
        most_reviewed_game_reviews = 0

    # 5. Jogo com Menor Avaliação - Usando o dataset da API Rawg
    if 'average_rating' in rawg_data.columns:
        lowest_rated_game = rawg_data.loc[rawg_data["average_rating"].idxmin()]
        lowest_rated_game_name = lowest_rated_game["name"]
        lowest_rated_game_score = lowest_rated_game["average_rating"]
    else:
        lowest_rated_game_name = "Não encontrado"
        lowest_rated_game_score = 0

# Substituindo "Grand Theft Auto V" por "GTA V" para abreviar
most_reviewed_game_name = most_reviewed_game_name.replace("Grand Theft Auto V", "GTA V")

# Exibir os KPIs em uma linha
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)  # Divide a linha em 5 colunas
    
    with col1:
        st.metric(label="Maior Nota de Avaliação", value=f"{highest_rating}")
    
    with col2:
        st.metric(label="Porcentagem de Jogos com Avaliação > 8", value=f"{percent_above_8:.2f}%")
    
    with col3:
        st.metric(label="Total de Vendas Globais", value=f"{total_revenue:.1f}M")
    
    with col4:
        st.metric(label="Jogo Mais Avaliado", value=f"{most_reviewed_game_name}", delta=f"{most_reviewed_game_reviews} avaliações")
    
    with col5:
        st.metric(label="Jogo com Menor Avaliação", value=f"{lowest_rated_game_name}", delta=f"{lowest_rated_game_score:.2f}")



# Dividir a tela em 2 linhas e 2 colunas
col1, col2 = st.columns(2)  # Primeira linha com duas colunas
col3, col4 = st.columns(2)  # Segunda linha com duas colunas

# Gráfico de dispersão (Relação entre Pontuação de Avaliação e Lucro Calculado)
if not steam_data.empty:
    with col1:
        # Calcular o total de lucro (revenue)
        steam_data['calculated_revenue'] = steam_data['copiesSold'] * steam_data['price']

        # Filtrar os jogos com reviewScore diferente de 0
        steam_data_filtered = steam_data[steam_data["reviewScore"] != 0]

        # Arredondar o valor de vendas (calculated_revenue) para milhões
        steam_data_filtered["calculated_revenue"] = steam_data_filtered["calculated_revenue"] / 1e6  # Convertendo para milhões
        steam_data_filtered["calculated_revenue"] = steam_data_filtered["calculated_revenue"].round()  # Arredondando

        # Criar o gráfico de dispersão
        fig = px.scatter(
            steam_data_filtered, 
            x="reviewScore",  # Coluna para o eixo X (pontuação de avaliação)
            y="calculated_revenue",  # Coluna para o eixo Y (lucro calculado)
            size="calculated_revenue",  # O tamanho das bolinhas será proporcional ao lucro
            color="calculated_revenue",  # Cor das bolinhas com base no lucro
            hover_name="name",  # Exibir o nome do jogo ao passar o mouse
            labels={"reviewScore": "Pontuação de Avaliação", "calculated_revenue": "Lucro Calculado (em Mi)"},
            title="Relação entre Pontuação de Avaliação e Lucro Calculado",
            size_max=40,  # Ajuste para o tamanho máximo das bolinhas
            color_continuous_scale="Viridis"  # Escolha uma paleta de cores
        )
        st.plotly_chart(fig)

        st.markdown("<hr style='border: 1px solid #D3D3D3;' />", unsafe_allow_html=True)

    with col2:
        # Gráfico de vendas globais e regionais
        if not games_data.empty:
            # Converter as colunas de vendas para numéricas
            games_data['NA_Sales'] = pd.to_numeric(games_data['NA_Sales'], errors='coerce')
            games_data['EU_Sales'] = pd.to_numeric(games_data['EU_Sales'], errors='coerce')
            games_data['JP_Sales'] = pd.to_numeric(games_data['JP_Sales'], errors='coerce')
            games_data['Global_Sales'] = pd.to_numeric(games_data['Global_Sales'], errors='coerce')

            # Aplicar a formatação na coluna de vendas
            games_data["Sales"] = games_data[region_filter].apply(lambda x: format_sales(x))

            # Título dinâmico para o gráfico de vendas
            if region_filter == "Global_Sales":
                title = "Vendas Globais por Jogo"
            else:
                title = f"Vendas Regionais ({region_filter}) por Jogo"

            # Criar o gráfico de barras para as vendas regionais ou globais
            fig2 = px.bar(
                games_data, 
                x="Name", 
                y="Sales", 
                title=title,
                labels={"Name": "Nome do Jogo", "Sales": f"Vendas ({region_filter})"},
                color="Sales",
                color_continuous_scale="Bluered"
            )
            st.plotly_chart(fig2)

            st.markdown("<hr style='border: 1px solid #D3D3D3;' />", unsafe_allow_html=True)

# Gráfico de pizza para visualizar o status dos jogos na API RAWG
with col3:
    if not rawg_data.empty:
        # Filtrar os dados do jogo selecionado
        game_data = rawg_data[rawg_data["name"] == game_filter].iloc[0]

        # Dados para o gráfico de pizza
        status_data = {
            "Beaten": game_data["beaten"],
            "Dropped": game_data["dropped"],
            "Owned": game_data["owned"],
            "Playing": game_data["playing"],
            "Toplay": game_data["toplay"],
            "Yet to Play": game_data["yet"]
        }

        # Criar o gráfico de pizza
        fig_pizza = px.pie(
            names=list(status_data.keys()), 
            values=list(status_data.values()), 
            title=f"Status de {game_filter}"
        )
        st.plotly_chart(fig_pizza)
# Gráfico aleatório para preencher o quarto gráfico (col4)
with col4:
    if not rawg_data.empty:
        # Verifica se a coluna 'genres' é uma lista de dicionários, e se sim, extrai o nome de cada gênero
        rawg_data['genre_name'] = rawg_data['genres'].apply(lambda genres: [genre['name'] for genre in genres] if isinstance(genres, list) else [])

        # Expande a lista de gêneros para múltiplas linhas, mantendo os outros dados correspondentes
        expanded_genres = rawg_data.explode('genre_name').dropna(subset=['genre_name'])

        # Agrupar por gênero e calcular a média de avaliação
        genre_avg_rating = expanded_genres.groupby("genre_name")["average_rating"].mean().reset_index()

        # Criar o gráfico de barras para a média de avaliação por gênero
        fig = px.bar(genre_avg_rating, 
                     x="genre_name", 
                     y="average_rating", 
                     title="Média de Avaliação por Gênero", 
                     labels={"average_rating": "Avaliação Média", "genre_name": "Gênero"})
        
        st.plotly_chart(fig)
