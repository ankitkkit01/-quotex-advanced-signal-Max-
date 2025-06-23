"""
Configuration file for Quotex Signal Bot
Author: Ankit Singh
"""

import os
from typing import Dict, List

class BotConfig:
    """Bot configuration settings"""
    
    # Telegram Bot Settings
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    
    # Signal Generation Settings
    SIGNAL_INTERVAL = 45  # Seconds between automatic signals
    MIN_CONFIDENCE = 'MEDIUM'  # Minimum confidence level to send signals
    MAX_SIGNALS_PER_HOUR = 20
    
    # Trading Pairs Configuration
    FOREX_PAIRS = [
        'EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 
        'USD/CAD', 'NZD/USD', 'EUR/GBP', 'EUR/JPY', 'GBP/JPY'
    ]
    
    CRYPTO_PAIRS = [
        'BTC/USD', 'ETH/USD', 'LTC/USD', 'BCH/USD', 'XRP/USD', 'ADA/USD'
    ]
    
    COMMODITY_PAIRS = [
        'GOLD', 'SILVER', 'OIL', 'NATURAL_GAS'
    ]
    
    STOCK_INDICES = [
        'S&P500', 'NASDAQ', 'DOW', 'FTSE', 'DAX', 'CAC'
    ]
    
    # Technical Analysis Settings
    INDICATORS_CONFIG = {
        'sma_periods': [10, 25, 100],
        'wma_period': 25,
        'rsi_period': 14,
        'demarker_period': 14,
        'volume_osc_short': 5,
        'volume_osc_long': 10,
        'support_resistance_window': 20
    }
    
    # Risk Management Settings
    DEFAULT_SETTINGS = {
        'trading_goal': 100.0,      # Daily goal in currency
        'daily_limit': 500.0,       # Maximum daily loss limit
        'risk_percentage': 2.0,     # Risk per trade percentage
        'max_consecutive_losses': 3, # Stop after consecutive losses
        'profit_lock_percentage': 70 # Lock profit percentage
    }
    
    # Performance Targets
    PERFORMANCE_TARGETS = {
        'excellent_accuracy': 75,
        'good_accuracy': 65,
        'minimum_accuracy': 50,
        'target_signals_per_day': 15
    }
    
    # Database Settings
    DATABASE_PATH = 'quotex_bot.db'
    
    # Chart Settings
    CHART_CONFIG = {
        'figsize': (10, 8),
        'dpi': 150,
        'style': 'dark_background',
        'colors': {
            'profit': '#00ff88',
            'loss': '#ff6b6b',
            'neutral': '#ffeb3b',
            'background': '#1e1e1e'
        }
    }
    
    # Message Templates
    MESSAGES = {
        'welcome': """
🎯 **QUOTEX PROFESSIONAL SIGNAL BOT**

नमस्ते! मैं आपका professional Quotex trading signal bot हूँ।

**🚀 मुख्य विशेषताएं:**
• Advanced Technical Analysis
• Real-time Signal Generation  
• Professional Money Management
• Performance Tracking
• Daily/Monthly Reports

**📊 Supported Assets:**
• Forex (Major & Minor pairs)
• Cryptocurrencies (BTC, ETH, etc.)
• Commodities (Gold, Oil, etc.)
• Stock Indices (S&P500, NASDAQ, etc.)

**👤 Developer:** Ankit Singh

नीचे दिए गए menu का उपयोग करके trading शुरू करें!
        """.strip(),
        
        'signal_format': """
🎯 **QUOTEX SIGNAL**

📍 **Pair:** {pair}
📊 **Direction:** {direction}
🕒 **Valid Until:** {valid_until}
📌 **Confidence:** {confidence}
📈 **Analysis:** {analysis}

👤 **By:** Ankit Singh

⚡ **Trade Now on Quotex!**
        """.strip(),
        
        'no_signal': """
❌ **कोई signal नहीं मिला**

अभी market conditions signal generate करने के लिए suitable नहीं हैं।
कुछ समय बाद फिर से try करें।
        """.strip()
    }
    
    # API Settings (for future integration)
    API_SETTINGS = {
        'rate_limit': 100,  # Requests per minute
        'timeout': 30,      # Request timeout in seconds
        'retry_attempts': 3,
        'backoff_factor': 2
    }
    
    @classmethod
    def validate_token(cls) -> bool:
        """Validate if bot token is set"""
        return cls.BOT_TOKEN and cls.BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE'
    
    @classmethod
    def get_all_pairs(cls) -> List[str]:
        """Get all trading pairs"""
        return (cls.FOREX_PAIRS + cls.CRYPTO_PAIRS + 
                cls.COMMODITY_PAIRS + cls.STOCK_INDICES)
    
    @classmethod
    def get_pair_category(cls, pair: str) -> str:
        """Get category of trading pair"""
        if pair in cls.FOREX_PAIRS:
            return 'Forex'
        elif pair in cls.CRYPTO_PAIRS:
            return 'Cryptocurrency'
        elif pair in cls.COMMODITY_PAIRS:
            return 'Commodity'
        elif pair in cls.STOCK_INDICES:
            return 'Stock Index'
        else:
            return 'Other'

# Environment-specific configurations
class DevelopmentConfig(BotConfig):
    """Development environment configuration"""
    DEBUG = True
    SIGNAL_INTERVAL = 30  # Faster signals for testing
    MAX_SIGNALS_PER_HOUR = 60

class ProductionConfig(BotConfig):
    """Production environment configuration"""
    DEBUG = False
    SIGNAL_INTERVAL = 45
    MAX_SIGNALS_PER_HOUR = 20

# Select configuration based on environment
ENV = os.getenv('BOT_ENV', 'development').lower()

if ENV == 'production':
    Config = ProductionConfig
else:
    Config = DevelopmentConfig

# Export the active configuration
__all__ = ['Config', 'BotConfig', 'DevelopmentConfig', 'ProductionConfig']
