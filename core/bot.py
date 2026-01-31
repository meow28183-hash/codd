import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from core.gemini import GeminiClient
from core.processor import ProjectProcessor

class AIDevBot:
    def __init__(self, token: str, gemini_key: str):
        self.app = ApplicationBuilder().token(token).build()
        self.gemini = GeminiClient(gemini_key)
        self.processor = None 
        self.logger = logging.getLogger(__name__)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "👋 Hello! I’m your AI Developer Bot.\n"
            "💡 Send a project idea, upload an app to fix, or request self-updates."
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        text = update.message.text

        if not self.processor:
            self.processor = ProjectProcessor(self.gemini, context.bot, chat_id)

        if text.lower() in ["hi", "hello", "/start"]:
            await self.start(update, context)
            return

        if any(word in text.lower() for word in ["status", "how's", "progress"]):
            status = await self.processor.get_status()
            await update.message.reply_text(status)
            return

        # Start new project
        project_id = f"project_{len(self.processor.active_projects) + 1}"
        await self.processor.start_new_project(project_id, text)

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔍 Analyzing uploaded project... (Feature being implemented)")

    def run(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        self.logger.info("Bot is running...")
        self.app.run_polling()
