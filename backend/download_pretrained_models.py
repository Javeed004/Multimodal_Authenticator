"""Download OpenCV pretrained models for age and gender prediction."""

import urllib.request
from pathlib import Path

# Create models directory
project_root = Path(__file__).resolve().parent.parent
models_dir = project_root / "models"
models_dir.mkdir(exist_ok=True)

# Model URLs - using alternative sources
models = {
    "age_net.caffemodel": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/age_net.caffemodel",
    "age_deploy.prototxt": "https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/age_deploy.prototxt",
    "gender_net.caffemodel": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/gender_net.caffemodel",
    "gender_deploy.prototxt": "https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/gender_deploy.prototxt",
    "opencv_face_detector.pbtxt": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/opencv_face_detector.pbtxt",
    "opencv_face_detector_uint8.pb": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/opencv_face_detector_uint8.pb"
}

print("Downloading OpenCV pretrained models...")
print("=" * 60)

for filename, url in models.items():
    filepath = models_dir / filename
    
    if filepath.exists():
        print(f"✓ {filename} already exists")
    else:
        print(f"⬇ Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"  ✓ Saved to {filepath}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

print("=" * 60)
print("\n✓ Download complete!")
print(f"Models saved to: {models_dir.absolute()}")
print("\nYou can now run: python backend/app.py")
