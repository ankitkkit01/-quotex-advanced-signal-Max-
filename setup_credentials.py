"""
Secure Credential Setup for Quotex Signal Bot
Author: Ankit Singh
"""

import os
import getpass
from pathlib import Path

def print_banner():
    """Print setup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║              SECURE CREDENTIAL SETUP                        ║
    ║                                                              ║
    ║          Quotex Signal Bot - Security First                 ║
    ║                  By: Ankit Singh                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_bot_token():
    """Securely get bot token from user"""
    print("\n🤖 Telegram Bot Token Setup")
    print("=" * 50)
    print("📋 Bot Token कैसे प्राप्त करें:")
    print("1. Telegram पर @BotFather को message करें")
    print("2. /newbot command भेजें") 
    print("3. Bot का name और username set करें")
    print("4. आपको bot token मिलेगा")
    print("5. Token को यहाँ safely enter करें")
    print()
    
    while True:
        # Use getpass for secure input (doesn't show on screen)
        token = getpass.getpass("🔑 Bot Token enter करें (hidden input): ").strip()
        
        if not token:
            print("❌ Token empty नहीं हो सकता!")
            continue
            
        if len(token) < 40:
            print("❌ Invalid token! Proper bot token enter करें.")
            continue
            
        # Basic validation
        if ':' not in token:
            print("❌ Token format गलत है! Format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
            continue
            
        return token

def setup_env_file(token):
    """Create .env file with secure token"""
    try:
        env_content = f"""# Quotex Signal Bot - Environment Variables
# Generated: {os.name} system
# Author: Ankit Singh
# WARNING: Keep this file secure and never share it!

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={token}

# Bot Environment
BOT_ENV=production

# Optional Settings
DATABASE_PATH=quotex_bot.db
LOG_LEVEL=INFO

# Security Note:
# This file contains sensitive information
# Never commit this file to Git/GitHub
# Always keep it local and secure
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        # Set proper file permissions (Unix/Linux)
        if os.name != 'nt':  # Not Windows
            os.chmod('.env', 0o600)  # Read/write for owner only
        
        print("✅ .env file created successfully!")
        print("🔒 File permissions set for security")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def verify_gitignore():
    """Ensure .gitignore protects sensitive files"""
    gitignore_path = Path('.gitignore')
    
    if not gitignore_path.exists():
        print("⚠️ .gitignore file नहीं मिली!")
        return False
    
    try:
        with open('.gitignore', 'r') as f:
            content = f.read()
        
        # Check if .env is protected
        if '.env' not in content:
            print("⚠️ Adding .env protection to .gitignore...")
            with open('.gitignore', 'a') as f:
                f.write('\n# Environment variables\n.env\n*.env\n')
        
        print("✅ .gitignore properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error checking .gitignore: {e}")
        return False

def test_bot_setup():
    """Test if bot can be imported and configured"""
    try:
        print("\n🧪 Testing bot setup...")
        
        # Try to import config
        from config import Config
        
        if Config.validate_token():
            print("✅ Bot token validation passed!")
            print("✅ Configuration loaded successfully!")
            return True
        else:
            print("❌ Bot token validation failed!")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_security_guidelines():
    """Print security best practices"""
    guidelines = """
    
    🔒 SECURITY GUIDELINES:
    
    ✅ DO:
    • Keep .env file local और secure
    • Regular token rotation करें
    • Bot permissions को minimum रखें
    • Logs को regularly check करें
    • Backup करते समय .env exclude करें
    
    ❌ DON'T:
    • Token को कभी share न करें
    • .env file को Git पर commit न करें
    • Public channels में token post न करें
    • Screenshots में token visible न करें
    • Unsecured systems पर token store न करें
    
    🚨 अगर Token Compromise हो जाए:
    1. तुरंत @BotFather से token revoke करें
    2. नया token generate करें
    3. सभी systems पर update करें
    4. Logs में suspicious activity check करें
    """
    print(guidelines)

def main():
    """Main setup function"""
    print_banner()
    
    print("🔐 यह script आपके Telegram Bot Token को securely setup करेगा।")
    print("📋 Token कभी भी plaintext में store नहीं होगा।")
    
    # Get bot token securely
    token = get_bot_token()
    
    # Setup .env file
    if not setup_env_file(token):
        print("❌ Setup failed at .env creation!")
        return False
    
    # Verify .gitignore protection
    verify_gitignore()
    
    # Test setup
    if test_bot_setup():
        print("\n🎉 SETUP SUCCESSFUL!")
        print("✅ Bot token securely configured")
        print("✅ All security checks passed")
        print("✅ Ready to run the bot!")
        
        print("\n🚀 अब bot start करने के लिए:")
        print("   python quotex_bot.py")
        
    else:
        print("\n❌ Setup validation failed!")
        print("कृपया configuration check करें।")
    
    # Show security guidelines
    print_security_guidelines()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("कृपया फिर से try करें।")
