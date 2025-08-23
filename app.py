import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from io import StringIO

# Configure page
st.set_page_config(
    page_title="Telecom Billing Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from utils.data_processor import DataProcessor
from utils.anomaly_detector import AnomalyDetector
from utils.chart_generator import ChartGenerator
from components.sidebar import render_sidebar
from components.kpi_cards import render_kpi_cards
from components.anomaly_details import render_anomaly_details

def main():
    """Main application function"""
    
    # Initialize session state
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'selected_anomaly' not in st.session_state:
        st.session_state.selected_anomaly = None
    
    # Render sidebar and get navigation choice
    page = render_sidebar()
    
    # Main content area
    if page == "Dashboard":
        render_dashboard()
    elif page == "Analytics":
        render_analytics()
    elif page == "Anomaly Details":
        render_anomaly_details_page()
    elif page == "Export":
        render_export_page()

def render_dashboard():
    """Render the main dashboard page"""
    st.title("📊 Telecom Billing Analyzer")
    st.markdown("Upload your billing data to detect anomalies and analyze patterns")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload CSV with columns: user_id, billed_amount, expected_amount, data_usage_mb, expected_vs_actual_diff"
    )
    
    if uploaded_file is not None:
        try:
            # Process uploaded data
            data = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = data
            
            # Validate required columns
            required_columns = ['user_id', 'billed_amount', 'expected_amount', 'data_usage_mb', 'expected_vs_actual_diff']
            missing_columns = [col for col in required_columns if col not in data.columns]
            
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
                return
            
            # Process data for anomalies
            processor = DataProcessor()
            detector = AnomalyDetector()
            
            processed_data = processor.process_data(data)
            anomalies = detector.detect_anomalies(processed_data)
            
            st.session_state.processed_data = {
                'data': processed_data,
                'anomalies': anomalies
            }
            
            # Display KPIs
            render_kpi_cards(processed_data, anomalies)
            
            # Display data table
            st.subheader("📋 Billing Records")
            
            # Add anomaly status to display
            display_data = processed_data.copy()
            display_data['Status'] = display_data['user_id'].apply(
                lambda x: '🚨 Anomaly' if x in anomalies['user_id'].values else '✅ Normal'
            )
            
            st.dataframe(
                display_data[['user_id', 'billed_amount', 'expected_amount', 'data_usage_mb', 'Status']],
                use_container_width=True
            )
            
            # Anomalies section with click functionality
            if len(anomalies) > 0:
                st.subheader("🚨 Detected Anomalies")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"Found {len(anomalies)} anomalous billing records")
                with col2:
                    if st.button("View All Anomalies", type="primary"):
                        st.session_state.selected_page = "Anomaly Details"
                        st.rerun()
                
                # Show top 5 anomalies
                st.dataframe(
                    anomalies.head()[['user_id', 'billed_amount', 'expected_amount', 'anomaly_reason']],
                    use_container_width=True
                )
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    else:
        # Show sample data option
        st.info("👆 Upload a CSV file to get started, or try with sample data below")
        
        if st.button("Load Sample Data", type="secondary"):
            sample_data = generate_sample_data()
            st.session_state.uploaded_data = sample_data
            
            processor = DataProcessor()
            detector = AnomalyDetector()
            
            processed_data = processor.process_data(sample_data)
            anomalies = detector.detect_anomalies(processed_data)
            
            st.session_state.processed_data = {
                'data': processed_data,
                'anomalies': anomalies
            }
            st.rerun()

