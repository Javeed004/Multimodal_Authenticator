from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import os
import cv2
import tempfile
from pathlib import Path
try:
    import librosa
    LIBROSA_IMPORT_ERROR = None
except Exception as import_error:
    librosa = None
    LIBROSA_IMPORT_ERROR = str(import_error)

try:
    from joblib import load as joblib_load
    JOBLIB_IMPORT_ERROR = None
except Exception as import_error:
    joblib_load = None
    JOBLIB_IMPORT_ERROR = str(import_error)

app = FastAPI(
    title="Age and Gender Prediction API",
    description="API for predicting age and gender from facial images using OpenCV pretrained models",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model paths
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
MODEL_DIR = Path(os.environ.get("MODEL_DIR", PROJECT_ROOT / "models")).resolve()
FACE_PROTO = str(MODEL_DIR / "opencv_face_detector.pbtxt")
FACE_MODEL = str(MODEL_DIR / "opencv_face_detector_uint8.pb")
AGE_PROTO = str(MODEL_DIR / "age_deploy.prototxt")
AGE_MODEL = str(MODEL_DIR / "age_net.caffemodel")
GENDER_PROTO = str(MODEL_DIR / "gender_deploy.prototxt")
GENDER_MODEL = str(MODEL_DIR / "gender_net.caffemodel")
VOICE_AGE_MODEL = str(MODEL_DIR / "age_from_voice.keras")
VOICE_GENDER_MODEL = str(MODEL_DIR / "gender_from_voice.keras")
VOICE_SCALER = str(MODEL_DIR / "voice_scaler.pkl")

# Model definitions
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']
VOICE_AGE_CLASSES = np.array(['twenties', 'seventies', 'thirties', 'sixties', 'fifties', 'fourties', 'teens', 'eighties'])
VOICE_GENDER_CLASSES = np.array(['male', 'female', 'other'])
VOICE_AGE_TO_NUMERIC = {
    'teens': 16,
    'twenties': 25,
    'thirties': 35,
    'fourties': 45,
    'fifties': 55,
    'sixties': 65,
    'seventies': 75,
    'eighties': 85,
}

face_net = None
age_net = None
gender_net = None
voice_age_model = None
voice_gender_model = None
voice_scaler = None
voice_runtime_error = None

@app.on_event("startup")
async def load_models():
    """Load OpenCV DNN models on startup"""
    global face_net, age_net, gender_net, voice_age_model, voice_gender_model, voice_scaler, voice_runtime_error
    
    try:
        # Load face detection model
        if os.path.exists(FACE_PROTO) and os.path.exists(FACE_MODEL):
            face_net = cv2.dnn.readNet(FACE_MODEL, FACE_PROTO)
            print("[OK] Face detection model loaded successfully")
        else:
            print(f"[WARN] Face detection models not found")
            print(f"   Expected: {FACE_PROTO} and {FACE_MODEL}")
            
        # Load age prediction model
        if os.path.exists(AGE_PROTO) and os.path.exists(AGE_MODEL):
            age_net = cv2.dnn.readNet(AGE_MODEL, AGE_PROTO)
            print("[OK] Age prediction model loaded successfully")
        else:
            print(f"[WARN] Age prediction models not found")
            print(f"   Expected: {AGE_PROTO} and {AGE_MODEL}")
            
        # Load gender prediction model
        if os.path.exists(GENDER_PROTO) and os.path.exists(GENDER_MODEL):
            gender_net = cv2.dnn.readNet(GENDER_MODEL, GENDER_PROTO)
            print("[OK] Gender prediction model loaded successfully")
        else:
            print(f"[WARN] Gender prediction models not found")
            print(f"   Expected: {GENDER_PROTO} and {GENDER_MODEL}")
            
        if face_net is None or age_net is None or gender_net is None:
            print("\n[INFO] Run from project root: python backend/download_pretrained_models.py")

        # Load voice prediction models (optional runtime)
        if joblib_load is None:
            voice_runtime_error = f"joblib unavailable for voice inference: {JOBLIB_IMPORT_ERROR}"
            print(f"[WARN] {voice_runtime_error}")
        elif os.path.exists(VOICE_SCALER):
            voice_scaler = joblib_load(VOICE_SCALER)
            print("[OK] Voice feature scaler loaded successfully")
        else:
            print(f"[WARN] Voice scaler not found at {VOICE_SCALER}")

        if librosa is None:
            missing_librosa_message = f"librosa unavailable for voice inference: {LIBROSA_IMPORT_ERROR}"
            if voice_runtime_error:
                voice_runtime_error = f"{voice_runtime_error}; {missing_librosa_message}"
            else:
                voice_runtime_error = missing_librosa_message
            print(f"[WARN] {missing_librosa_message}")

        try:
            from tensorflow.keras.models import load_model as keras_load_model
        except Exception as voice_import_error:
            voice_runtime_error = f"TensorFlow unavailable for voice inference: {voice_import_error}"
            print(f"[WARN] {voice_runtime_error}")
            return

        if os.path.exists(VOICE_AGE_MODEL) and os.path.exists(VOICE_GENDER_MODEL):
            voice_age_model = keras_load_model(VOICE_AGE_MODEL)
            voice_gender_model = keras_load_model(VOICE_GENDER_MODEL)
            print("[OK] Voice age/gender models loaded successfully")
        else:
            print("[WARN] Voice models not found")
            print(f"   Expected: {VOICE_AGE_MODEL} and {VOICE_GENDER_MODEL}")

    except Exception as e:
        print(f"[ERROR] Error loading models: {str(e)}")

def detect_faces(image_bytes: bytes):
    """Detect faces in image using OpenCV DNN"""
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image")
        
        h, w = img.shape[:2]
        
        # Create blob from image
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104, 117, 123], False, False)
        
        # Set input and get detections
        face_net.setInput(blob)
        detections = face_net.forward()
        
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:  # Confidence threshold
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                faces.append((x1, y1, x2 - x1, y2 - y1))
        
        return faces, img
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error detecting faces: {str(e)}")

