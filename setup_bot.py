"""
Setup script for Quotex Signal Bot
Author: Ankit Singh
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime

def print_banner():
    """Print setup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                 QUOTEX SIGNAL BOT SETUP                     ║
    ║                                                              ║
    ║           Professional Trading Signal Generator              ║
    ║                   By: Ankit Singh                           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 या उससे नया version चाहिए!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    try:
        # Check if requirements.txt exists
        if not os.path.exists('requirements.txt'):
            print("❌ requirements.txt file नहीं मिली!")
            return False
        
        # Install packages
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        print("✅ सभी packages successfully install हो गए!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Package installation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_database():
    """Setup SQLite database"""
    print("\n🗄️ Setting up database...")
    
    try:
        conn = sqlite3.connect('quotex_bot.db')
        cursor = conn.cursor()
        
        # Create signals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                direction TEXT NOT NULL,
                confidence TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                result TEXT DEFAULT 'pending',
                user_id INTEGER,
                analysis TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                custom_pairs TEXT,
                trading_goal REAL DEFAULT 100.0,
                daily_limit REAL DEFAULT 500.0,
                risk_percentage REAL DEFAULT 2.0,
                notifications BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create performance_stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE,
                total_signals INTEGER DEFAULT 0,
                winning_signals INTEGER DEFAULT 0,
                losing_signals INTEGER DEFAULT 0,
                accuracy REAL DEFAULT 0.0,
                profit_percentage REAL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create trading_pairs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair_name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                performance_score REAL DEFAULT 0.0,
                last_signal DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def get_bot_token():
    """Get bot token from user"""
    print("\n🤖 Telegram Bot Token Setup")
    print("=" * 50)
    print("1. Telegram पर @BotFather को message करें")
    print("2. /newbot command भेजें")
    print("3. Bot का name और username set करें")
    print("4. आपको bot token मिलेगा")
    print("5. उस token को यहाँ paste करें")
    print()
    
    token = input("🔑 Telegram Bot Token enter करें: ").strip()
    
    if not token or len(token) < 40:
        print("❌ Invalid token! Please enter valid bot token.")
        return None
    
    # Save token to environment file
    try:
        with open('.env', 'w') as f:
            f.write(f"TELEGRAM_BOT_TOKEN={token}\n")
            f.write(f"BOT_ENV=production\n")
            f.write(f"SETUP_DATE={datetime.now().isoformat()}\n")
        
        print("✅ Token saved successfully!")
        return token
        
    except Exception as e:
        print(f"❌ Error saving token: {e}")
        return None

def create_startup_script():
    """Create startup script"""
    print("\n📝 Creating startup script...")
    
    startup_script = '''#!/bin/bash
# Quotex Signal Bot Startup Script
# Author: Ankit Singh

echo "🚀 Starting Quotex Signal Bot..."
echo "👤 Developer: Ankit Singh"
echo "📅 $(date)"
echo

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | xargs)
    echo "✅ Environment variables loaded"
fi

# Run the bot
python quotex_bot.py

echo "🏁 Bot stopped at $(date)"
'''
    
    try:
        with open('start_bot.sh', 'w') as f:
            f.write(startup_script)
        
        # Make script executable
        os.chmod('start_bot.sh', 0o755)
        
        print("✅ Startup script created: start_bot.sh")
        return True
        
    except Exception as e:
        print(f"❌ Error creating startup script: {e}")
        return False

def test_setup():
    """Test the setup"""
    print("\n🧪 Testing setup...")
    
    try:
        # Test imports
        import pandas
        import numpy
        import requests
        import ta
        from telegram.ext import Application
        import matplotlib.pyplot as plt
        import seaborn
        
        print("✅ सभी required modules import हो गए!")
        
        # Test database connection
        conn = sqlite3.connect('quotex_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        print(f"✅ Database tables: {len(tables)} tables created")
        
        # Test configuration
        from config import Config
        print(f"✅ Configuration loaded successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_instructions():
    """Print usage instructions"""
    instructions = """
    
    ╔══════════════════════════════════════════════════════════════╗
    ║                     SETUP COMPLETE! 🎉                      ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🚀 HOW TO RUN THE BOT:
    
    Method 1 - Direct Python:
    ▶️  python quotex_bot.py
    
    Method 2 - Startup Script:
    ▶️  ./start_bot.sh
    
    Method 3 - Background Process:
    ▶️  nohup python quotex_bot.py &
    
    📱 BOT USAGE:
    
    1. Start your bot
    2. Telegram पर अपने bot को search करें
    3. /start command भेजें
    4. Menu से "Start Signals" select करें
    5. Trading signals receive करना शुरू करें!
    
    🛠️ TROUBLESHOOTING:
    
    • Bot token verify करें
    • Internet connection check करें
    • Python version 3.8+ होना चाहिए
    • सभी dependencies install होना चाहिए
    
    📞 SUPPORT:
    Developer: Ankit Singh
    Strategy: Advanced Technical Analysis
    
    🎯 DISCLAIMER:
    Trading involves risk. Past performance doesn't guarantee future results.
    Only invest what you can afford to lose.
    
    ✨ Happy Trading! ✨
    """
    print(instructions)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed at package installation!")
        return False
    
    # Setup database
    if not setup_database():
        print("\n❌ Setup failed at database creation!")
        return False
    
    # Get bot token
    token = get_bot_token()
    if not token:
        print("\n❌ Setup failed at bot token configuration!")
        return False
    
    # Create startup script
    if not create_startup_script():
        print("\n⚠️ Warning: Could not create startup script")
    
    # Test setup
    if not test_setup():
        print("\n❌ Setup validation failed!")
        return False
    
    # Print instructions
    print_instructions()
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        
        # Ask if user wants to start bot immediately
        response = input("\n🤔 क्या आप अभी bot start करना चाहते हैं? (y/n): ").lower()
        
        if response in ['y', 'yes', 'हां', 'हाँ']:
            print("\n🚀 Starting bot...")
            try:
                import quotex_bot
                quotex_bot.main()
            except Exception as e:
                print(f"❌ Error starting bot: {e}")
                print("Please run manually: python quotex_bot.py")
    else:
        print("\n❌ Setup failed! Please check errors above.")
        sys.exit(1)
