import boto3
import os
import logging

logging.basicConfig(level=logging.DEBUG)

BUCKET_NAME = 'serlomucubo'
MODEL_KEY = 'ner_model/pytorch_model.bin'
TOKENIZER_KEY = 'ner_model/tokenizer.json'
MODEL_PATH = './ner_model'
TOKENIZER_PATH = './ner_tokenizer'

def download_file_from_s3(bucket_name, s3_key, local_path, region_name='eu-north-1'):
    s3 = boto3.client('s3', region_name=region_name)
    s3.download_file(bucket_name, s3_key, local_path)
    logging.info(f"Downloaded {s3_key} from S3 to {local_path}")

# Descargar el modelo y el tokenizador si no existen localmente
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH, exist_ok=True)  # Crea el directorio si no existe
    download_file_from_s3(BUCKET_NAME, MODEL_KEY, os.path.join(MODEL_PATH, 'pytorch_model.bin'))

if not os.path.exists(TOKENIZER_PATH):
    os.makedirs(TOKENIZER_PATH, exist_ok=True)  # Crea el directorio si no existe
    download_file_from_s3(BUCKET_NAME, TOKENIZER_KEY, os.path.join(TOKENIZER_PATH, 'tokenizer.json'))



print("Files downloaded successfully.")
