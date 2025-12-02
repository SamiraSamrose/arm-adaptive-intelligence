import os
import requests
from tqdm import tqdm

def download_file(url, destination):
    """
    Downloads a file with progress bar
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    with open(destination, 'wb') as f, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)

def download_sample_models():
    """
    Downloads sample models for testing
    """
    models = {
        'mobilenet_v2.onnx': 'https://github.com/onnx/models/raw/main/vision/classification/mobilenet/model/mobilenetv2-7.onnx',
        'resnet18.onnx': 'https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet18-v1-7.onnx',
    }
    
    for filename, url in models.items():
        destination = os.path.join(os.path.dirname(__file__), filename)
        
        if os.path.exists(destination):
            print(f"Model {filename} already exists, skipping...")
            continue
        
        print(f"Downloading {filename}...")
        try:
            download_file(url, destination)
            print(f"Successfully downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

if __name__ == '__main__':
    download_sample_models()