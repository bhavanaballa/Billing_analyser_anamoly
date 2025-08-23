import streamlit as st

def render_sidebar():
    """Render the sidebar navigation"""
    
    with st.sidebar:
        st.title("🏠 Navigation")
        
        # Navigation menu
        page = st.radio(
            "Go to:",
            ["Dashboard", "Analytics", "Anomaly Details", "Export"],
            index=0
        )
        
        st.markdown("---")
        
        # App info
        st.markdown("### 📊 Telecom Billing Analyzer")
        st.markdown("""
        **Features:**
        - 📁 CSV Data Upload
        - 🔍 Anomaly Detection
        - 📈 Interactive Analytics
        - 📥 Data Export
        """)
        
        st.markdown("---")
        
        # Instructions
        with st.expander("📋 Instructions"):
            st.markdown("""
            1. **Upload Data**: Use the Dashboard to upload your CSV file
            2. **View Analytics**: Check the Analytics page for insights
            3. **Drill Down**: Explore anomaly details
            4. **Export**: Download reports as needed
            """)
        
        # Data format info
        with st.expander("📄 CSV Format"):
            st.markdown("""
            Required columns:
            - `user_id`: Unique user identifier
            - `billed_amount`: Actual billed amount
            - `expected_amount`: Expected billing amount
            - `data_usage_mb`: Data usage in MB
            - `expected_vs_actual_diff`: Difference between expected and actual
            """)
    
    return page