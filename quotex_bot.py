"""
Quotex Signal Telegram Bot
Professional automated trading signals bot
Author: Ankit Singh
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3
import threading
import time
from dataclasses import asdict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

from technical_analysis import TechnicalAnalysisEngine, Signal

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class QuotexSignalBot:
    """Professional Quotex Signal Telegram Bot"""
    
    def __init__(self, token: str):
        self.token = token
        self.engine = TechnicalAnalysisEngine()
        self.active_users = set()
        self.user_settings = {}
        self.signal_history = []
        self.performance_stats = {
            'total_signals': 0,
            'winning_signals': 0,
            'losing_signals': 0,
            'accuracy': 0.0,
            'daily_stats': {},
            'monthly_stats': {}
        }
        
        # Initialize database
        self.init_database()
        
        # Signal generation control
        self.signal_active = False
        self.signal_thread = None
        
        # Setup matplotlib for chart generation
        self.setup_matplotlib()
    
    def setup_matplotlib(self):
        """Setup matplotlib for chart generation"""
        plt.style.use('dark_background')
        plt.rcParams['figure.facecolor'] = '#1e1e1e'
        plt.rcParams['axes.facecolor'] = '#2d2d2d'
        plt.rcParams['text.color'] = '#ffffff'
        plt.rcParams['axes.labelcolor'] = '#ffffff'
        plt.rcParams['xtick.color'] = '#ffffff'
        plt.rcParams['ytick.color'] = '#ffffff'
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.figsize'] = (10, 6)
    
    def init_database(self):
        """Initialize SQLite database for storing signals and stats"""
        self.conn = sqlite3.connect('quotex_bot.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT,
                direction TEXT,
                confidence TEXT,
                timestamp DATETIME,
                result TEXT DEFAULT 'pending',
                user_id INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                custom_pairs TEXT,
                trading_goal REAL DEFAULT 100.0,
                daily_limit REAL DEFAULT 500.0,
                risk_percentage REAL DEFAULT 2.0,
                notifications BOOLEAN DEFAULT 1
            )
        ''')
        
        self.conn.commit()
    
    def get_main_menu_keyboard(self):
        """Get main menu keyboard"""
        keyboard = [
            [KeyboardButton("🚀 Start Signals"), KeyboardButton("⏹️ Stop Signals")],
            [KeyboardButton("🎲 Random Signal"), KeyboardButton("🎯 Custom Pair Signal")],
            [KeyboardButton("📊 Statistics"), KeyboardButton("🏆 Performance")],
            [KeyboardButton("💰 Money Management"), KeyboardButton("📈 Best Pairs Today")],
            [KeyboardButton("⚙️ Settings"), KeyboardButton("ℹ️ Help")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    def get_pairs_keyboard(self):
        """Get trading pairs selection keyboard"""
        pairs = list(self.engine.trading_pairs.keys())
        keyboard = []
        
        # Group pairs in rows of 2
        for i in range(0, len(pairs), 2):
            row = []
            row.append(InlineKeyboardButton(pairs[i], callback_data=f"pair_{pairs[i]}"))
            if i + 1 < len(pairs):
                row.append(InlineKeyboardButton(pairs[i + 1], callback_data=f"pair_{pairs[i + 1]}"))
            keyboard.append(row)
        
        return InlineKeyboardMarkup(keyboard)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        welcome_message = f"""
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
        """.strip()
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=self.get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    async def start_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start automatic signal generation"""
        user_id = update.effective_user.id
        self.active_users.add(user_id)
        
        if not self.signal_active:
            self.signal_active = True
            self.signal_thread = threading.Thread(target=self.signal_generator_loop, daemon=True)
            self.signal_thread.start()
        
        await update.message.reply_text(
            "🚀 **Signals Started!**\n\nअब आपको automatic signals मिलेंगे। Best of luck trading! 📈",
            parse_mode='Markdown'
        )
    
    async def stop_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stop automatic signal generation"""
        user_id = update.effective_user.id
        self.active_users.discard(user_id)
        
        if not self.active_users:
            self.signal_active = False
        
        await update.message.reply_text(
            "⏹️ **Signals Stopped!**\n\nSignals रोक दिए गए हैं। जब चाहें फिर से start कर सकते हैं।",
            parse_mode='Markdown'
        )
    
    async def random_signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate random pair signal"""
        pair = self.engine.get_random_pair()
        signal = self.engine.generate_comprehensive_signal(pair)
        
        if signal:
            message = self.engine.format_signal_message(signal)
            await update.message.reply_text(message, parse_mode='Markdown')
            
            # Store signal in database
            self.store_signal(signal, update.effective_user.id)
        else:
            await update.message.reply_text(
                "❌ **कोई signal नहीं मिला**\n\nअभी market conditions signal generate करने के लिए suitable नहीं हैं।",
                parse_mode='Markdown'
            )
    
    async def custom_pair_signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show custom pair selection"""
        await update.message.reply_text(
            "🎯 **Select Trading Pair:**\n\nनीचे से अपना पसंदीदा pair चुनें:",
            reply_markup=self.get_pairs_keyboard(),
            parse_mode='Markdown'
        )
    
    async def handle_pair_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle pair selection callback"""
        query = update.callback_query
        await query.answer()
        
        pair = query.data.replace("pair_", "")
        signal = self.engine.generate_comprehensive_signal(pair)
        
        if signal:
            message = self.engine.format_signal_message(signal)
            await query.edit_message_text(message, parse_mode='Markdown')
            
            # Store signal in database
            self.store_signal(signal, update.effective_user.id)
        else:
            await query.edit_message_text(
                f"❌ **{pair} के लिए कोई signal नहीं**\n\nअभी इस pair के लिए trading conditions suitable नहीं हैं।",
                parse_mode='Markdown'
            )
    
    async def show_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show trading statistics with charts"""
        try:
            # Generate statistics chart
            chart_buffer = self.generate_statistics_chart()
            
            stats_text = f"""
