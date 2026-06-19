"""
Train Age and Gender Prediction Models using UTK Faces Dataset
"""

import os
import numpy as np
import cv2
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from glob import glob

# Configuration
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 50
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "models"))

def load_utk_dataset(dataset_path):
    """
    Load UTK Faces dataset
    Dataset naming convention: [age]_[gender]_[race]_[date&time].jpg
    - age: 0-116
    - gender: 0 (male), 1 (female)
    """
    images = []
    ages = []
    genders = []
    
    print("Loading UTK Faces dataset...")
    image_files = glob(os.path.join(dataset_path, "*.jpg"))
    
    if len(image_files) == 0:
        raise Exception(f"No images found in {dataset_path}")
    
    print(f"Found {len(image_files)} images")
    
    for img_path in image_files:
        try:
            # Parse filename
            filename = os.path.basename(img_path)
            parts = filename.split('_')
            
            if len(parts) < 3:
                continue
                
            age = int(parts[0])
            gender = int(parts[1])
            
            # Skip invalid data
            if age < 0 or age > 116 or gender not in [0, 1]:
                continue
            
            # Load and preprocess image
            img = cv2.imread(img_path)
            if img is None:
                continue
                
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            
            images.append(img)
            ages.append(age)
            genders.append(gender)
            
        except Exception as e:
            continue
    
    print(f"Successfully loaded {len(images)} images")
    
    # Convert to numpy arrays
    images = np.array(images, dtype='float32') / 255.0
    ages = np.array(ages, dtype='float32')
    genders = np.array(genders, dtype='int32')
    
    return images, ages, genders

def create_gender_model():
    """Create CNN model for gender classification"""
    model = models.Sequential([
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 4
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(2, activation='softmax')  # Binary classification: Male/Female
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_age_model():
    """Create CNN model for age regression"""
    model = models.Sequential([
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 4
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='relu')  # Regression: predict age
    ])
    
    model.compile(
        optimizer='adam',
        loss='mae',  # Mean Absolute Error for age prediction
        metrics=['mae']
    )
    
    return model

def plot_training_history(history, model_name):
    """Plot training history"""
    plt.figure(figsize=(12, 4))
    
    # Loss plot
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title(f'{model_name} - Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    # Metric plot
    metric_key = 'accuracy' if 'accuracy' in history.history else 'mae'
    plt.subplot(1, 2, 2)
    plt.plot(history.history[metric_key], label=f'Training {metric_key}')
    plt.plot(history.history[f'val_{metric_key}'], label=f'Validation {metric_key}')
    plt.title(f'{model_name} - {metric_key}')
    plt.xlabel('Epoch')
    plt.ylabel(metric_key)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, f'{model_name}_training_history.png'))
    plt.close()

def train_models(dataset_path):
    """Train both age and gender models"""
    
    # Create models directory if it doesn't exist
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Load dataset
    print("="*50)
    print("LOADING DATASET")
    print("="*50)
    images, ages, genders = load_utk_dataset(dataset_path)
    
    print(f"\nDataset Statistics:")
    print(f"Total images: {len(images)}")
    print(f"Age range: {ages.min():.0f} - {ages.max():.0f}")
    print(f"Gender distribution: Male={np.sum(genders==0)}, Female={np.sum(genders==1)}")
    
    # Split dataset
    X_train, X_test, age_train, age_test, gender_train, gender_test = train_test_split(
        images, ages, genders, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set: {len(X_train)} images")
    print(f"Test set: {len(X_test)} images")
    
    # Train Gender Model
    print("\n" + "="*50)
    print("TRAINING GENDER CLASSIFICATION MODEL")
    print("="*50)
    
    gender_model = create_gender_model()
    print("\nGender Model Architecture:")
    gender_model.summary()
    
    gender_callbacks = [
        ModelCheckpoint(
            os.path.join(MODEL_DIR, 'gender_classifier_model.keras'),
            save_best_only=True,
            monitor='val_accuracy',
            mode='max'
        ),
        EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True
        )
    ]
    
    print("\nTraining gender model...")
    gender_history = gender_model.fit(
        X_train, gender_train,
        validation_data=(X_test, gender_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=gender_callbacks,
        verbose=1
    )
    
    # Evaluate gender model
    gender_loss, gender_acc = gender_model.evaluate(X_test, gender_test, verbose=0)
    print(f"\n✅ Gender Model - Test Accuracy: {gender_acc*100:.2f}%")
    
    # Plot gender model history
    plot_training_history(gender_history, 'gender_model')
    
    # Train Age Model
    print("\n" + "="*50)
    print("TRAINING AGE REGRESSION MODEL")
    print("="*50)
    
    age_model = create_age_model()
    print("\nAge Model Architecture:")
    age_model.summary()
    
    age_callbacks = [
        ModelCheckpoint(
            os.path.join(MODEL_DIR, 'age_prediction_model.keras'),
            save_best_only=True,
            monitor='val_mae',
            mode='min'
        ),
        EarlyStopping(
            monitor='val_mae',
            patience=10,
            restore_best_weights=True
        )
    ]
    
    print("\nTraining age model...")
    age_history = age_model.fit(
        X_train, age_train,
        validation_data=(X_test, age_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=age_callbacks,
        verbose=1
    )
    
    # Evaluate age model
    age_loss = age_model.evaluate(X_test, age_test, verbose=0)
    print(f"\n✅ Age Model - Test MAE: {age_loss[1]:.2f} years")
    
    # Plot age model history
    plot_training_history(age_history, 'age_model')
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE!")
    print("="*50)
    print(f"Models saved to: {MODEL_DIR}/")
    print(f"- gender_classifier_model.keras (Accuracy: {gender_acc*100:.2f}%)")
    print(f"- age_prediction_model.keras (MAE: {age_loss[1]:.2f} years)")
    print(f"\nTraining plots saved to {MODEL_DIR}/")

if __name__ == "__main__":
    import sys
    
    print("="*50)
    print("UTK FACES MODEL TRAINING")
    print("="*50)
    
    # Check if dataset path is provided
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
    else:
        dataset_path = input("Enter the path to UTK Faces dataset directory: ").strip()
    
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset path '{dataset_path}' does not exist!")
        print("\nPlease download UTK Faces dataset from:")
        print("https://susanqq.github.io/UTKFace/")
        print("\nExtract the images and provide the directory path.")
        sys.exit(1)
    
    try:
        train_models(dataset_path)
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
