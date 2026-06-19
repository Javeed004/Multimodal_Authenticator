"""
Script to help download and prepare UTK Faces dataset
"""

import os
import requests
from tqdm import tqdm
import zipfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def download_file(url, destination):
    """Download file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=destination,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

def extract_zip(zip_path, extract_to):
    """Extract zip file"""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ Extracted to {extract_to}")

def main():
    print("="*60)
    print("UTK FACES DATASET DOWNLOADER")
    print("="*60)
    
    print("\nUTK Faces Dataset Information:")
    print("- Contains 20,000+ face images")
    print("- Age range: 0-116 years")
    print("- Gender: Male/Female")
    print("- Multiple ethnicities")
    print("\nDataset Source:")
    print("https://susanqq.github.io/UTKFace/")
    
    # Create data directory
    data_dir = os.path.join(PROJECT_ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("DOWNLOAD OPTIONS")
    print("="*60)
    print("\nOption 1: Manual Download (Recommended)")
    print("1. Visit: https://drive.google.com/drive/folders/0BxYys69jI14kU0I1YUQyY1ZDRUE")
    print("2. Download the UTKFace dataset")
    print("3. Extract it to a folder")
    print("4. Run: python backend/train_models.py <path_to_extracted_folder>")
    
    print("\nOption 2: Kaggle Dataset")
    print("1. Install: pip install kaggle")
    print("2. Setup Kaggle API credentials")
    print("3. Download: kaggle datasets download -d jangedoo/utkface-new")
    print("4. Extract and run training script")
    
    print("\n" + "="*60)
    print("ALTERNATIVE: Use a smaller sample dataset")
    print("="*60)
    
    choice = input("\nCreate sample dataset structure for testing? (y/n): ").lower()
    
    if choice == 'y':
        sample_dir = os.path.join(data_dir, "utk_sample")
        os.makedirs(sample_dir, exist_ok=True)
        
        print(f"\n✅ Created sample directory: {sample_dir}")
        print("\nTo use UTK Faces dataset:")
        print("1. Download images from the official source")
        print("2. Place them in the sample directory")
        print("3. Run: python backend/train_models.py data/utk_sample")
        
        print("\nImage naming format: [age]_[gender]_[race]_[date].jpg")
        print("Example: 25_0_2_20170116174525125.jpg")
        print("  - Age: 25")
        print("  - Gender: 0 (male) or 1 (female)")
        print("  - Race: 0-4 (various ethnicities)")
    
    print("\n" + "="*60)
    print("For Kaggle dataset (requires Kaggle API):")
    print("="*60)
    print("\nSetup instructions:")
    print("1. pip install kaggle")
    print("2. Create Kaggle account")
    print("3. Get API token from kaggle.com/account")
    print("4. Place kaggle.json in ~/.kaggle/")
    
    use_kaggle = input("\nTry downloading from Kaggle? (requires setup) (y/n): ").lower()
    
    if use_kaggle == 'y':
        try:
            import kaggle
            print("\nDownloading UTKFace dataset from Kaggle...")
            kaggle.api.dataset_download_files(
                'jangedoo/utkface-new',
                path=data_dir,
                unzip=True
            )
            print(f"✅ Dataset downloaded to {data_dir}")
            print(f"\nRun: python backend/train_models.py {data_dir}/utkface_new")
        except ImportError:
            print("\n❌ Kaggle package not installed. Run: pip install kaggle")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please follow Kaggle API setup instructions.")

if __name__ == "__main__":
    main()
