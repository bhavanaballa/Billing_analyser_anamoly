import pandas as pd
import numpy as np

class DataProcessor:
    """Handle data processing and validation"""
    
    def __init__(self):
        self.required_columns = [
            'user_id', 'billed_amount', 'expected_amount', 
            'data_usage_mb', 'expected_vs_actual_diff'
        ]
    
    def validate_data(self, data):
        """Validate that the data has required columns and proper format"""
        missing_columns = [col for col in self.required_columns if col not in data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check for numeric columns
        numeric_columns = ['billed_amount', 'expected_amount', 'data_usage_mb', 'expected_vs_actual_diff']
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(data[col]):
                try:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
                except:
                    raise ValueError(f"Column {col} must be numeric")
        
        return data
    
    def process_data(self, data):
        """Process and clean the uploaded data"""
        # Validate data first
        data = self.validate_data(data)
        
        # Remove any rows with missing critical data
        data = data.dropna(subset=['user_id', 'billed_amount', 'expected_amount'])
        
        # Ensure positive amounts
        data = data[data['billed_amount'] >= 0]
        data = data[data['expected_amount'] >= 0]
        
        # Calculate difference if not provided correctly
        data['expected_vs_actual_diff'] = data['billed_amount'] - data['expected_amount']
        
        # Add billing cycle (dummy data for demonstration)
        np.random.seed(42)
        data['billing_cycle'] = np.random.choice(
            ['2024-01', '2024-02', '2024-03', '2024-04'], 
            size=len(data)
        )
        
        return data
    
    def get_data_summary(self, data):
        """Get summary statistics of the data"""
        summary = {
            'total_records': len(data),
            'avg_billed_amount': data['billed_amount'].mean(),
            'max_billed_amount': data['billed_amount'].max(),
            'min_billed_amount': data['billed_amount'].min(),
            'avg_data_usage': data['data_usage_mb'].mean(),
            'total_revenue': data['billed_amount'].sum()
        }
        
        return summary