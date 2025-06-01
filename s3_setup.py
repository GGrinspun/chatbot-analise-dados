import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

bucket_name = os.getenv("S3_BUCKET")

# Cria o bucket se ele ainda não existir
def criar_bucket():
    try:
        region = os.getenv("AWS_DEFAULT_REGION")
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"✅ Bucket '{bucket_name}' criado com sucesso.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"ℹ️ O bucket '{bucket_name}' já existe e pertence a você.")
    except Exception as e:
        print(f"❌ Erro ao criar bucket: {e}")


def enviar_arquivo(local_path, s3_file_name):
    try:
        s3.upload_file(local_path, bucket_name, s3_file_name)
        print(f"✅ Arquivo '{local_path}' enviado como '{s3_file_name}' no bucket '{bucket_name}'.")
    except Exception as e:
        print(f"❌ Erro ao enviar arquivo: {e}")


if __name__ == "__main__":
    criar_bucket()
    enviar_arquivo("caminho/para/seu/arquivo.csv", os.getenv("S3_FILE"))

