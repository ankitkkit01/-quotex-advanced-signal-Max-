"""
Quotex Signal Technical Analysis Engine
Professional trading signal generator with multiple indicators
Author: Ankit Singh
"""

import numpy as np
import pandas as pd
import requests
import json
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import ta
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Signal:
    """Signal data structure"""
    pair: str
    direction: str  # 'UP' or 'DOWN'
    confidence: str  # 'HIGH', 'MEDIUM', 'LOW'
    valid_until: str
    analysis: str
    entry_time: datetime
    author: str = "Ankit Singh"

class TechnicalAnalysisEngine:
    """Advanced technical analysis engine for Quotex signals"""
    
    def __init__(self):
        self.indicators_cache = {}
        self.pairs_data = {}
        
        # Major trading pairs
        self.trading_pairs = {
            # Forex Major
            'EUR/USD': 'EURUSD', 'GBP/USD': 'GBPUSD', 'USD/JPY': 'USDJPY',
            'USD/CHF': 'USDCHF', 'AUD/USD': 'AUDUSD', 'USD/CAD': 'USDCAD',
            'NZD/USD': 'NZDUSD', 'EUR/GBP': 'EURGBP', 'EUR/JPY': 'EURJPY',
            
            # Forex Minor
            'GBP/JPY': 'GBPJPY', 'GBP/CHF': 'GBPCHF', 'EUR/CHF': 'EURCHF',
            'AUD/JPY': 'AUDJPY', 'AUD/CAD': 'AUDCAD', 'CAD/JPY': 'CADJPY',
            
            # Cryptocurrencies
            'BTC/USD': 'BTCUSD', 'ETH/USD': 'ETHUSD', 'LTC/USD': 'LTCUSD',
            'BCH/USD': 'BCHUSD', 'XRP/USD': 'XRPUSD', 'ADA/USD': 'ADAUSD',
            
            # Commodities
            'GOLD': 'XAUUSD', 'SILVER': 'XAGUSD', 'OIL': 'CRUDE',
            'NATURAL_GAS': 'NATGAS',
            
            # Stock Indices
            'S&P500': 'SPX500', 'NASDAQ': 'NAS100', 'DOW': 'DJ30',
            'FTSE': 'FTSE100', 'DAX': 'DAX30', 'CAC': 'CAC40'
        }
    
    def get_market_data(self, symbol: str, timeframe: str = '1m', limit: int = 500) -> pd.DataFrame:
        """
        Get market data for analysis
        Using simulated data for demonstration - in production, connect to real API
        """
        try:
            # Simulated market data for demonstration
            # In production, replace with real API like Alpha Vantage, IEX, or broker API
            
            np.random.seed(hash(symbol) % 2**32)  # Consistent data for same symbol
            
            dates = pd.date_range(
                start=datetime.now() - timedelta(hours=limit//60), 
                periods=limit, 
                freq='1min'
            )
            
            # Generate realistic OHLCV data
            base_price = np.random.uniform(1.0, 2000.0)  # Different base for different assets
            
            # Random walk with trend
            trend = np.random.uniform(-0.001, 0.001)
            volatility = base_price * 0.002
            
            returns = np.random.normal(trend, volatility, limit)
            prices = base_price * np.exp(np.cumsum(returns))
            
            # Generate OHLC from prices
            opens = prices
            closes = prices * (1 + np.random.normal(0, 0.001, limit))
            highs = np.maximum(opens, closes) * (1 + np.abs(np.random.normal(0, 0.001, limit)))
            lows = np.minimum(opens, closes) * (1 - np.abs(np.random.normal(0, 0.001, limit)))
            volumes = np.random.uniform(1000, 10000, limit)
            
            df = pd.DataFrame({
                'timestamp': dates,
                'open': opens,
                'high': highs,
                'low': lows,
                'close': closes,
                'volume': volumes
            })
            
            df.set_index('timestamp', inplace=True)
            return df
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_sma(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        return data.rolling(window=period).mean()
    
    def calculate_wma(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Weighted Moving Average"""
        weights = np.arange(1, period + 1)
        return data.rolling(window=period).apply(
            lambda x: np.dot(x, weights) / weights.sum() if len(x) == period else np.nan
        )
    
    def calculate_rsi(self, data: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI"""
        return ta.momentum.RSIIndicator(data, window=period).rsi()
    
    def calculate_macd(self, data: pd.Series) -> Dict:
        """Calculate MACD"""
        macd_indicator = ta.trend.MACD(data)
        return {
            'macd': macd_indicator.macd(),
            'signal': macd_indicator.macd_signal(),
            'histogram': macd_indicator.macd_diff()
        }
    
    def calculate_demarker(self, high: pd.Series, low: pd.Series, period: int = 14) -> pd.Series:
        """Calculate DeMarker indicator"""
        de_max = pd.Series(index=high.index, dtype=float)
        de_min = pd.Series(index=low.index, dtype=float)
        
        for i in range(1, len(high)):
            de_max.iloc[i] = max(0, high.iloc[i] - high.iloc[i-1])
            de_min.iloc[i] = max(0, low.iloc[i-1] - low.iloc[i])
        
        sma_de_max = de_max.rolling(window=period).mean()
        sma_de_min = de_min.rolling(window=period).mean()
        
        demarker = sma_de_max / (sma_de_max + sma_de_min)
        return demarker
    
    def calculate_volume_oscillator(self, volume: pd.Series, short_period: int = 5, long_period: int = 10) -> pd.Series:
        """Calculate Volume Oscillator (Weis Waves style)"""
        short_ma = volume.rolling(window=short_period).mean()
        long_ma = volume.rolling(window=long_period).mean()
        return ((short_ma - long_ma) / long_ma) * 100
    
    def detect_support_resistance(self, data: pd.DataFrame, window: int = 20) -> Dict:
        """Detect support and resistance levels"""
        high_prices = data['high']
        low_prices = data['low']
        
        # Find local maxima and minima
        resistance_levels = []
        support_levels = []
        
        for i in range(window, len(data) - window):
            # Resistance (local maxima)
            if high_prices.iloc[i] == high_prices.iloc[i-window:i+window+1].max():
                resistance_levels.append(high_prices.iloc[i])
            
            # Support (local minima)
            if low_prices.iloc[i] == low_prices.iloc[i-window:i+window+1].min():
                support_levels.append(low_prices.iloc[i])
        
        return {
            'resistance': resistance_levels[-3:] if resistance_levels else [],
            'support': support_levels[-3:] if support_levels else []
        }
    
    def analyze_market_conditions(self, data: pd.DataFrame) -> Dict:
        """Analyze overall market conditions"""
        if len(data) < 50:
            return {'condition': 'insufficient_data', 'trend': 'unknown'}
        
        close_prices = data['close']
        sma_20 = self.calculate_sma(close_prices, 20)
        sma_50 = self.calculate_sma(close_prices, 50)
        
        current_price = close_prices.iloc[-1]
        sma_20_current = sma_20.iloc[-1]
        sma_50_current = sma_50.iloc[-1]
        
        # Trend determination
        if current_price > sma_20_current > sma_50_current:
            trend = 'uptrend'
        elif current_price < sma_20_current < sma_50_current:
            trend = 'downtrend'
        else:
            trend = 'sideways'
        
        # Volatility check
        recent_highs = data['high'].tail(20)
        recent_lows = data['low'].tail(20)
        volatility = (recent_highs.max() - recent_lows.min()) / current_price
        
        # Market condition
        if volatility < 0.01:
            condition = 'low_volatility'
        elif volatility > 0.05:
            condition = 'high_volatility'
        else:
            condition = 'normal'
        
        return {
            'condition': condition,
            'trend': trend,
            'volatility': volatility,
            'current_price': current_price
        }
    
    def generate_signal_10s_strategy(self, data: pd.DataFrame) -> Optional[Signal]:
        """
        Generate signal using 10-second strategy
        Indicators: SMA 100, WMA 25, SMA 10, RSI 14, Demarker 14, Volume Oscillator
        """
        try:
            if len(data) < 100:
                return None
            
            close_prices = data['close']
            high_prices = data['high']
            low_prices = data['low']
            volume = data['volume']
            
            # Calculate indicators
            sma_100 = self.calculate_sma(close_prices, 100)
            wma_25 = self.calculate_wma(close_prices, 25)
            sma_10 = self.calculate_sma(close_prices, 10)
            rsi = self.calculate_rsi(close_prices, 14)
            demarker = self.calculate_demarker(high_prices, low_prices, 14)
            volume_osc = self.calculate_volume_oscillator(volume)
            
            # Current values
            current_price = close_prices.iloc[-1]
            current_sma_100 = sma_100.iloc[-1]
            current_wma_25 = wma_25.iloc[-1]
            current_sma_10 = sma_10.iloc[-1]
            current_rsi = rsi.iloc[-1]
            current_demarker = demarker.iloc[-1]
            current_volume_osc = volume_osc.iloc[-1]
            
            # Previous values for crossover detection
            prev_wma_25 = wma_25.iloc[-2]
            prev_sma_10 = sma_10.iloc[-2]
            
            # Signal conditions
            signal_direction = None
            confidence = 'LOW'
            analysis_points = []
            
            # Check market condition (avoid sideways)
            market_conditions = self.analyze_market_conditions(data)
            if market_conditions['condition'] == 'low_volatility':
                return None  # Avoid sideways market
            
            # BUY Signal Conditions
            if (current_price > current_sma_100 and  # Price above SMA 100
                current_sma_10 > current_wma_25 and prev_sma_10 <= prev_wma_25 and  # SMA 10 crosses above WMA 25
                current_rsi < 70 and current_rsi > 30 and  # RSI in reasonable range
                current_demarker > 0.3 and  # Demarker bullish
                current_volume_osc > 0):  # Volume confirmation
                
                signal_direction = 'UP'
                analysis_points.extend([
                    "Price above SMA 100 (Bullish trend)",
                    "SMA 10 crossed above WMA 25",
                    f"RSI at {current_rsi:.1f} (Momentum)",
                    f"DeMarker at {current_demarker:.2f} (Bullish)",
                    "High volume confirmation"
                ])
                
                # Confidence calculation
                confidence_score = 0
                if current_rsi > 40 and current_rsi < 60:
                    confidence_score += 1
                if current_demarker > 0.5:
                    confidence_score += 1
                if current_volume_osc > 5:
                    confidence_score += 1
                if current_price > current_sma_100 * 1.005:  # Strong above SMA 100
                    confidence_score += 1
                
                confidence = 'HIGH' if confidence_score >= 3 else 'MEDIUM' if confidence_score >= 2 else 'LOW'
            
            # SELL Signal Conditions  
            elif (current_price < current_sma_100 and  # Price below SMA 100
                  current_sma_10 < current_wma_25 and prev_sma_10 >= prev_wma_25 and  # SMA 10 crosses below WMA 25
                  current_rsi < 70 and current_rsi > 30 and  # RSI in reasonable range
                  current_demarker < 0.7 and  # Demarker bearish
                  current_volume_osc > 0):  # Volume confirmation
                
                signal_direction = 'DOWN'
                analysis_points.extend([
                    "Price below SMA 100 (Bearish trend)",
                    "SMA 10 crossed below WMA 25",
                    f"RSI at {current_rsi:.1f} (Momentum)",
                    f"DeMarker at {current_demarker:.2f} (Bearish)",
                    "High volume confirmation"
                ])
                
                # Confidence calculation
                confidence_score = 0
                if current_rsi > 40 and current_rsi < 60:
                    confidence_score += 1
                if current_demarker < 0.5:
                    confidence_score += 1
                if current_volume_osc > 5:
                    confidence_score += 1
                if current_price < current_sma_100 * 0.995:  # Strong below SMA 100
                    confidence_score += 1
                
                confidence = 'HIGH' if confidence_score >= 3 else 'MEDIUM' if confidence_score >= 2 else 'LOW'
            
            if signal_direction:
                # Generate signal
                current_time = datetime.now()
                valid_until = current_time + timedelta(minutes=1)  # 1 minute validity
                
                analysis_text = " + ".join(analysis_points)
                
                return Signal(
                    pair="",  # Will be set by caller
                    direction=signal_direction,
                    confidence=confidence,
                    valid_until=valid_until.strftime("%H:%M:%S UTC"),
                    analysis=analysis_text,
                    entry_time=current_time
                )
            
            return None
            
        except Exception as e:
            print(f"Error in 10s strategy: {e}")
            return None
    
    def generate_comprehensive_signal(self, pair: str) -> Optional[Signal]:
        """Generate comprehensive signal with all analysis"""
        try:
            # Get market data
            data = self.get_market_data(self.trading_pairs.get(pair, pair))
            
            if data.empty or len(data) < 100:
                return None
            
            # Generate signal using 10s strategy
            signal = self.generate_signal_10s_strategy(data)
            
            if signal:
                signal.pair = pair
                
                # Add support/resistance analysis
                sr_levels = self.detect_support_resistance(data)
                current_price = data['close'].iloc[-1]
                
                # Check if price is near support/resistance
                sr_analysis = ""
                if sr_levels['resistance']:
                    nearest_resistance = min(sr_levels['resistance'], key=lambda x: abs(x - current_price))
                    if abs(nearest_resistance - current_price) / current_price < 0.01:  # Within 1%
                        sr_analysis = f" | Near Resistance at {nearest_resistance:.4f}"
                
                if sr_levels['support']:
                    nearest_support = min(sr_levels['support'], key=lambda x: abs(x - current_price))
                    if abs(nearest_support - current_price) / current_price < 0.01:  # Within 1%
                        sr_analysis = f" | Near Support at {nearest_support:.4f}"
                
                signal.analysis += sr_analysis
                
                return signal
            
            return None
            
        except Exception as e:
            print(f"Error generating signal for {pair}: {e}")
            return None
    
    def get_random_pair(self) -> str:
        """Get random trading pair"""
        import random
        return random.choice(list(self.trading_pairs.keys()))
    
    def format_signal_message(self, signal: Signal) -> str:
        """Format signal for telegram message"""
        return f"""
🎯 **QUOTEX SIGNAL**

📍 **Pair:** {signal.pair}
📊 **Direction:** {'🟢 UP (BUY)' if signal.direction == 'UP' else '🔴 DOWN (SELL)'}
🕒 **Valid Until:** {signal.valid_until}
📌 **Confidence:** {signal.confidence}
📈 **Analysis:** {signal.analysis}

👤 **By:** {signal.author}

⚡ **Trade Now on Quotex!**
        """.strip()

# Test the engine
if __name__ == "__main__":
    engine = TechnicalAnalysisEngine()
    
    # Test signal generation
    test_pairs = ['EUR/USD', 'BTC/USD', 'GOLD']
    
    print("🚀 Testing Technical Analysis Engine...\n")
    
    for pair in test_pairs:
        print(f"Testing {pair}...")
        signal = engine.generate_comprehensive_signal(pair)
        
        if signal:
            print("✅ Signal Generated:")
            print(engine.format_signal_message(signal))
        else:
            print("❌ No signal generated")
        
        print("-" * 50)
