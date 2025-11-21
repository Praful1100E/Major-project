import numpy as np
import librosa

def preprocess_audio(y, sr):
    # Minimal preprocessing: trim silence, apply pre-emphasis, normalize
    y_trimmed, _ = librosa.effects.trim(y, top_db=20)
    y_emph = librosa.effects.preemphasis(y_trimmed)
    # normalize to max absolute 1.0
    if np.max(np.abs(y_emph)) > 0:
        y_emph = y_emph / np.max(np.abs(y_emph))
    return y_emph

def extract_features(y, sr):
    feats = {}
    # duration
    duration = float(len(y)) / sr
    feats["duration"] = duration
    # MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    feats["mfcc_mean"] = np.mean(mfcc, axis=1)
    feats["mfcc_var"] = np.var(mfcc, axis=1)
    # tempo (approx speech rate)
    try:
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    except Exception:
        tempo = 0.0
    feats["tempo"] = float(tempo)
    # energy (RMS)
    rms = librosa.feature.rms(y=y)
    feats["rms_mean"] = float(np.mean(rms))
    # pitch (use librosa.yin if available)
    try:
        f0 = librosa.yin(y, fmin=50, fmax=400, sr=sr)
        # remove unvoiced NaNs
        f0_voiced = f0[~np.isnan(f0)]
        avg_pitch = float(np.mean(f0_voiced)) if len(f0_voiced) > 0 else 0.0
    except Exception:
        avg_pitch = 0.0
    feats["avg_pitch"] = avg_pitch
    # voiced ratio (simple energy threshold)
    energy = np.abs(y)
    voiced_ratio = float(np.mean(energy > (0.01 * np.max(energy)))) if np.max(energy) > 0 else 0.0
    feats["voiced_ratio"] = voiced_ratio
    return feats
