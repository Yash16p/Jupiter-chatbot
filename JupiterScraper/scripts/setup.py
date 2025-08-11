#!/usr/bin/env python3
"""
Setup script for Jupiter.money RAG Bot
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "logs",
        "cache"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        ("streamlit", "streamlit"),
        ("numpy", "numpy"), 
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"),
        ("lxml", "lxml")
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} is installed")
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name} is missing")
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_data_file():
    """Check if data file exists"""
    data_file = Path("JupiterScraper/data/scraped_texts.txt")
    
    if data_file.exists():
        size = data_file.stat().st_size / 1024  # KB
        print(f"✅ Data file found: {data_file} ({size:.1f} KB)")
        return True
    else:
        print(f"⚠️  Data file not found: {data_file}")
        print("   Run: python scripts/scrape_jupiter.py")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Jupiter.money RAG Bot...\n")
    
    # Create directories
    create_directories()
    print()
    
    # Check dependencies
    print("📦 Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    # Check data
    print("📁 Checking data...")
    data_ok = check_data_file()
    print()
    
    if deps_ok and data_ok:
        print("🎉 Setup complete! You can now run:")
        print("   python -m streamlit run chatbot.py")
    elif deps_ok:
        print("⚠️  Setup partially complete. Install dependencies and scrape data first.")
    else:
        print("❌ Setup incomplete. Please install missing dependencies.")

if __name__ == "__main__":
    main() 