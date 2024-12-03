import pandas as pd

def process_rawg_data(rawg_data):
    # Função para calcular a média ponderada dos ratings
    def calculate_weighted_average(ratings):
        if isinstance(ratings, list):  # Certificar que é uma lista
            weighted_sum = sum(rating['id'] * rating['percent'] for rating in ratings)  # Soma ponderada
            total_percent = sum(rating['percent'] for rating in ratings)  # Soma dos pesos
            return weighted_sum / total_percent if total_percent > 0 else None  # Evitar divisão por zero
        return None  # Retorna None para valores inválidos

    # Aplicar a função de média ponderada na coluna 'ratings'
    rawg_data['average_rating'] = rawg_data['ratings'].apply(calculate_weighted_average)
    
    # Função para mapear a média ponderada para a escala de 1 a 10
    def map_to_10_scale(average_rating):
        if average_rating is not None:
            return ((average_rating - 1) / 4) * 9 + 1  # Mapeia de 1-5 para 1-10
        return None  # Retorna None se a média não for válida

    # Aplicar a função de mapeamento para 1-10 na coluna 'average_rating'
    rawg_data['rating_1_to_10'] = rawg_data['average_rating'].apply(map_to_10_scale)

    # Função para processar a coluna 'added_by_status' que contém dados em formato JSON
    def process_status_column(status_data):
        if isinstance(status_data, dict):  # Verifica se já é um dicionário
            return status_data
        elif isinstance(status_data, str):
            try:
                # Se for uma string, tenta converter para dicionário
                return eval(status_data)  # Usar eval para interpretar a string como um dicionário
            except Exception as e:
                print(f"Erro ao processar a string na coluna 'added_by_status': {e}")
                return {}
        return {}

    # Função para acessar o status com segurança
    def get_status_value(status_dict, status_key):
        return status_dict.get(status_key, 0)  # Retorna 0 caso a chave não exista ou o dict seja vazio

    # Expandir a coluna 'added_by_status' para novas colunas
    status_columns = ['beaten', 'dropped', 'owned', 'playing', 'toplay', 'yet']
    
    for col in status_columns:
        rawg_data[col] = rawg_data['added_by_status'].apply(lambda x: get_status_value(process_status_column(x), col))

    # Retirar a coluna original 'added_by_status' para limpeza
    rawg_data = rawg_data.drop(columns=['added_by_status'])

    return rawg_data
