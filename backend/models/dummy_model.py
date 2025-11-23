import math
import numpy as np

def _sigmoid(x):
    return 1 / (1 + math.exp(-x))

def predict_risk(features):
    """
    Heuristic VoiceGuardian classifier (placeholder).
    Returns: (score [0..1], label, report_text, action_hint)
    """
    mfcc_var = np.array(features.get("mfcc_var", np.zeros(13)), dtype=float)
    var_score = float(np.mean(mfcc_var)) if mfcc_var.size else 0.0
    tempo = float(features.get("tempo", 0.0))
    voiced = float(features.get("voiced_ratio", 0.0))
    avg_pitch = float(features.get("avg_pitch", 0.0))
    duration = float(features.get("duration", 0.0))

    # Compose heuristic raw score (tunable)
    score_raw = 0.9 * (var_score / (1 + var_score)) - 0.45 * (tempo / (tempo + 50)) - 0.6 * voiced + 0.008 * max(0, 120 - avg_pitch)
    # small penalty for very short recordings (less reliable)
    if duration < 5.0:
        score_raw += 0.4 * ((5.0 - duration) / 5.0)

    try:
        score = float(_sigmoid(score_raw))
    except OverflowError:
        score = 0.0 if score_raw < 0 else 1.0

    if score < 0.33:
        label = "low"
        short = "Low risk indicators. Routine monitoring recommended."
        action = "monitor"
    elif score < 0.66:
        label = "moderate"
        short = "Moderate risk indicators. Consider follow-up."
        action = "follow-up"
    else:
        label = "high"
        short = "High risk indicators. Clinical assessment advised."
        action = "clinical"

    # Build a readable VoiceGuardian report
    report_lines = [
        f"VoiceGuardian — Cognitive Risk Snapshot",
        f"Estimated risk: {label.upper()} ({round(score*100)}%)",
        "",
        short,
        "",
        "Key measured signals:",
        f"- Recording duration: {duration:.1f} s",
        f"- Approx. speech rate (tempo): {tempo:.2f}",
        f"- Voiced ratio (speech presence): {voiced:.2f}",
        f"- Average pitch (Hz): {avg_pitch:.2f}",
        f"- MFCC variance (avg): {var_score:.4f}",
        "",
        "Why Voice matters:",
        "Changes in speech (slowing, extra pauses, reduced fluency) can precede clinical symptoms. This prototype highlights signals for further clinical review.",
        "",
        "Recommendations:",
        "- If MODERATE or HIGH: schedule a formal cognitive assessment with a clinician.",
        "- Repeat this voice test periodically to observe trends over time.",
        "- Share this report with your healthcare provider; the features section contains technical details.",
        "",
        "Technical note:",
        "This is a prototype. Replace this heuristic with a trained clinical model (Wav2Vec2/Whisper/HuBERT embeddings + classifier) before using for diagnosis."
    ]
    report_text = "\n".join(report_lines)

    # return tuple: score, label, report_text, action_hint
    return score, label, report_text, action