def predict_age_gender(face_img):
    """Predict age and gender for face region"""
    # Prepare input blob
    blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), 
                                  (78.4263377603, 87.7689143744, 114.895847746), 
                                  swapRB=False)
    
    # Predict gender
    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender_idx = gender_preds[0].argmax()
    gender = GENDER_LIST[gender_idx]
    gender_confidence = float(gender_preds[0][gender_idx])
    
    # Predict age
    age_net.setInput(blob)
    age_preds = age_net.forward()
    age_idx = age_preds[0].argmax()
    age_range = AGE_LIST[age_idx]
    age_confidence = float(age_preds[0][age_idx])
    
    # Extract numeric age from range (use midpoint)
    age_mapping = {
        '(0-2)': 1, '(4-6)': 5, '(8-12)': 10, '(15-20)': 17,
        '(25-32)': 28, '(38-43)': 40, '(48-53)': 50, '(60-100)': 70
    }
    predicted_age = age_mapping.get(age_range, 25)
    
    return {
        'gender': gender,
        'gender_confidence': gender_confidence,
        'age_range': age_range,
        'predicted_age': predicted_age,
        'age_confidence': age_confidence
    }


def extract_voice_features(filepath: str, sampling_rate: int = 48000):
    """Extract spectral + MFCC features for voice inference."""
    if librosa is None:
        raise RuntimeError("librosa is required for voice feature extraction but is not installed.")

    audio, _ = librosa.load(filepath, sr=sampling_rate)

    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sampling_rate))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=audio, sr=sampling_rate))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sampling_rate))

    mfcc = librosa.feature.mfcc(y=audio, sr=sampling_rate)
    mfcc_means = [np.mean(coeff) for coeff in mfcc]

    features = [spectral_centroid, spectral_bandwidth, spectral_rolloff] + mfcc_means
    return np.array(features).reshape(1, -1)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Age and Gender Prediction API",
        "version": "2.0.0",
        "model": "OpenCV Pretrained Models",
        "endpoints": {
            "/predict/gender": "Predict gender from image",
            "/predict/age": "Predict age from image",
            "/predict/both": "Predict both age and gender from image",
            "/predict/voice": "Predict age and gender from audio",
            "/health": "Check API health status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "face_detection_loaded": face_net is not None,
        "gender_model_loaded": gender_net is not None,
        "age_model_loaded": age_net is not None,
        "voice_age_model_loaded": voice_age_model is not None,
        "voice_gender_model_loaded": voice_gender_model is not None,
        "voice_scaler_loaded": voice_scaler is not None,
        "voice_runtime_error": voice_runtime_error,
    }

