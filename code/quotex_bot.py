import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

class QuotexSignalBot:
    def __init__(self, token):
        self.token = token
        self.active_users = set()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("🚀 Start Signals", callback_data='start')],
            [InlineKeyboardButton("⏹️ Stop Signals", callback_data='stop')],
            [InlineKeyboardButton("🎲 Random Signal", callback_data='random')],
            [InlineKeyboardButton("📊 Statistics", callback_data='stats')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Welcome to Quotex Signal Bot!", reply_markup=reply_markup)

    async def start_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.active_users.add(user_id)
        await update.message.reply_text("✅ Signals started!")

    async def stop_signals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.active_users.discard(user_id)
        await update.message.reply_text("⏹️ Signals stopped.")

    async def random_signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🎲 Random Signal: EURUSD - BUY ✅")

    async def handle_pair_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"You selected {query.data}")

    async def show_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📊 Statistics: Wins: 10 | Losses: 2 | Accuracy: 83%")

    async def show_performance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🏆 Performance: GOOD")

    async def money_management(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("💰 Money Management Advice:\nRisk per trade: 2%")

    async def best_pairs_today(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📈 Best Performing Pairs Today:\n1️⃣ EURUSD\n2️⃣ GBPJPY\n3️⃣ BTCUSD")

    async def settings_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("⚙️ Settings coming soon...")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("ℹ️ Help:\n/start - Start the bot\nUse menu buttons to navigate.")

    async def run(self):
        application = Application.builder().token(self.token).build()

        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^🚀 Start Signals$"), self.start_signals))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^⏹️ Stop Signals$"), self.stop_signals))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^🎲 Random Signal$"), self.random_signal))
        application.add_handler(CallbackQueryHandler(self.handle_pair_selection, pattern=r"^pair_"))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^📊 Statistics$"), self.show_statistics))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^🏆 Performance$"), self.show_performance))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^💰 Money Management$"), self.money_management))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^📈 Best Pairs Today$"), self.best_pairs_today))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^⚙️ Settings$"), self.settings_menu))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^ℹ️ Help$"), self.help_command))

        await application.run_polling()