def render_analytics():
    """Render the analytics page"""
    st.title("📈 Analytics Dashboard")
    
    if st.session_state.processed_data is None:
        st.warning("Please upload data first from the Dashboard page")
        return
    
    data = st.session_state.processed_data['data']
    anomalies = st.session_state.processed_data['anomalies']
    
    # Generate charts
    chart_generator = ChartGenerator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Billing Trends")
        line_chart = chart_generator.create_billing_trend_chart(data)
        st.plotly_chart(line_chart, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Normal vs Anomalous Bills")
        pie_chart = chart_generator.create_anomaly_pie_chart(data, anomalies)
        st.plotly_chart(pie_chart, use_container_width=True)
    
    # Additional analytics
    st.subheader("📋 Detailed Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Highest Bill",
            f"${data['billed_amount'].max():.2f}",
            f"User: {data.loc[data['billed_amount'].idxmax(), 'user_id']}"
        )
    
    with col2:
        st.metric(
            "Average Data Usage",
            f"{data['data_usage_mb'].mean():.0f} MB",
            f"±{data['data_usage_mb'].std():.0f} MB"
        )
    
    with col3:
        anomaly_rate = (len(anomalies) / len(data)) * 100
        st.metric(
            "Anomaly Rate",
            f"{anomaly_rate:.1f}%",
            f"{len(anomalies)} of {len(data)} records"
        )

def render_anomaly_details_page():
    """Render the anomaly details page"""
    st.title("🔍 Anomaly Details")
    
    if st.session_state.processed_data is None:
        st.warning("Please upload data first from the Dashboard page")
        return
    
    anomalies = st.session_state.processed_data['anomalies']
    
    if len(anomalies) == 0:
        st.info("No anomalies detected in the current dataset")
        return
    
    st.subheader(f"Found {len(anomalies)} Anomalous Records")
    
    # Anomaly selection
    selected_user = st.selectbox(
        "Select a user to view detailed report:",
        options=anomalies['user_id'].tolist(),
        format_func=lambda x: f"User {x} - ${anomalies[anomalies['user_id']==x]['billed_amount'].iloc[0]:.2f}"
    )
    
    if selected_user:
        anomaly_record = anomalies[anomalies['user_id'] == selected_user].iloc[0]
        
        # Detailed report
        st.subheader(f"📋 Detailed Report - User {selected_user}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("User ID", anomaly_record['user_id'])
            st.metric("Billed Amount", f"${anomaly_record['billed_amount']:.2f}")
            st.metric("Expected Amount", f"${anomaly_record['expected_amount']:.2f}")
        
        with col2:
            st.metric("Data Usage", f"{anomaly_record['data_usage_mb']:.0f} MB")
            st.metric("Difference", f"${anomaly_record['expected_vs_actual_diff']:.2f}")
            st.metric("Anomaly Reason", anomaly_record['anomaly_reason'])
        
        # Visual comparison
        st.subheader("📊 Visual Comparison")
        
        comparison_data = pd.DataFrame({
            'Amount Type': ['Expected', 'Actual'],
            'Amount': [anomaly_record['expected_amount'], anomaly_record['billed_amount']]
        })
        
        fig = px.bar(
            comparison_data,
            x='Amount Type',
            y='Amount',
            title=f"Expected vs Actual Amount - User {selected_user}",
            color='Amount Type',
            color_discrete_map={'Expected': '#10B981', 'Actual': '#EF4444'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # All anomalies table
    st.subheader("📋 All Anomalies")
    st.dataframe(anomalies, use_container_width=True)

def render_export_page():
    """Render the export page"""
    st.title("📥 Export Data")
    
    if st.session_state.processed_data is None:
        st.warning("Please upload data first from the Dashboard page")
        return
    
    anomalies = st.session_state.processed_data['anomalies']
    
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Anomaly Report**")
        st.write(f"Export {len(anomalies)} anomalous records")
        
        if len(anomalies) > 0:
            csv_data = anomalies.to_csv(index=False)
            st.download_button(
                label="📥 Download Anomaly Report (CSV)",
                data=csv_data,
                file_name=f"anomaly_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="primary"
            )
        else:
            st.info("No anomalies to export")
    
    with col2:
        st.write("**Full Dataset**")
        st.write(f"Export complete processed dataset")
        
        full_data = st.session_state.processed_data['data']
        csv_data = full_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Dataset (CSV)",
            data=csv_data,
            file_name=f"full_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Export statistics
    st.subheader("📊 Export Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(st.session_state.processed_data['data']))
    
    with col2:
        st.metric("Anomalies", len(anomalies))
    
    with col3:
        anomaly_rate = (len(anomalies) / len(st.session_state.processed_data['data'])) * 100
        st.metric("Anomaly Rate", f"{anomaly_rate:.1f}%")
    
    with col4:
        avg_amount = st.session_state.processed_data['data']['billed_amount'].mean()
        st.metric("Avg Bill Amount", f"${avg_amount:.2f}")

def generate_sample_data():
    """Generate sample billing data for demonstration"""
    np.random.seed(42)
    n_records = 100
    
    user_ids = [f"USER_{i:04d}" for i in range(1, n_records + 1)]
    
    # Generate realistic billing data
    expected_amounts = np.random.normal(800, 200, n_records)
    expected_amounts = np.clip(expected_amounts, 200, 2000)
    
    # Add some anomalies (high bills)
    anomaly_indices = np.random.choice(n_records, size=int(n_records * 0.15), replace=False)
    billed_amounts = expected_amounts.copy()
    billed_amounts[anomaly_indices] += np.random.normal(500, 200, len(anomaly_indices))
    
    # Ensure some bills are above 1200 (our anomaly threshold)
    high_anomaly_indices = np.random.choice(anomaly_indices, size=len(anomaly_indices)//2, replace=False)
    billed_amounts[high_anomaly_indices] = np.random.uniform(1200, 2500, len(high_anomaly_indices))
    
    data_usage = np.random.normal(5000, 2000, n_records)
    data_usage = np.clip(data_usage, 1000, 15000)
    
    expected_vs_actual_diff = billed_amounts - expected_amounts
    
    sample_data = pd.DataFrame({
        'user_id': user_ids,
        'billed_amount': np.round(billed_amounts, 2),
        'expected_amount': np.round(expected_amounts, 2),
        'data_usage_mb': np.round(data_usage, 0),
        'expected_vs_actual_diff': np.round(expected_vs_actual_diff, 2)
    })
    
    return sample_data

if __name__ == "__main__":
    main()