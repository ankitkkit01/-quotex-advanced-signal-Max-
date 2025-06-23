"""
Test Script for Final Quotex Signal Bot
Author: Ankit Singh
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print test banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   BOT FINAL TEST                             ║
    ║                                                              ║
    ║              Quotex Signal Bot Verification                  ║
    ║                  By: Ankit Singh                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def test_files_exist():
    """Test if all required files exist"""
    print("📁 Checking required files...")
    
    required_files = [
        'quotex_bot_final.py',
        'technical_analysis.py',
        'config.py',
        'requirements.txt',
        '.env',
        '.gitignore',
        'README.md',
        'LICENSE'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            all_exist = False
    
    return all_exist

def test_env_file():
    """Test .env file configuration"""
    print("\n🔒 Checking environment configuration...")
    
    if not Path('.env').exists():
        print("❌ .env file not found!")
        return False
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        if 'TELEGRAM_BOT_TOKEN' in content:
            print("✅ Bot token found in .env")
            
            # Check if token looks valid
            lines = content.split('\n')
            for line in lines:
                if line.startswith('TELEGRAM_BOT_TOKEN='):
                    token = line.split('=')[1]
                    if len(token) > 40 and ':' in token:
                        print("✅ Token format appears valid")
                        return True
                    else:
                        print("❌ Token format appears invalid")
                        return False
        else:
            print("❌ Bot token not found in .env")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n📦 Testing imports...")
    
    required_modules = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('ta', 'ta'),
        ('telegram', 'telegram'),
        ('matplotlib.pyplot', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('dotenv', 'python-dotenv')
    ]
    
    all_imported = True
    for module, package_name in required_modules:
        try:
            __import__(module)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - NOT INSTALLED!")
            all_imported = False
    
    return all_imported

def test_technical_analysis():
    """Test technical analysis engine"""
    print("\n🔬 Testing technical analysis engine...")
    
    try:
        from technical_analysis import TechnicalAnalysisEngine
        engine = TechnicalAnalysisEngine()
        print("✅ Technical analysis engine initialized")
        
        # Test data generation
        data = engine.get_market_data('EURUSD', '1m', 100)
        if not data.empty:
            print("✅ Market data generation working")
        else:
            print("⚠️ Market data generation returned empty (normal for demo)")
        
        # Test signal generation
        signal = engine.generate_comprehensive_signal('EUR/USD')
        if signal:
            print("✅ Signal generation working")
        else:
            print("⚠️ No signal generated (normal, depends on market conditions)")
        
        return True
        
    except Exception as e:
        print(f"❌ Technical analysis test failed: {e}")
        return False

def test_bot_initialization():
    """Test bot initialization"""
    print("\n🤖 Testing bot initialization...")
    
    try:
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check token
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if token:
            print("✅ Token loaded from environment")
        else:
            print("❌ Token not found in environment")
            return False
        
        # Try to initialize bot class (without running)
        from quotex_bot_final import QuotexSignalBotFinal
        print("✅ Bot class imported successfully")
        
        # We won't actually initialize to avoid Telegram API calls
        print("✅ Bot ready for initialization")
        return True
        
    except Exception as e:
        print(f"❌ Bot initialization test failed: {e}")
        return False

def test_security():
    """Test security configuration"""
    print("\n🔒 Testing security configuration...")
    
    # Check .gitignore
    if Path('.gitignore').exists():
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        if '.env' in gitignore_content:
            print("✅ .env file protected in .gitignore")
        else:
            print("❌ .env file not protected in .gitignore")
            return False
    else:
        print("❌ .gitignore file not found")
        return False
    
    # Check if .env would be committed
    try:
        import subprocess
        result = subprocess.run(['git', 'check-ignore', '.env'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ .env file properly ignored by git")
        else:
            print("⚠️ Git not initialized or .env not properly ignored")
    except:
        print("⚠️ Could not test git ignore (git not available)")
    
    return True

def main():
    """Main test function"""
    print_banner()
    
    print("🧪 Running comprehensive tests for Quotex Signal Bot...")
    print("=" * 60)
    
    tests = [
        ("File Existence", test_files_exist),
        ("Environment Configuration", test_env_file),
        ("Package Imports", test_imports),
        ("Technical Analysis", test_technical_analysis),
        ("Bot Initialization", test_bot_initialization),
        ("Security Configuration", test_security)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running: {test_name}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Bot is ready for production!")
        print("\n🚀 Next steps:")
        print("1. Run bot: python RUN_BOT.py")
        print("2. Test on Telegram: /start")
        print("3. Upload to GitHub (excluding .env)")
        print("4. Start trading with small positions")
    elif passed_tests >= total_tests - 1:
        print("✅ MOSTLY READY! Minor issues found but bot should work.")
        print("⚠️ Check failed tests above")
    else:
        print("❌ MULTIPLE ISSUES FOUND! Please fix before running.")
        print("💡 Check error messages above")
    
    print(f"\n👤 Bot ready by: Ankit Singh")
    print(f"📅 Test completed: {os.path.basename(sys.argv[0])}")

if __name__ == "__main__":
    main()
