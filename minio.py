from minio import Minio
from minio.error import S3Error

# Conecte-se ao MinIO
client = Minio(
    "localhost:9000",  # Endereço do servidor MinIO
    access_key="SEU_ACCESS_KEY",  # Substitua pelo seu Access Key
    secret_key="SEU_SECRET_KEY",  # Substitua pelo seu Secret Key
    secure=False  # Defina como True se usar HTTPS
)

# Nome do bucket e caminho do arquivo local
bucket_name = "meu-bucket"
file_path = "C:/Users/Lucas/Downloads/Games.csv"
object_name = "Games.csv"

# Crie o bucket, se ele não existir
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' criado com sucesso.")
else:
    print(f"Bucket '{bucket_name}' já existe.")

# Faça upload do arquivo CSV
client.fput_object(bucket_name, object_name, file_path)
print(f"Arquivo '{object_name}' enviado para o bucket '{bucket_name}'.")
