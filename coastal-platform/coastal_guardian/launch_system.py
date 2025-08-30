#!/usr/bin/env python3
"""
🌊 Coastal Guardian - Unified System Launcher
Launches both the ML API service and Streamlit dashboard
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def start_ml_api():
    """Start the ML Anomaly Detection API service"""
    print("🚀 Starting ML Anomaly Detection API...")
    try:
        # Start the ML API service
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "ml_anomaly_detection.api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], cwd=os.getcwd())
        
        print("✅ ML API service started on http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        return api_process
    except Exception as e:
        print(f"❌ Failed to start ML API: {e}")
        return None

def start_streamlit():
    """Start the Streamlit dashboard"""
    print("🌐 Starting Streamlit Dashboard...")
    try:
        # Start Streamlit app
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], cwd=os.getcwd())
        
        print("✅ Streamlit dashboard started on http://localhost:8501")
        return streamlit_process
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return None

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking system dependencies...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 'folium',
        'scikit-learn', 'fastapi', 'uvicorn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages using: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available!")
    return True

def main():
    """Main launcher function"""
    print("🌊" * 50)
    print("🌊 COASTAL GUARDIAN - UNIFIED SYSTEM LAUNCHER 🌊")
    print("🌊" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🚀 Launching Coastal Guardian Unified System...")
    
    # Start ML API service
    api_process = start_ml_api()
    if not api_process:
        print("❌ Failed to start ML API service")
        sys.exit(1)
    
    # Wait a moment for API to start
    time.sleep(3)
    
    # Start Streamlit dashboard
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("❌ Failed to start Streamlit dashboard")
        api_process.terminate()
        sys.exit(1)
    
    print("\n🎉 COASTAL GUARDIAN SYSTEM SUCCESSFULLY LAUNCHED!")
    print("=" * 60)
    print("🌐 Streamlit Dashboard: http://localhost:8501")
    print("🤖 ML API Service: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    print("\n💡 The system will automatically open in your browser.")
    print("🔄 Press Ctrl+C to stop all services.")
    
    try:
        # Wait for both processes
        while True:
            if api_process.poll() is not None:
                print("❌ ML API service stopped unexpectedly")
                break
            if streamlit_process.poll() is not None:
                print("❌ Streamlit dashboard stopped unexpectedly")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Coastal Guardian system...")
    
    # Clean shutdown
    if api_process:
        api_process.terminate()
        print("✅ ML API service stopped")
    
    if streamlit_process:
        streamlit_process.terminate()
        print("✅ Streamlit dashboard stopped")
    
    print("🌊 Coastal Guardian system shutdown complete!")

if __name__ == "__main__":
    main()