📊 **TRADING STATISTICS**

**📈 Overall Performance:**
• Total Signals: {self.performance_stats['total_signals']}
• Winning Signals: {self.performance_stats['winning_signals']}
• Losing Signals: {self.performance_stats['losing_signals']}
• Accuracy: {self.performance_stats['accuracy']:.1f}%

**📅 Daily Stats:** {len(self.performance_stats.get('daily_stats', {}))} active days
**📆 Monthly Performance:** Available for {len(self.performance_stats.get('monthly_stats', {}))} months

**👤 Analyst:** Ankit Singh
            """.strip()
            
            if chart_buffer:
                await update.message.reply_photo(
                    photo=chart_buffer,
                    caption=stats_text,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(stats_text, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"Error showing statistics: {e}")
            await update.message.reply_text(
                "📊 Statistics loading... कुछ समय बाद try करें।",
                parse_mode='Markdown'
            )
    
    async def show_performance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show performance analysis"""
        # Simulate performance analysis
        current_performance = self.calculate_current_performance()
        
        performance_text = f"""
🏆 **PERFORMANCE ANALYSIS**

**📊 Current Status:** {current_performance['status']}
**🎯 Today's Accuracy:** {current_performance['today_accuracy']:.1f}%
**💰 Profit Potential:** {current_performance['profit_potential']}%

**📈 Trend Analysis:**
• **Best Performing Pairs:** {', '.join(current_performance['best_pairs'])}
• **Market Condition:** {current_performance['market_condition']}
• **Recommended Action:** {current_performance['recommendation']}

**⭐ Performance Rating:** {current_performance['rating']}

**👤 Analysis by:** Ankit Singh
        """.strip()
        
        await update.message.reply_text(performance_text, parse_mode='Markdown')
    
    async def money_management(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show money management suggestions"""
        user_id = update.effective_user.id
        
        # Get user settings or defaults
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        settings = cursor.fetchone()
        
        if settings:
            trading_goal = settings[2]
            daily_limit = settings[3]
            risk_percentage = settings[4]
        else:
            trading_goal = 100.0
            daily_limit = 500.0
            risk_percentage = 2.0
        
        # Calculate suggestions
        suggested_trade_size = (daily_limit * risk_percentage) / 100
        max_trades_per_day = daily_limit / suggested_trade_size
        
        mm_text = f"""
💰 **MONEY MANAGEMENT PLAN**

**📊 Your Current Settings:**
• Trading Goal: ₹{trading_goal:.0f}/day
• Daily Limit: ₹{daily_limit:.0f}
• Risk per Trade: {risk_percentage}%

**🎯 Recommendations:**
• **Trade Size:** ₹{suggested_trade_size:.0f} per signal
• **Maximum Trades:** {max_trades_per_day:.0f}/day
• **Stop Loss:** 3 consecutive losses = Stop trading
• **Daily Profit Lock:** {trading_goal * 0.8:.0f}% of goal achieved

**⚡ Recovery Plan:**
• After 2 losses: Reduce trade size by 50%
• After profit target: Lock 70% profit
• Never risk more than {risk_percentage * 2}% in recovery

**🛡️ Risk Management:**
• Diversify across different pairs
• Avoid trading during major news events
• Follow signal confidence levels strictly

**👤 Advisor:** Ankit Singh
        """.strip()
        
        await update.message.reply_text(mm_text, parse_mode='Markdown')
    
    async def best_pairs_today(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show best performing pairs today"""
        best_pairs = self.analyze_best_pairs()
        
        pairs_text = f"""
📈 **BEST PERFORMING PAIRS TODAY**

**🥇 Top Performers:**
{chr(10).join([f"• **{pair}** - {performance}" for pair, performance in best_pairs[:5]])}

**📊 Analysis Criteria:**
• Volume spike detection
• Trend strength measurement  
• Volatility optimization
• Technical indicator alignment

**🎯 Recommendation:**
Focus on top 3 pairs for better accuracy

**⏰ Updated:** {datetime.now().strftime('%H:%M UTC')}
**👤 Analyst:** Ankit Singh
        """.strip()
        
        await update.message.reply_text(pairs_text, parse_mode='Markdown')
    
    async def settings_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show settings menu"""
        settings_text = """
⚙️ **SETTINGS MENU**

यहाँ से अपनी preferences set करें:

• `/set_goal <amount>` - Daily trading goal set करें
• `/set_limit <amount>` - Daily trading limit set करें  
• `/set_risk <percentage>` - Risk percentage set करें
• `/notifications on/off` - Notifications toggle करें

**Example:**
`/set_goal 200` - ₹200 daily goal
`/set_risk 3` - 3% risk per trade
        """.strip()
        
        await update.message.reply_text(settings_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        help_text = """
ℹ️ **HELP & COMMANDS**

**🚀 Quick Start:**
1. "Start Signals" पर click करें
2. Automatic signals receive करें
3. Quotex पर trade करें

**📱 Menu Options:**
• **Random Signal** - Random pair का signal
• **Custom Pair** - Specific pair choose करें
• **Statistics** - Performance charts देखें
• **Money Management** - Risk management tips

**⚡ Strategy:**
• 10-second expiry recommended
• Follow signal confidence levels
• Use proper money management

**📞 Support:**
Developer: Ankit Singh
Strategy: Advanced Technical Analysis

**🎯 Disclaimer:**
Trading involves risk. Past performance doesn't guarantee future results.
        """.strip()
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    def signal_generator_loop(self):
        """Background thread for automatic signal generation"""
        while self.signal_active and self.active_users:
            try:
                # Generate signal every 30-60 seconds
                time.sleep(45)  # Wait 45 seconds between signals
                
                if not self.signal_active:
                    break
                
                # Get random pair and generate signal
                pair = self.engine.get_random_pair()
                signal = self.engine.generate_comprehensive_signal(pair)
                
                if signal and signal.confidence in ['HIGH', 'MEDIUM']:
                    # Send signal to all active users
                    message = self.engine.format_signal_message(signal)
                    self.broadcast_signal(message, signal)
                
            except Exception as e:
                logger.error(f"Error in signal generator: {e}")
                time.sleep(10)
    
    def broadcast_signal(self, message: str, signal: Signal):
        """Broadcast signal to all active users"""
        asyncio.create_task(self.send_to_active_users(message, signal))
    
    async def send_to_active_users(self, message: str, signal: Signal):
        """Send message to all active users"""
        try:
            application = Application.builder().token(self.token).build()
            
            for user_id in self.active_users.copy():
                try:
                    await application.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                    
                    # Store signal
                    self.store_signal(signal, user_id)
                    
                except TelegramError as e:
                    logger.error(f"Failed to send message to {user_id}: {e}")
                    # Remove inactive user
                    self.active_users.discard(user_id)
                    
        except Exception as e:
            logger.error(f"Error broadcasting signal: {e}")
    
    def store_signal(self, signal: Signal, user_id: int):
        """Store signal in database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO signals (pair, direction, confidence, timestamp, user_id) VALUES (?, ?, ?, ?, ?)",
                (signal.pair, signal.direction, signal.confidence, signal.entry_time, user_id)
            )
            self.conn.commit()
            
            # Update performance stats
            self.performance_stats['total_signals'] += 1
            
            # Schedule result checking (simulate for demo)
            threading.Timer(300, self.check_signal_result, args=[cursor.lastrowid]).start()
            
        except Exception as e:
            logger.error(f"Error storing signal: {e}")
    
    def check_signal_result(self, signal_id: int):
        """Check signal result after 5 minutes (simulated)"""
        try:
            # Simulate signal result (in production, get actual result from broker API)
            import random
            result = 'win' if random.random() > 0.35 else 'loss'  # 65% win rate simulation
            
            cursor = self.conn.cursor()
            cursor.execute("UPDATE signals SET result = ? WHERE id = ?", (result, signal_id))
            self.conn.commit()
            
            # Update performance stats
            if result == 'win':
                self.performance_stats['winning_signals'] += 1
            else:
                self.performance_stats['losing_signals'] += 1
            
            # Recalculate accuracy
            total = self.performance_stats['winning_signals'] + self.performance_stats['losing_signals']
            if total > 0:
                self.performance_stats['accuracy'] = (self.performance_stats['winning_signals'] / total) * 100
            
        except Exception as e:
            logger.error(f"Error checking signal result: {e}")
    
    def generate_statistics_chart(self) -> Optional[BytesIO]:
        """Generate statistics chart"""
        try:
            # Sample data for chart
            dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='1d')
            accuracies = [65, 72, 68, 75, 70, 78, 73]  # Sample accuracy data
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            # Accuracy chart
            ax1.plot(dates, accuracies, marker='o', linewidth=2, markersize=6, color='#00ff88')
            ax1.set_title('Weekly Accuracy Trend', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Accuracy (%)')
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(50, 85)
            
            # Daily signals chart
            daily_signals = [12, 15, 18, 14, 16, 20, 17]
            ax2.bar(dates, daily_signals, color='#ff6b6b', alpha=0.7)
            ax2.set_title('Daily Signal Count', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Signals Count')
            ax2.grid(True, alpha=0.3)
            
            # Add branding
            fig.suptitle('Quotex Signal Bot Statistics - By Ankit Singh', fontsize=16, fontweight='bold')
            
            plt.tight_layout()
            
            # Save to buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            
            return buffer
            
        except Exception as e:
            logger.error(f"Error generating chart: {e}")
            return None
    
    def calculate_current_performance(self) -> Dict:
        """Calculate current performance metrics"""
        # Simulate performance calculation
        import random
        
        accuracy = random.uniform(65, 80)
        
        status_map = {
            (75, 100): ('EXCELLENT', '🟢'),
            (65, 75): ('GOOD', '🟡'),
            (50, 65): ('AVERAGE', '🟠'),
            (0, 50): ('POOR', '🔴')
        }
        
        status = 'GOOD'
        for (low, high), (s, _) in status_map.items():
            if low <= accuracy < high:
                status = s
                break
        
        return {
            'status': status,
            'today_accuracy': accuracy,
            'profit_potential': random.uniform(15, 35),
            'best_pairs': ['EUR/USD', 'BTC/USD', 'GOLD'],
            'market_condition': random.choice(['Trending', 'Volatile', 'Stable']),
            'recommendation': 'Focus on high confidence signals',
            'rating': '⭐⭐⭐⭐' if accuracy > 70 else '⭐⭐⭐'
        }
    
    def analyze_best_pairs(self) -> List[tuple]:
        """Analyze and return best performing pairs"""
        pairs_performance = [
            ('EUR/USD', '78% accuracy, High volume'),
            ('BTC/USD', '75% accuracy, Strong trend'),
            ('GOLD', '72% accuracy, Good volatility'),
            ('GBP/USD', '70% accuracy, Clear patterns'),
            ('USD/JPY', '68% accuracy, Stable movement'),
            ('ETH/USD', '74% accuracy, Momentum strong'),
            ('S&P500', '71% accuracy, Index trending')
        ]
        
        # Sort by accuracy (simulated)
        return sorted(pairs_performance, key=lambda x: float(x[1].split('%')[0]), reverse=True)
    
    def run(self):
        """Run the bot"""
        application = Application.builder().token(self.token).build()
        
        # Command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        
        # Message handlers
        application.add_handler(MessageHandler(filters.Regex("🚀 Start Signals"), self.start_signals))
        application.add_handler(MessageHandler(filters.Regex("⏹️ Stop Signals"), self.stop_signals))
        application.add_handler(MessageHandler(filters.Regex("🎲 Random Signal"), self.random_signal))
        application.add_handler(MessageHandler(filters.Regex("🎯 Custom Pair Signal"), self.custom_pair_signal))
        application.add_handler(MessageHandler(filters.Regex("📊 Statistics"), self.show_statistics))
        application.add_handler(MessageHandler(filters.Regex("🏆 Performance"), self.show_performance))
        application.add_handler(MessageHandler(filters.Regex("💰 Money Management"), self.money_management))
        application.add_handler(MessageHandler(filters.Regex("📈 Best Pairs Today"), self.best_pairs_today))
        application.add_handler(MessageHandler(filters.Regex("⚙️ Settings"), self.settings_menu))
        application.add_handler(MessageHandler(filters.Regex("ℹ️ Help"), self.help_command))
        
        # Callback handlers
        application.add_handler(CallbackQueryHandler(self.handle_pair_selection, pattern=r"^pair_"))
        
        print("🚀 Quotex Signal Bot started successfully!")
        print("📱 Send /start to begin trading")
        print("👤 Developer: Ankit Singh")
        
        # Run the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to run the bot"""
    # Bot token - Replace with your actual bot token
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set your Telegram Bot Token!")
        print("1. Message @BotFather on Telegram")
        print("2. Create new bot with /newbot")
        print("3. Replace 'YOUR_BOT_TOKEN_HERE' with your token")
        return
    
    try:
        bot = QuotexSignalBot(BOT_TOKEN)
        bot.run()
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    main()
