"""
Automated GitHub Upload Script for Quotex Signal Bot
Author: Ankit Singh
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Print banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║               AUTOMATED GITHUB UPLOAD                       ║
    ║                                                              ║
    ║            Quotex Signal Bot Easy Upload                    ║
    ║                  By: Ankit Singh                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_git_installed():
    """Check if Git is installed"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git not found!")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed!")
        print("📋 Please install Git first:")
        print("   Windows: https://git-scm.com/download/win")
        print("   Mac: brew install git")
        print("   Linux: sudo apt install git")
        return False

def get_user_details():
    """Get user details for GitHub"""
    print("\n👤 GitHub User Details Setup")
    print("=" * 40)
    
    # Get user name
    name = input("📝 Your Name (for Git commits): ").strip()
    if not name:
        name = "Ankit Singh"  # Default
    
    # Get email
    email = input("📧 Your Email (for Git commits): ").strip()
    if not email:
        print("⚠️ Email is required for Git!")
        return None, None
    
    # Get GitHub username
    github_username = input("🐙 Your GitHub Username: ").strip()
    if not github_username:
        print("⚠️ GitHub username is required!")
        return None, None
    
    # Get repository name
    repo_name = input("📁 Repository Name [quotex-signal-bot]: ").strip()
    if not repo_name:
        repo_name = "quotex-signal-bot"
    
    return {
        'name': name,
        'email': email,
        'github_username': github_username,
        'repo_name': repo_name
    }

def setup_git_config(user_details):
    """Setup Git configuration"""
    try:
        # Set user name and email
        subprocess.run(['git', 'config', '--global', 'user.name', user_details['name']], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', user_details['email']], check=True)
        
        print(f"✅ Git configured for: {user_details['name']} <{user_details['email']}>")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git configuration failed: {e}")
        return False

def initialize_git_repo():
    """Initialize Git repository"""
    try:
        # Initialize repository
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        print("✅ Git repository initialized")
        
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        print("✅ Files added to Git")
        
        # Create initial commit
        commit_message = """🎯 Initial Release: Professional Quotex Signal Bot

✅ Complete Features Implemented:
• Advanced Technical Analysis Engine (10-second strategy)
• Real-time Telegram Bot with full menu system  
• Professional money management and risk analysis
• Performance tracking with visual charts
• Multi-asset support (Forex, Crypto, Commodities, Indices)
• Comprehensive documentation and setup guides

📊 Technical Specifications:
• Multi-indicator analysis (SMA, WMA, RSI, MACD, DeMarker)
• Automated signal generation with confidence scoring
• Database integration for user management
• Professional security implementation
• Production-ready deployment scripts

🎯 Strategy Details:
• Entry conditions: Multi-indicator crossover confirmation
• Risk management: Configurable position sizing
• Market filtering: Avoids sideways/low-volatility markets
• Performance target: 65-80% accuracy rate

👤 Developer: Ankit Singh
🏆 Status: Production Ready
📈 Use Case: Professional Quotex trading signals"""

        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True)
        print("✅ Initial commit created")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git repository setup failed: {e}")
        return False

def connect_to_github(user_details):
    """Connect to GitHub repository"""
    try:
        # Set up remote
        repo_url = f"https://github.com/{user_details['github_username']}/{user_details['repo_name']}.git"
        
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True, capture_output=True)
        print(f"✅ Connected to: {repo_url}")
        
        # Set main branch
        subprocess.run(['git', 'branch', '-M', 'main'], check=True, capture_output=True)
        print("✅ Main branch configured")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub connection failed: {e}")
        print("💡 Make sure repository exists on GitHub first!")
        return False

def push_to_github():
    """Push code to GitHub"""
    try:
        print("\n🚀 Uploading to GitHub...")
        print("📋 You may need to enter your GitHub credentials:")
        print("   Username: Your GitHub username")
        print("   Password: Personal Access Token (not your password!)")
        print()
        
        # Push to GitHub
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully uploaded to GitHub!")
            return True
        else:
            print("❌ Upload failed!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub push failed: {e}")
        return False

def print_instructions(user_details):
    """Print final instructions"""
    instructions = f"""
    
    🎉 UPLOAD COMPLETE! 🎉
    
    📍 Your repository: https://github.com/{user_details['github_username']}/{user_details['repo_name']}
    
    🔄 NEXT STEPS:
    
    1. 🔗 Repository पर जाकर verify करें
    2. 🔒 Bot token setup करें:
       python setup_credentials.py
    3. 🚀 Bot को test करें:
       python demo.py
    4. 🤖 Production में run करें:
       python quotex_bot.py
    
    📚 DOCUMENTATION:
    • README.md - Complete usage guide
    • GITHUB_SETUP_GUIDE.md - Detailed GitHub setup
    • setup_credentials.py - Secure token setup
    
    🔐 SECURITY REMINDERS:
    • Never share your bot token
    • Keep .env file local (not on GitHub)
    • Use repository secrets for sensitive data
    • Regular security audits करते रहें
    
    📈 TRADING SUCCESS:
    • Proper money management follow करें
    • Signal confidence levels respect करें
    • Risk management rules strictly follow करें
    
    🎯 Happy Trading! 📊💰
    """
    print(instructions)

def main():
    """Main function"""
    print_banner()
    
    print("🚀 यह script आपके Quotex Signal Bot को automatically GitHub पर upload करेगा!")
    print("📋 बस कुछ details provide करें और script सब कुछ handle कर देगी।")
    
    # Check if Git is installed
    if not check_git_installed():
        return False
    
    # Get user details
    user_details = get_user_details()
    if not user_details:
        print("❌ User details incomplete!")
        return False
    
    print(f"\n📋 Setup Summary:")
    print(f"   👤 Name: {user_details['name']}")
    print(f"   📧 Email: {user_details['email']}")
    print(f"   🐙 GitHub: {user_details['github_username']}")
    print(f"   📁 Repository: {user_details['repo_name']}")
    
    confirm = input("\n✅ Details correct हैं? (y/n): ").lower()
    if confirm not in ['y', 'yes', 'हां', 'हाँ']:
        print("❌ Setup cancelled!")
        return False
    
    # Step-by-step setup
    steps = [
        ("Setting up Git configuration", lambda: setup_git_config(user_details)),
        ("Initializing Git repository", initialize_git_repo),
        ("Connecting to GitHub", lambda: connect_to_github(user_details)),
        ("Uploading to GitHub", push_to_github)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"❌ Failed at: {step_name}")
            return False
    
    # Success!
    print_instructions(user_details)
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Upload failed! Check errors above.")
            print("💡 Manual upload guide: QUICK_GITHUB_UPLOAD.md")
    except KeyboardInterrupt:
        print("\n\n⏹️ Upload cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please try manual upload method.")
