# Telecom Billing Analyzer - Streamlit Dashboard

A comprehensive Streamlit dashboard for analyzing telecom billing data and detecting anomalies.

## Features

- 📁 **CSV Data Upload**: Upload billing data with drag-and-drop functionality
- 🔍 **Anomaly Detection**: Automated detection of billing anomalies using business rules
- 📊 **Interactive Analytics**: Visual charts and graphs for data analysis
- 🔍 **Drill-down Analysis**: Detailed view of individual anomalies
- 📥 **Data Export**: Export anomaly reports and full datasets as CSV
- 🎨 **Clean UI**: Professional Streamlit interface with sidebar navigation

## Installation

1. Clone this repository or download the files
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Use the sidebar to navigate between different sections:
   - **Dashboard**: Upload data and view overview
   - **Analytics**: Interactive charts and visualizations
   - **Anomaly Details**: Drill-down into specific anomalies
   - **Export**: Download reports and data

## Data Format

Your CSV file should contain the following columns:

- `user_id`: Unique identifier for each user
- `billed_amount`: The actual amount billed to the user
- `expected_amount`: The expected billing amount
- `data_usage_mb`: Data usage in megabytes
- `expected_vs_actual_diff`: Difference between expected and actual amounts

## Anomaly Detection Rules

The system detects anomalies based on:

1. **High Bills**: Billed amount > $1200
2. **Large Differences**: Significant variance between expected and actual amounts
3. **Usage Patterns**: High data usage with unexpectedly low bills
4. **Billing Errors**: Inconsistencies in billing logic

## Sample Data

If you don't have data ready, use the "Load Sample Data" button on the Dashboard to generate sample billing records for testing.

## Project Structure

```
├── app.py                 # Main Streamlit application
├── components/           # UI components
│   ├── sidebar.py        # Sidebar navigation
│   ├── kpi_cards.py      # KPI metrics display
│   └── anomaly_details.py # Anomaly detail views
├── utils/                # Utility modules
│   ├── data_processor.py # Data processing and validation
│   ├── anomaly_detector.py # Anomaly detection logic
│   └── chart_generator.py # Chart creation utilities
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Customization

- **Anomaly Rules**: Modify `utils/anomaly_detector.py` to adjust detection rules
- **Charts**: Update `utils/chart_generator.py` to customize visualizations
- **UI Components**: Edit files in `components/` to change the interface
- **Styling**: Modify the Streamlit theme in `.streamlit/config.toml` (create if needed)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this dashboard.

## License

This project is open source and available under the MIT License.