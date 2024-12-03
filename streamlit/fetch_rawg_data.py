import requests
import json
import os

API_KEY = "551c41910d344b288c2134b807ec44c9"
BASE_URL = "https://api.rawg.io/api"

def fetch_games_data(page=1, page_size=500):
    """
    Função para buscar dados de jogos na API da RAWG.
    
    Args:
        page (int): Número da página para busca.
        page_size (int): Quantidade de itens por página.
    
    Returns:
        dict: Dados retornados pela API.
    """
    endpoint = f"{BASE_URL}/games"
    params = {
        "key": API_KEY,
        "page": page,
        "page_size": page_size
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Verifica se ocorreu algum erro
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao acessar a API da RAWG: {e}")
        return None

def save_to_json(data, filename):
    """
    Salva os dados da API em um arquivo JSON.
    
    Args:
        data (dict): Dados a serem salvos.
        filename (str): Caminho do arquivo JSON.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Dados salvos em {filename}")
    except Exception as e:
        print(f"Erro ao salvar os dados em JSON: {e}")

# Bloco principal para execução
if __name__ == "__main__":
    # Diretório onde o arquivo será salvo (garante que o diretório exista)
    output_dir = "data"  # Ou o caminho desejado
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "games_data.json")

    # Buscar os dados da API
    data = fetch_games_data(page=1, page_size=100)  # Ajuste a quantidade de itens conforme necessário

    if data:
        # Salvar os dados no arquivo JSON
        save_to_json(data, output_file)
    else:
        print("Nenhum dado foi recuperado da API.")
