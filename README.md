# Multimodal Authenticator

Full-stack age and gender verification demo that combines a React video interface with a FastAPI backend for face and voice prediction.

## Project Structure

```text
Final Year project/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── download_pretrained_models.py
│   ├── download_utk_dataset.py
│   ├── train_models.py
│   └── train_models_colab.ipynb
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── tailwind.config.js
├── models/               # local model files, ignored by Git
├── README.md
└── .gitignore
```

## Features

- React video browsing UI with an age verification gate.
- Webcam-based face capture.
- Microphone-based voice sample capture.
- FastAPI endpoints for face age/gender and voice age/gender prediction.
- Local session storage after successful verification.
- Swagger API docs at `http://localhost:8000/docs`.

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- npm

## Backend Setup

Install Python dependencies:

```powershell
cd backend
pip install -r requirements.txt
```

Model files are expected in the root-level `models/` folder. The OpenCV face, age, and gender models can be downloaded with:

```powershell
cd ..
python backend/download_pretrained_models.py
```

Start the API:

```powershell
python backend/app.py
```

The backend runs at `http://localhost:8000`.

## Frontend Setup

Install frontend dependencies:

```powershell
cd frontend
npm install
```

Start the React app:

```powershell
npm start
```

The frontend runs at `http://localhost:3000` and calls the backend at `http://localhost:8000`.

## API Endpoints

- `GET /health` - backend and model load status
- `POST /predict/gender` - predict gender from an uploaded face image
- `POST /predict/age` - predict age from an uploaded face image
- `POST /predict/both` - predict age and gender from an uploaded face image
- `POST /predict/voice` - predict age group and gender from an uploaded audio sample

## Development Notes

- `models/`, datasets, build output, archives, and dependency folders are intentionally ignored by Git.
- If voice inference is unavailable, the frontend keeps the face result and shows a fallback note.
- CORS is open for local development in `backend/app.py`; restrict it before production deployment.

## License

This project is for educational use.
