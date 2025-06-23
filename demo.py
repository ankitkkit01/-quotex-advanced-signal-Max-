"""
Quotex Signal Bot Demo
Demonstrates bot functionality without Telegram
Author: Ankit Singh
"""

import time
import random
from datetime import datetime, timedelta
from technical_analysis import TechnicalAnalysisEngine, Signal

def print_banner():
    """Print demo banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   QUOTEX SIGNAL BOT DEMO                    ║
    ║                                                              ║
    ║              Professional Trading Signal Generator           ║
    ║                     By: Ankit Singh                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def simulate_signal_generation():
    """Simulate signal generation process"""
    print("\n🚀 Starting Signal Generation Demo...")
    print("=" * 60)
    
    engine = TechnicalAnalysisEngine()
    
    # Test pairs
    test_pairs = ['EUR/USD', 'BTC/USD', 'GOLD', 'GBP/USD', 'ETH/USD']
    
    signal_count = 0
    successful_signals = 0
    
    for i in range(10):  # Generate 10 test signals
        print(f"\n🔄 Attempt {i+1}/10 - Generating signal...")
        
        # Select random pair
        pair = random.choice(test_pairs)
        print(f"   📊 Testing pair: {pair}")
        
        # Generate signal
        signal = engine.generate_comprehensive_signal(pair)
        
        if signal:
            successful_signals += 1
            print("   ✅ Signal Generated!")
            print(f"   📍 Pair: {signal.pair}")
            print(f"   📊 Direction: {signal.direction}")
            print(f"   📌 Confidence: {signal.confidence}")
            print(f"   🕒 Valid Until: {signal.valid_until}")
            print(f"   📈 Analysis: {signal.analysis[:50]}...")
            
            # Format full signal
            formatted_signal = engine.format_signal_message(signal)
            print("\n   📱 Telegram Message Preview:")
            print("   " + "─" * 50)
            for line in formatted_signal.split('\n')[:8]:  # Show first 8 lines
                print(f"   {line}")
            print("   " + "─" * 50)
            
        else:
            print("   ❌ No signal generated (market conditions not suitable)")
        
        signal_count += 1
        time.sleep(1)  # Small delay for demo
    
    # Summary
    print(f"\n📊 DEMO SUMMARY:")
    print(f"   Total Attempts: {signal_count}")
    print(f"   Successful Signals: {successful_signals}")
    print(f"   Success Rate: {(successful_signals/signal_count)*100:.1f}%")

def demonstrate_technical_analysis():
    """Demonstrate technical analysis capabilities"""
    print("\n🔬 Technical Analysis Demo...")
    print("=" * 60)
    
    engine = TechnicalAnalysisEngine()
    
    # Get sample data
    print("📊 Fetching market data...")
    data = engine.get_market_data('EURUSD', '1m', 200)
    
    if not data.empty:
        print(f"✅ Data fetched: {len(data)} candles")
        
        # Calculate indicators
        print("\n📈 Calculating Technical Indicators...")
        
        close_prices = data['close']
        high_prices = data['high']
        low_prices = data['low']
        volume = data['volume']
        
        # Calculate all indicators
        sma_100 = engine.calculate_sma(close_prices, 100)
        wma_25 = engine.calculate_wma(close_prices, 25)
        sma_10 = engine.calculate_sma(close_prices, 10)
        rsi = engine.calculate_rsi(close_prices, 14)
        demarker = engine.calculate_demarker(high_prices, low_prices, 14)
        volume_osc = engine.calculate_volume_oscillator(volume)
        
        # Current values
        current_price = close_prices.iloc[-1]
        current_sma_100 = sma_100.iloc[-1]
        current_wma_25 = wma_25.iloc[-1]
        current_sma_10 = sma_10.iloc[-1]
        current_rsi = rsi.iloc[-1]
        current_demarker = demarker.iloc[-1]
        current_volume_osc = volume_osc.iloc[-1]
        
        print(f"   💰 Current Price: {current_price:.5f}")
        print(f"   📊 SMA 100: {current_sma_100:.5f}")
        print(f"   📊 WMA 25: {current_wma_25:.5f}")
        print(f"   📊 SMA 10: {current_sma_10:.5f}")
        print(f"   📊 RSI 14: {current_rsi:.2f}")
        print(f"   📊 DeMarker: {current_demarker:.3f}")
        print(f"   📊 Volume Osc: {current_volume_osc:.2f}")
        
        # Market condition analysis
        market_conditions = engine.analyze_market_conditions(data)
        print(f"\n🌍 Market Analysis:")
        print(f"   📈 Trend: {market_conditions['trend'].upper()}")
        print(f"   📊 Condition: {market_conditions['condition'].upper()}")
        print(f"   📊 Volatility: {market_conditions['volatility']:.4f}")
        
        # Support/Resistance
        sr_levels = engine.detect_support_resistance(data)
        print(f"\n🎯 Support/Resistance Levels:")
        if sr_levels['resistance']:
            print(f"   🔴 Resistance: {sr_levels['resistance'][-1]:.5f}")
        if sr_levels['support']:
            print(f"   🟢 Support: {sr_levels['support'][-1]:.5f}")
        
    else:
        print("❌ Could not fetch market data")

def demonstrate_money_management():
    """Demonstrate money management calculations"""
    print("\n💰 Money Management Demo...")
    print("=" * 60)
    
    # Sample settings
    trading_goal = 200.0  # ₹200 daily goal
    daily_limit = 1000.0  # ₹1000 daily limit
    risk_percentage = 2.5  # 2.5% risk per trade
    
    print(f"📊 Trading Settings:")
    print(f"   🎯 Daily Goal: ₹{trading_goal}")
    print(f"   ⚠️ Daily Limit: ₹{daily_limit}")
    print(f"   📊 Risk per Trade: {risk_percentage}%")
    
    # Calculations
    trade_size = (daily_limit * risk_percentage) / 100
    max_trades = daily_limit / trade_size
    profit_lock_amount = trading_goal * 0.7
    
    print(f"\n💡 Money Management Calculations:")
    print(f"   💰 Recommended Trade Size: ₹{trade_size:.0f}")
    print(f"   📊 Maximum Trades per Day: {max_trades:.0f}")
    print(f"   🔒 Profit Lock at: ₹{profit_lock_amount:.0f}")
    
    # Risk scenarios
    print(f"\n⚠️ Risk Scenarios:")
    print(f"   📉 3 Consecutive Losses: ₹{trade_size * 3:.0f} loss")
    print(f"   📈 5 Consecutive Wins: ₹{trade_size * 5 * 0.8:.0f} profit (80% payout)")
    print(f"   📊 Break-even Point: {100/80:.1f} wins needed per loss")

def demonstrate_performance_tracking():
    """Demonstrate performance tracking"""
    print("\n📊 Performance Tracking Demo...")
    print("=" * 60)
    
    # Simulate performance data
    total_signals = 150
    winning_signals = 105
    losing_signals = 45
    accuracy = (winning_signals / total_signals) * 100
    
    print(f"📈 Overall Performance:")
    print(f"   📊 Total Signals: {total_signals}")
    print(f"   ✅ Winning Signals: {winning_signals}")
    print(f"   ❌ Losing Signals: {losing_signals}")
    print(f"   🎯 Accuracy: {accuracy:.1f}%")
    
    # Performance rating
    if accuracy >= 75:
        rating = "EXCELLENT ⭐⭐⭐⭐⭐"
    elif accuracy >= 65:
        rating = "GOOD ⭐⭐⭐⭐"
    elif accuracy >= 55:
        rating = "AVERAGE ⭐⭐⭐"
    else:
        rating = "POOR ⭐⭐"
    
    print(f"   🏆 Rating: {rating}")
    
    # Daily stats simulation
    print(f"\n📅 Recent Daily Performance:")
    for i in range(5):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        daily_signals = random.randint(8, 20)
        daily_wins = random.randint(int(daily_signals * 0.6), int(daily_signals * 0.8))
        daily_accuracy = (daily_wins / daily_signals) * 100
        print(f"   📊 {date}: {daily_wins}/{daily_signals} signals ({daily_accuracy:.1f}%)")

def main():
    """Main demo function"""
    print_banner()
    
    print("🎯 यह demo Quotex Signal Bot की capabilities को demonstrate करता है।")
    print("📱 Real bot में ये सभी features Telegram के through available हैं।")
    
    # Menu
    while True:
        print(f"\n📋 DEMO MENU:")
        print("1. 🚀 Signal Generation Demo")
        print("2. 🔬 Technical Analysis Demo")
        print("3. 💰 Money Management Demo")
        print("4. 📊 Performance Tracking Demo")
        print("5. 🏃‍♂️ Run All Demos")
        print("0. ❌ Exit")
        
        choice = input("\n🎯 Select option (0-5): ").strip()
        
        if choice == '1':
            simulate_signal_generation()
        elif choice == '2':
            demonstrate_technical_analysis()
        elif choice == '3':
            demonstrate_money_management()
        elif choice == '4':
            demonstrate_performance_tracking()
        elif choice == '5':
            simulate_signal_generation()
            demonstrate_technical_analysis()
            demonstrate_money_management()
            demonstrate_performance_tracking()
        elif choice == '0':
            print("\n👋 Demo completed! Happy Trading!")
            print("🚀 अब real bot को run करने के लिए: python quotex_bot.py")
            break
        else:
            print("❌ Invalid choice! Please select 0-5.")
        
        input("\n⏸️ Press Enter to continue...")

if __name__ == "__main__":
    main()
