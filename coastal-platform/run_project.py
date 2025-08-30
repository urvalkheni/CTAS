#!/usr/bin/env python3
"""
🌊 Coastal Guardian - Main Project Launcher
Complete setup and launch script for the Coastal Guardian system
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print the project banner"""
    print("🌊" * 60)
    print("🌊           COASTAL GUARDIAN - COMPLETE PROJECT           🌊")
    print("🌊              AI-Powered Coastal Protection              🌊")
    print("🌊" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def setup_virtual_environment():
    """Setup virtual environment if it doesn't exist"""
    print("🔧 Setting up virtual environment...")
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            return False
    else:
        print("✅ Virtual environment already exists")
    
    return True

def activate_virtual_environment():
    """Activate virtual environment"""
    print("🔌 Activating virtual environment...")
    
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate.bat"
        if os.path.exists(activate_script):
            print("✅ Virtual environment ready for Windows")
            return True
    else:  # Linux/Mac
        activate_script = "venv/bin/activate"
        if os.path.exists(activate_script):
            print("✅ Virtual environment ready for Linux/Mac")
            return True
    
    print("❌ Virtual environment activation script not found")
    return False

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing project dependencies...")
    
    try:
        # Install main requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Main dependencies installed")
        
        # Install ML requirements
        ml_req_path = Path("coastal_guardian/ml_anomaly_detection/requirements.txt")
        if ml_req_path.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(ml_req_path)], check=True)
            print("✅ ML dependencies installed")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check if all required packages are available"""
    print("🔍 Checking system dependencies...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 'folium',
        'scikit-learn', 'fastapi', 'uvicorn', 'joblib'
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
        return False
    
    print("✅ All dependencies available!")
    return True

def generate_data():
    """Generate initial data if needed"""
    print("📊 Checking data files...")
    
    data_dir = Path("coastal_guardian/data")
    if not data_dir.exists():
        print("📁 Creating data directory...")
        data_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if data files exist
    data_files = [
        "coastal_guardian/data/simulated_tide_data.csv",
        "coastal_guardian/data/simulated_weather_data.csv",
        "coastal_guardian/data/historical_tide_data.csv"
    ]
    
    missing_data = [f for f in data_files if not Path(f).exists()]
    
    if missing_data:
        print("🔄 Generating missing data files...")
        try:
            subprocess.run([sys.executable, "coastal_guardian/data_ingestion.py"], check=True)
            print("✅ Data generation completed")
        except subprocess.CalledProcessError:
            print("❌ Data generation failed")
            return False
    else:
        print("✅ All data files exist")
    
    return True

def launch_system():
    """Launch the complete Coastal Guardian system"""
    print("🚀 Launching Coastal Guardian system...")
    
    try:
        # Change to coastal_guardian directory
        os.chdir("coastal_guardian")
        
        # Launch the system
        subprocess.run([sys.executable, "launch_system.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch system: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Launch interrupted by user")
        return False
    
    return True

def main():
    """Main project launcher function"""
    print_banner()
    
    print("🎯 Setting up Coastal Guardian project...")
    print()
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    print()
    
    # Step 2: Setup virtual environment
    if not setup_virtual_environment():
        print("❌ Virtual environment setup failed")
        sys.exit(1)
    print()
    
    # Step 3: Activate virtual environment
    if not activate_virtual_environment():
        print("❌ Virtual environment activation failed")
        sys.exit(1)
    print()
    
    # Step 4: Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    print()
    
    # Step 5: Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    print()
    
    # Step 6: Generate data
    if not generate_data():
        print("❌ Data generation failed")
        sys.exit(1)
    print()
    
    print("🎉 Project setup completed successfully!")
    print("🚀 Ready to launch Coastal Guardian system...")
    print()
    
    # Ask user if they want to launch now
    try:
        response = input("🚀 Launch Coastal Guardian now? (y/n): ").lower().strip()
        if response in ['y', 'yes', '']:
            print()
            launch_system()
        else:
            print("\n💡 To launch later, run:")
            print("   cd coastal_guardian")
            print("   python launch_system.py")
            print("\n🌊 Coastal Guardian is ready to protect our coastlines!")
    except KeyboardInterrupt:
        print("\n\n🌊 Setup completed! Run 'python coastal_guardian/launch_system.py' to start.")

if __name__ == "__main__":
    main()
