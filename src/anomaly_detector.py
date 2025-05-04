import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.001, random_state=42)
        
    def train(self, X):
        """Train the anomaly detection model"""
        self.model.fit(X)
        
    def predict(self, transaction):
        """Predict if a transaction is fraudulent"""
        prediction = self.model.predict(transaction)
        # Convert prediction to fraud probability
        return 1 if prediction[0] == -1 else 0
    
    def get_anomaly_score(self, transaction):
        """Get anomaly score for a transaction"""
        return -self.model.score_samples(transaction)[0]