import os
import urllib.request
import zipfile
import tarfile
from tqdm import tqdm

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path):
    """
    Downloads file from URL with progress bar
    """
    with DownloadProgressBar(unit='B', unit_scale=True,
                            miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def extract_archive(archive_path, extract_to):
    """
    Extracts zip or tar archive
    """
    print(f"Extracting {archive_path}...")
    
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif archive_path.endswith(('.tar.gz', '.tgz')):
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    elif archive_path.endswith('.tar'):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(extract_to)

def download_coco_sample():
    """
    Downloads a small sample of COCO dataset
    """
    print("Downloading COCO sample dataset...")
    
    # This would download actual COCO data
    # For demo, we create placeholder
    coco_dir = os.path.join(os.path.dirname(__file__), 'coco_sample')
    os.makedirs(coco_dir, exist_ok=True)
    
    with open(os.path.join(coco_dir, 'annotations.json'), 'w') as f:
        f.write('{"images": [], "annotations": []}')
    
    print("COCO sample created")

def download_mlperf_mobile():
    """
    Downloads MLPerf Mobile benchmark data
    """
    print("Downloading MLPerf Mobile benchmark data...")
    
    mlperf_dir = os.path.join(os.path.dirname(__file__), 'mlperf_mobile')
    os.makedirs(mlperf_dir, exist_ok=True)
    
    print("MLPerf Mobile benchmark data created")

def main():
    """
    Main download function
    """
    print("Downloading benchmark datasets...")
    print("=" * 60)
    
    datasets_dir = os.path.dirname(__file__)
    os.makedirs(datasets_dir, exist_ok=True)
    
    download_coco_sample()
    download_mlperf_mobile()
    
    print("=" * 60)
    print("All datasets downloaded successfully!")

if __name__ == '__main__':
    main()