#!/usr/bin/env python3
"""
🌊 Coastal Guardian - Simple Launcher
Direct launch without complex setup
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print the project banner"""
    print("🌊" * 50)
    print("🌊 COASTAL GUARDIAN - SIMPLE LAUNCHER 🌊")
    print("🌊" * 50)
    print()

def check_dependencies():
    """Check if basic dependencies are available"""
    print("🔍 Checking basic dependencies...")
    
    required_packages = ['streamlit', 'pandas', 'numpy']
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
        print("Installing missing packages...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
            print("✅ Dependencies installed!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def launch_system():
    """Launch the Coastal Guardian system"""
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
    """Main launcher function"""
    print_banner()
    
    print("🎯 Simple Coastal Guardian launcher...")
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    
    print("✅ Dependencies ready!")
    print()
    
    # Launch system
    launch_system()

if __name__ == "__main__":
    main()
