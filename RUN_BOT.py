"""
Quick Start Script for Quotex Signal Bot
Author: Ankit Singh
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                 QUOTEX SIGNAL BOT                            ║
    ║                   QUICK START                                ║
    ║                                                              ║
    ║              Ready-to-Run Production Version                 ║
    ║                  By: Ankit Singh                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'pandas', 'numpy', 'requests', 'ta', 
        'telegram', 'matplotlib', 'seaborn', 'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages!")
            return False
    
    return True

def check_env_file():
    """Check if .env file exists"""
    if Path('.env').exists():
        print("✅ Environment file found")
        return True
    else:
        print("❌ .env file not found!")
        print("💡 Creating .env file...")
        return False

def main():
    """Main function"""
    print_banner()
    
    print("🚀 Starting Quotex Signal Bot...")
    print("📋 Pre-flight checks:")
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed!")
        return
    
    # Check environment
    if not check_env_file():
        print("⚠️ Environment file missing, but bot has token configured")
    
    print("\n" + "="*60)
    print("🎯 QUOTEX SIGNAL BOT - PRODUCTION VERSION")
    print("👤 Developer: Ankit Singh")
    print("📊 Strategy: Advanced Technical Analysis")
    print("🎯 Target Accuracy: 65-80%")
    print("💰 Risk Management: Built-in")
    print("="*60)
    
    print("\n🚀 Launching bot...")
    print("📱 Bot will be available on Telegram")
    print("⏹️ Press Ctrl+C to stop")
    print("📊 Logs will be saved to: quotex_bot.log")
    print("\n" + "="*60)
    
    try:
        # Import and run the final bot
        from quotex_bot_final import main as run_bot
        run_bot()
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all files are in the same directory")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == "__main__":
    main()
