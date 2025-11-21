import math
import numpy as np

def _sigmoid(x):
    return 1 / (1 + math.exp(-x))

def predict_risk(features):
    """
    Simple heuristic:
    - higher MFCC variance and low tempo / low voiced_ratio -> higher risk
    - lower pitch variability may increase risk
    This is a placeholder. Replace with trained model for production.
    """
    mfcc_var = np.array(features.get("mfcc_var", np.zeros(13)), dtype=float)
    var_score = float(np.mean(mfcc_var))  # higher -> more irregularity
    tempo = float(features.get("tempo", 0.0))
    voiced = float(features.get("voiced_ratio", 0.0))
    avg_pitch = float(features.get("avg_pitch", 0.0))

    # Compose heuristic linear score
    score_raw = 0.8 * (var_score / (1 + var_score)) - 0.4 * (tempo / (tempo + 50)) - 0.5 * voiced + 0.01 * (100 - avg_pitch)
    # map to 0..1
    try:
        score = float(_sigmoid(score_raw))
    except OverflowError:
        score = 0.0 if score_raw < 0 else 1.0

    if score < 0.33:
        label = "low"
        report = "Low risk indicators. Continue monitoring periodically."
    elif score < 0.66:
        label = "moderate"
        report = "Moderate risk. Consider follow-up assessment or repeat tests."
    else:
        label = "high"
        report = "High risk indicators. Seek clinical assessment."

    return score, label, report
