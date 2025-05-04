import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import deque

class TransactionProcessor:
    def __init__(self):
        self.df = pd.read_csv('data/creditcard.csv')
        self.feature_means = {}
        self.feature_stds = {}
        
        # Initialize statistics
        self.feature_means['Amount'] = self.df['Amount'].mean()
        self.feature_stds['Amount'] = self.df['Amount'].std()
        
        for col in [col for col in self.df.columns if col.startswith('V')]:
            self.feature_means[col] = self.df[col].mean()
            self.feature_stds[col] = self.df[col].std()
        
        # Store recent transactions (last 100 transactions)
        self.recent_transactions = deque(maxlen=100)
        self.fraud_threshold = self.calculate_fraud_threshold()

        # New statistics
        self.transactions = []
        self.total_amount = 0
        self.fraud_cases = 0
        self.normal_cases = 0

    def calculate_fraud_threshold(self):
        fraud_amounts = self.df[self.df['Class'] == 1]['Amount']
        return float(fraud_amounts.mean() + (2 * fraud_amounts.std()))

    def process_transaction(self, transaction_data):
        features_score = 0
        n_features = 0
        z_scores = {}
        
        for feature, value in transaction_data.items():
            if feature in self.feature_means:
                z_score = (value - self.feature_means[feature]) / self.feature_stds[feature]
                z_scores[feature] = float(z_score)
                features_score += abs(z_score)
                n_features += 1
        
        avg_risk_score = min(features_score / (n_features * 4), 1) if n_features > 0 else 0
        is_fraudulent = bool(avg_risk_score > 0.7 or transaction_data.get('Amount', 0) > self.fraud_threshold)
        
        # Create transaction record
        transaction = {
            'amount': float(transaction_data.get('Amount', 0)),
            'risk_score': float(avg_risk_score),
            'is_fraudulent': is_fraudulent,
            'feature_scores': {k: float(v) for k, v in z_scores.items()},
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to recent transactions
        self.recent_transactions.append(transaction)

        # Update statistics
        self.transactions.append({
            'amount': transaction_data['Amount'],
            'is_fraudulent': transaction['is_fraudulent'],
            'timestamp': transaction['timestamp']
        })
        
        self.total_amount += transaction_data['Amount']
        if transaction['is_fraudulent']:
            self.fraud_cases += 1
        else:
            self.normal_cases += 1
        
        return transaction

    def get_statistics(self):
        """Get real-time statistics including recent transactions"""
        if not self.recent_transactions:
            return {
                'total_transactions': 0,
                'fraud_cases': 0,
                'normal_cases': 0,
                'fraud_threshold': float(self.fraud_threshold),
                'recent_avg_amount': 0,
                'recent_fraud_rate': 0
            }
        
        recent_frauds = sum(1 for t in self.recent_transactions if t['is_fraudulent'])
        recent_amounts = [t['amount'] for t in self.recent_transactions]
        
        total_transactions = len(self.transactions)
        if total_transactions == 0:
            return {
                'total_transactions': 0,
                'fraud_cases': 0,
                'normal_cases': 0,
                'average_amount': 0.00,
                'fraud_rate': 0.00
            }
        
        return {
            'total_transactions': total_transactions,
            'fraud_cases': self.fraud_cases,
            'normal_cases': self.normal_cases,
            'average_amount': self.total_amount / total_transactions,
            'fraud_rate': (self.fraud_cases / total_transactions) * 100,
            'fraud_threshold': float(self.fraud_threshold),
            'recent_avg_amount': float(np.mean(recent_amounts)),
            'recent_fraud_rate': float(recent_frauds / len(self.recent_transactions) * 100)
        }