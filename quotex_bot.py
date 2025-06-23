async def run(self):
        """Run the bot"""
        application = Application.builder().token(self.token).build()

        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^🚀 Start Signals$"), self.start_signals))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^⏹️ Stop Signals$"), self.stop_signals))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^🎲 Random Signal$"), self.random_signal))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^🎯 Custom Pair Signal$"), self.custom_pair_signal))
        application.add_handler(CallbackQueryHandler(self.handle_pair_selection, pattern=r"^pair_"))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^📊 Statistics$"), self.show_statistics))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^🏆 Performance$"), self.show_performance))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^💰 Money Management$"), self.money_management))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^📈 Best Pairs Today$"), self.best_pairs_today))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^⚙️ Settings$"), self.settings_menu))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^ℹ️ Help$"), self.help_command))

        await application.run_polling()
