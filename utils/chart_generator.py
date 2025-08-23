import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class ChartGenerator:
    """Generate charts for the dashboard"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#3B82F6',
            'secondary': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'normal': '#10B981',
            'anomaly': '#EF4444'
        }
    
    def create_billing_trend_chart(self, data):
        """Create a line chart showing billing trends over time"""
        # Group by billing cycle and calculate average
        trend_data = data.groupby('billing_cycle').agg({
            'billed_amount': ['mean', 'count'],
            'expected_amount': 'mean'
        }).round(2)
        
        # Flatten column names
        trend_data.columns = ['avg_billed', 'record_count', 'avg_expected']
        trend_data = trend_data.reset_index()
        
        # Create line chart
        fig = go.Figure()
        
        # Add billed amount line
        fig.add_trace(go.Scatter(
            x=trend_data['billing_cycle'],
            y=trend_data['avg_billed'],
            mode='lines+markers',
            name='Average Billed Amount',
            line=dict(color=self.color_palette['primary'], width=3),
            marker=dict(size=8)
        ))
        
        # Add expected amount line
        fig.add_trace(go.Scatter(
            x=trend_data['billing_cycle'],
            y=trend_data['avg_expected'],
            mode='lines+markers',
            name='Average Expected Amount',
            line=dict(color=self.color_palette['secondary'], width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Billing Amount Trends Over Time',
            xaxis_title='Billing Cycle',
            yaxis_title='Amount ($)',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_anomaly_pie_chart(self, data, anomalies):
        """Create a pie chart showing normal vs anomalous bills"""
        normal_count = len(data) - len(anomalies)
        anomaly_count = len(anomalies)
        
        labels = ['Normal Bills', 'Anomalous Bills']
        values = [normal_count, anomaly_count]
        colors = [self.color_palette['normal'], self.color_palette['anomaly']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent+value',
            textfont_size=12
        )])
        
        fig.update_layout(
            title='Distribution of Normal vs Anomalous Bills',
            template='plotly_white',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_amount_distribution_chart(self, data, anomalies):
        """Create a histogram showing distribution of billing amounts"""
        fig = go.Figure()
        
        # Add normal bills
        normal_data = data[~data['user_id'].isin(anomalies['user_id'])]
        fig.add_trace(go.Histogram(
            x=normal_data['billed_amount'],
            name='Normal Bills',
            opacity=0.7,
            marker_color=self.color_palette['normal'],
            nbinsx=30
        ))
        
        # Add anomalous bills
        if len(anomalies) > 0:
            fig.add_trace(go.Histogram(
                x=anomalies['billed_amount'],
                name='Anomalous Bills',
                opacity=0.7,
                marker_color=self.color_palette['anomaly'],
                nbinsx=30
            ))
        
        fig.update_layout(
            title='Distribution of Billing Amounts',
            xaxis_title='Billed Amount ($)',
            yaxis_title='Frequency',
            barmode='overlay',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_data_usage_vs_billing_chart(self, data, anomalies):
        """Create a scatter plot of data usage vs billing amount"""
        # Separate normal and anomalous data
        normal_data = data[~data['user_id'].isin(anomalies['user_id'])]
        
        fig = go.Figure()
        
        # Add normal points
        fig.add_trace(go.Scatter(
            x=normal_data['data_usage_mb'],
            y=normal_data['billed_amount'],
            mode='markers',
            name='Normal Bills',
            marker=dict(
                color=self.color_palette['normal'],
                size=6,
                opacity=0.6
            ),
            text=normal_data['user_id'],
            hovertemplate='<b>%{text}</b><br>Data Usage: %{x} MB<br>Billed: $%{y}<extra></extra>'
        ))
        
        # Add anomalous points
        if len(anomalies) > 0:
            fig.add_trace(go.Scatter(
                x=anomalies['data_usage_mb'],
                y=anomalies['billed_amount'],
                mode='markers',
                name='Anomalous Bills',
                marker=dict(
                    color=self.color_palette['anomaly'],
                    size=8,
                    opacity=0.8,
                    symbol='diamond'
                ),
                text=anomalies['user_id'],
                hovertemplate='<b>%{text}</b><br>Data Usage: %{x} MB<br>Billed: $%{y}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Data Usage vs Billing Amount',
            xaxis_title='Data Usage (MB)',
            yaxis_title='Billed Amount ($)',
            template='plotly_white',
            height=400
        )
        
        return fig