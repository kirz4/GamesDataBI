import requests

API_KEY = "551c41910d344b288c2134b807ec44c9"
BASE_URL = "https://api.rawg.io/api"

def fetch_games_data(page=1, page_size=10):
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
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao acessar a API da RAWG: {e}")
        return None
