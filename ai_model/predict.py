import joblib
import numpy as np

# Load trained model and scaler
MODEL_PATH = 'ai/model_rf.joblib'
SCALER_PATH = 'ai/scaler.joblib'

clf = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Example feature order: ['Age', 'Education', 'Skills_count', 'Interests_count']
def predict_career(features):
    """
    features: dict with keys 'Age', 'Education', 'Skills_count', 'Interests_count'
    Returns: dict with predicted career and confidence score
    """
    # Ensure order and shape
    X = np.array([
        features['Age'],
        features['Education'],
        features['Skills_count'],
        features['Interests_count']
    ]).reshape(1, -1)
    X_scaled = scaler.transform(X)
    pred = clf.predict(X_scaled)[0]
    proba = clf.predict_proba(X_scaled)[0]
    top_indices = np.argsort(proba)[::-1][:3]
    return {
        'predicted_career': int(pred),
        'top_3': [{'career': int(idx), 'score': float(proba[idx])} for idx in top_indices]
    }
