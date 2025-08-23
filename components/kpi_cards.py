import streamlit as st

def render_kpi_cards(data, anomalies):
    """Render KPI cards showing key metrics"""
    
    st.subheader("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Total Records",
            value=len(data),
            help="Total number of billing records processed"
        )
    
    with col2:
        st.metric(
            label="🚨 Total Anomalies",
            value=len(anomalies),
            delta=f"{(len(anomalies)/len(data)*100):.1f}% of total",
            help="Number of anomalous billing records detected"
        )
    
    with col3:
        avg_billed = data['billed_amount'].mean()
        st.metric(
            label="💰 Average Billed Amount",
            value=f"${avg_billed:.2f}",
            delta=f"±${data['billed_amount'].std():.2f}",
            help="Average billing amount across all records"
        )
    
    with col4:
        if len(anomalies) > 0:
            avg_anomaly_amount = anomalies['billed_amount'].mean()
            st.metric(
                label="⚠️ Avg Anomaly Amount",
                value=f"${avg_anomaly_amount:.2f}",
                delta=f"+${avg_anomaly_amount - avg_billed:.2f}",
                delta_color="inverse",
                help="Average billing amount for anomalous records"
            )
        else:
            st.metric(
                label="⚠️ Avg Anomaly Amount",
                value="$0.00",
                help="No anomalies detected"
            )