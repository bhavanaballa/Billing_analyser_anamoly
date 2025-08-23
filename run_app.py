#!/usr/bin/env python3
"""
Simple script to run the Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    
    print("🚀 Starting Telecom Billing Analyzer Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("🔧 Use Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        print("💡 Make sure you have installed the requirements:")
        print("   pip install -r requirements.txt")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it:")
        print("   pip install streamlit")

if __name__ == "__main__":
    main()