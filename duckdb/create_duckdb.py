import duckdb
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

def create_table_from_csv(csv_file, table_name, db_file):
    """
    Função para criar uma tabela no banco DuckDB a partir de um CSV.

    Args:
        csv_file (str): Caminho do arquivo CSV.
        table_name (str): Nome da tabela a ser criada.
        db_file (str): Caminho do arquivo DuckDB.

    Returns:
        str: Mensagem de status.
    """
    try:
        # Conectando ao banco DuckDB
        con = duckdb.connect(db_file)

        # Criando a tabela e importando os dados do CSV
        con.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_file}');
        """)

        # Verificando se os dados foram inseridos
        rows = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        con.close()

        return f"Tabela '{table_name}' criada com sucesso! {rows} registros importados."
    except Exception as e:
        return f"Erro ao criar a tabela '{table_name}': {e}"


if __name__ == "__main__":
    # Caminho do banco DuckDB
    db_file = "games_relational.duckdb"

    # Configurações do primeiro CSV
    csv_file1 = os.path.join(base_dir, "Games.csv")
    table_name1 = "games"

    # Configurações do segundo CSV
    csv_file2 = os.path.join(base_dir, "Steam_2024_bestRevenue_1500.csv")
    table_name2 = "steam_games"


    # Criando as tabelas
    print(create_table_from_csv(csv_file1, table_name1, db_file))
    print(create_table_from_csv(csv_file2, table_name2, db_file))