@app.post("/predict/gender")
async def predict_gender(file: UploadFile = File(...)):
    """
    Predict gender from uploaded image
    
    Returns:
        - prediction: "Male" or "Female"
        - confidence: Probability score (0-1)
    """
    if gender_net is None or face_net is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Read image
        image_bytes = await file.read()
        faces, img = detect_faces(image_bytes)
        
        if len(faces) == 0:
            raise HTTPException(status_code=400, detail="No face detected in image")
        
        # Use first detected face
        x, y, w, h = faces[0]
        face_img = img[y:y+h, x:x+w]
        
        # Predict
        result = predict_age_gender(face_img)
        
        return JSONResponse({
            "prediction": result['gender'],
            "confidence": result['gender_confidence']
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/age")
async def predict_age(file: UploadFile = File(...)):
    """
    Predict age from uploaded image
    
    Returns:
        - predicted_age: Estimated age in years
        - age_range: Age range category
    """
    if age_net is None or face_net is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Read image
        image_bytes = await file.read()
        faces, img = detect_faces(image_bytes)
        
        if len(faces) == 0:
            raise HTTPException(status_code=400, detail="No face detected in image")
        
        # Use first detected face
        x, y, w, h = faces[0]
        face_img = img[y:y+h, x:x+w]
        
        # Predict
        result = predict_age_gender(face_img)
        
        return JSONResponse({
            "predicted_age": result['predicted_age'],
            "age_range": result['age_range'],
            "confidence": result['age_confidence']
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/both")
async def predict_both(file: UploadFile = File(...)):
    """
    Predict both age and gender from uploaded image
    
    Returns:
        - gender: "Male" or "Female"
        - gender_confidence: Probability score
        - predicted_age: Estimated age in years
        - age_range: Age range category
    """
    if gender_net is None or age_net is None or face_net is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Read image
        image_bytes = await file.read()
        faces, img = detect_faces(image_bytes)
        
        if len(faces) == 0:
            raise HTTPException(status_code=400, detail="No face detected in image")
        
        # Use first detected face
        x, y, w, h = faces[0]
        face_img = img[y:y+h, x:x+w]
        
        # Predict
        result = predict_age_gender(face_img)
        
        return JSONResponse({
            "gender": result['gender'],
            "gender_confidence": result['gender_confidence'],
            "predicted_age": result['predicted_age'],
            "age_range": result['age_range'],
            "age_confidence": result['age_confidence'],
            "summary": f"{result['gender']}, approximately {result['predicted_age']} years old"
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/voice")
async def predict_voice(file: UploadFile = File(...)):
    """
    Predict age-group and gender from uploaded audio.

    Returns:
        - age_prediction: predicted age bucket label
        - predicted_age: mapped numeric age estimate
        - gender_prediction: predicted gender label
        - age_confidence: age prediction confidence
        - gender_confidence: gender prediction confidence
    """
    if librosa is None:
        detail = voice_runtime_error or "librosa is not available"
        raise HTTPException(status_code=503, detail=detail)

    if voice_age_model is None or voice_gender_model is None or voice_scaler is None:
        detail = voice_runtime_error or "Voice models not loaded"
        raise HTTPException(status_code=503, detail=detail)

    temp_path = None
    try:
        audio_bytes = await file.read()
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Uploaded audio is empty")

        _, ext = os.path.splitext(file.filename or "")
        if not ext:
            ext = ".wav"

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        features = extract_voice_features(temp_path)
        scaled_features = voice_scaler.transform(features)

        pred_age = voice_age_model.predict(scaled_features, verbose=0)[0]
        pred_gender = voice_gender_model.predict(scaled_features, verbose=0)[0]

        age_idx = int(np.argmax(pred_age))
        gender_idx = int(np.argmax(pred_gender))

        age_label = str(VOICE_AGE_CLASSES[age_idx])
        gender_label = str(VOICE_GENDER_CLASSES[gender_idx])
        predicted_age = int(VOICE_AGE_TO_NUMERIC.get(age_label, 18))

        return JSONResponse({
            "age_prediction": age_label,
            "predicted_age": predicted_age,
            "gender_prediction": gender_label,
            "age_confidence": float(np.max(pred_age)),
            "gender_confidence": float(np.max(pred_gender)),
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice prediction error: {str(e)}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
