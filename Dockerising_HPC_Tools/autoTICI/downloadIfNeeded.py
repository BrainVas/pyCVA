import os
import urllib.request

MODELS_DIR = os.environ.get("MODEL_DIR", "/app/models")
os.makedirs(MODELS_DIR, exist_ok=True)

def download(url, local_path):
    if not os.path.exists(local_path):
        print(f"Downloading model from {url}...")
        urllib.request.urlretrieve(url, local_path)
    return local_path
