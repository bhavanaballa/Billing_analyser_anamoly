import streamlit as st
import pandas as pd

def render_anomaly_details(anomalies, selected_user_id=None):
    """Render detailed anomaly information"""
    
    if len(anomalies) == 0:
        st.info("No anomalies detected in the current dataset")
        return
    
    st.subheader("🔍 Anomaly Analysis")
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Anomalies",
            len(anomalies)
        )
    
    with col2:
        highest_anomaly = anomalies['billed_amount'].max()
        st.metric(
            "Highest Anomaly",
            f"${highest_anomaly:.2f}"
        )
    
    with col3:
        avg_anomaly_diff = anomalies['expected_vs_actual_diff'].mean()
        st.metric(
            "Avg Excess Amount",
            f"${avg_anomaly_diff:.2f}"
        )
    
    # Anomaly breakdown by reason
    st.subheader("📊 Anomaly Breakdown")
    
    if 'anomaly_reason' in anomalies.columns:
        reason_counts = anomalies['anomaly_reason'].value_counts()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.bar_chart(reason_counts)
        
        with col2:
            st.write("**Anomaly Reasons:**")
            for reason, count in reason_counts.items():
                st.write(f"• {reason}: {count}")
    
    # Detailed anomaly table
    st.subheader("📋 Detailed Anomaly Records")
    
    # Add filters
    col1, col2 = st.columns(2)
    
    with col1:
        min_amount = st.number_input(
            "Minimum Billed Amount",
            min_value=0.0,
            max_value=float(anomalies['billed_amount'].max()),
            value=0.0,
            step=50.0
        )
    
    with col2:
        max_amount = st.number_input(
            "Maximum Billed Amount",
            min_value=min_amount,
            max_value=float(anomalies['billed_amount'].max()),
            value=float(anomalies['billed_amount'].max()),
            step=50.0
        )
    
    # Filter anomalies
    filtered_anomalies = anomalies[
        (anomalies['billed_amount'] >= min_amount) & 
        (anomalies['billed_amount'] <= max_amount)
    ]
    
    st.write(f"Showing {len(filtered_anomalies)} of {len(anomalies)} anomalies")
    
    # Display filtered anomalies
    st.dataframe(
        filtered_anomalies,
        use_container_width=True,
        column_config={
            "billed_amount": st.column_config.NumberColumn(
                "Billed Amount",
                format="$%.2f"
            ),
            "expected_amount": st.column_config.NumberColumn(
                "Expected Amount",
                format="$%.2f"
            ),
            "expected_vs_actual_diff": st.column_config.NumberColumn(
                "Difference",
                format="$%.2f"
            ),
            "data_usage_mb": st.column_config.NumberColumn(
                "Data Usage (MB)",
                format="%.0f MB"
            )
        }
    )
    
    return filtered_anomalies