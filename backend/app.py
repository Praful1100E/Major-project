from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import librosa
import tempfile
import os
from .utils.audio import preprocess_audio, extract_features
from .models.dummy_model import predict_risk

app = FastAPI(title="Speech Cognitive Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def status():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # save to temp file then use librosa to load
    suffix = os.path.splitext(file.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        y, sr = librosa.load(tmp_path, sr=16000, mono=True)
        y = preprocess_audio(y, sr)
        feats = extract_features(y, sr)
        score, label, report = predict_risk(feats)
        # ensure features are JSON-serializable (convert arrays to lists)
        json_feats = {}
        for k, v in feats.items():
            if hasattr(v, "tolist"):
                json_feats[k] = v.tolist()
            else:
                json_feats[k] = v
        return {"risk_score": float(score), "label": label, "report": report, "features": json_feats}
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
