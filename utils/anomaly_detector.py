import pandas as pd
import numpy as np

class AnomalyDetector:
    """Detect anomalies in billing data"""
    
    def __init__(self, threshold=1200):
        self.threshold = threshold
    
    def detect_anomalies(self, data):
        """Detect anomalies based on business rules"""
        anomalies = []
        
        for _, row in data.iterrows():
            anomaly_reasons = []
            
            # Rule 1: Billed amount > threshold
            if row['billed_amount'] > self.threshold:
                anomaly_reasons.append(f"High bill (>${row['billed_amount']:.2f} > ${self.threshold})")
            
            # Rule 2: Significant difference between expected and actual
            if abs(row['expected_vs_actual_diff']) > 300:
                anomaly_reasons.append(f"Large difference (${abs(row['expected_vs_actual_diff']):.2f})")
            
            # Rule 3: Very high data usage with low expected amount
            if row['data_usage_mb'] > 10000 and row['expected_amount'] < 500:
                anomaly_reasons.append("High data usage with low expected bill")
            
            # Rule 4: Negative difference but high bill (potential billing error)
            if row['expected_vs_actual_diff'] < -100 and row['billed_amount'] > 800:
                anomaly_reasons.append("Billed less than expected despite high usage")
            
            if anomaly_reasons:
                anomaly_record = row.copy()
                anomaly_record['anomaly_reason'] = "; ".join(anomaly_reasons)
                anomaly_record['anomaly_severity'] = self._calculate_severity(row, anomaly_reasons)
                anomalies.append(anomaly_record)
        
        if anomalies:
            anomaly_df = pd.DataFrame(anomalies)
            # Sort by severity (highest first)
            anomaly_df = anomaly_df.sort_values('anomaly_severity', ascending=False)
            return anomaly_df
        else:
            return pd.DataFrame()
    
    def _calculate_severity(self, row, reasons):
        """Calculate anomaly severity score"""
        severity = 0
        
        # Base severity on amount difference
        if row['billed_amount'] > self.threshold:
            severity += (row['billed_amount'] - self.threshold) / 100
        
        # Add severity for large differences
        severity += abs(row['expected_vs_actual_diff']) / 100
        
        # Add severity for multiple reasons
        severity += len(reasons) * 0.5
        
        return round(severity, 2)
    
    def get_anomaly_stats(self, anomalies):
        """Get statistics about detected anomalies"""
        if len(anomalies) == 0:
            return {
                'total_anomalies': 0,
                'avg_anomaly_amount': 0,
                'max_anomaly_amount': 0,
                'total_excess_amount': 0
            }
        
        stats = {
            'total_anomalies': len(anomalies),
            'avg_anomaly_amount': anomalies['billed_amount'].mean(),
            'max_anomaly_amount': anomalies['billed_amount'].max(),
            'total_excess_amount': anomalies['expected_vs_actual_diff'].sum(),
            'avg_severity': anomalies['anomaly_severity'].mean()
        }
        
        return stats