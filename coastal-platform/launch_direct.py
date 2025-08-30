#!/usr/bin/env python3
"""
🌊 Coastal Guardian - Direct Launcher
Immediate launch without any setup
"""

import os
import sys
import subprocess

def print_banner():
    """Print the project banner"""
    print("🌊" * 50)
    print("🌊 COASTAL GUARDIAN - DIRECT LAUNCH 🌊")
    print("🌊" * 50)
    print()

def launch_direct():
    """Launch the system directly"""
    print("🚀 Launching Coastal Guardian directly...")
    
    try:
        # Change to coastal_guardian directory
        os.chdir("coastal_guardian")
        
        # Launch Streamlit directly
        print("🌐 Starting Streamlit dashboard...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Launch interrupted by user")
        return False
    
    return True

def main():
    """Main function"""
    print_banner()
    launch_direct()

if __name__ == "__main__":
    main()
