# Games Data ETL and Visualization

Este projeto realiza a extração, transformação e carga (ETL) de dados de jogos de duas fontes diferentes: a API da RAWG e o banco de dados DuckDB. O objetivo principal é visualizar e analisar informações sobre jogos em um dashboard interativo usando Streamlit e Plotly.

## Funcionalidades

- **Extração de Dados (ETL)**: 
  - Recupera dados da API RAWG sobre jogos.
  - Processa e transforma esses dados para análise.
  - Carrega os dados processados no banco de dados DuckDB.

- **Visualizações**:
  - Visualiza dados sobre vendas de jogos regionais e globais.
  - Exibe KPIs como "Maior Nota de Avaliação", "Percentual de Jogos com Avaliação Acima de 8", "Total de Vendas Globais", e mais.
  - Gráficos de dispersão para avaliar a relação entre a pontuação de avaliação e o lucro dos jogos.
  - Gráficos de pizza para visualizar o status dos jogos (ex: "Jogos Beaten", "Jogos Playing", etc.).
  - Gráficos de barras para comparar a média de avaliações por gênero.

## Requisitos

- Python 3.7+
- Streamlit
- Pandas
- Plotly
- DuckDB
- Requests

## Resumo dos Comandos:

**Clone o Repositorio**:

```
git clone https://github.com/kirz4/GamesDataBI.git
```

**Va para raiz do projeto e instale o requirements.txt**:

```
pip install requirements.txt 
```

**Execute o script de extração de dados da API**:

```
python fetch_rawg_data.py
```
**Execute o script de processamento de dados**:

```
python process_rawg_data.py
```
**Execute o dashboard:**

```
streamlit run dashboard.py
```