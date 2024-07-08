import logging
from flask import Flask, request, jsonify
from transformers import BertTokenizerFast, TFBertForTokenClassification
import tensorflow as tf
import boto3
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

MODEL_PATH = './ner_model/model.safetensors'  # Updated local path for the model
TOKENIZER_PATH = './ner_tokenizer/tokenizer.json'
BUCKET_NAME = 'serlomucubo'  # Your S3 bucket name
MODEL_KEY = 'ner_model/model.safetensors'  # S3 key for the model
TOKENIZER_KEY = 'ner_tokenizer/tokenizer.json'  # S3 key for the tokenizer

def download_file_from_s3(bucket_name, s3_key, local_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, s3_key, local_path)
    logging.info(f"Downloaded {s3_key} from S3 to {local_path}")

# Download model and tokenizer if not exist locally
if not os.path.exists(MODEL_PATH):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    download_file_from_s3(BUCKET_NAME, MODEL_KEY, MODEL_PATH)

if not os.path.exists(TOKENIZER_PATH):
    os.makedirs(os.path.dirname(TOKENIZER_PATH), exist_ok=True)
    download_file_from_s3(BUCKET_NAME, TOKENIZER_KEY, TOKENIZER_PATH)

# Load model and tokenizer
try:
    model = TFBertForTokenClassification.from_pretrained(os.path.dirname(MODEL_PATH))
    tokenizer = BertTokenizerFast.from_pretrained(os.path.dirname(TOKENIZER_PATH))
    logging.info("Model and tokenizer loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model or tokenizer: {e}")

@app.route('/')
def home():
    return jsonify({'message': 'App is running!'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        inputs = tokenizer(data['text'], return_tensors='tf')
        outputs = model(**inputs)
        predictions = tf.argmax(outputs.logits, axis=-1)
        result = predictions.numpy().tolist()
        return jsonify({'predictions': result})
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)




















