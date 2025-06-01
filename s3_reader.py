import boto3
import os
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

def carregar_csv_do_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION")
    )

    bucket_name = os.getenv("S3_BUCKET")
    s3_file = os.getenv("S3_FILE")

    try:
        # Faz o download do objeto e carrega no pandas
        obj = s3.get_object(Bucket=bucket_name, Key=s3_file)
        df = pd.read_csv(obj['Body'])
        print("✅ CSV carregado do S3 com sucesso.")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar CSV do S3: {e}")
        return None
