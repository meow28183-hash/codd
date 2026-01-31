import os
import logging
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from core.gemini import GeminiClient

logger = logging.getLogger(__name__)

class AIDevBot:
    def __init__(self, token: str, gemini_key: str):
        self.app = ApplicationBuilder().token(token).build()
        self.gemini = GeminiClient(gemini_key)
        self.system_prompt = (
            "You are a highly intelligent, helpful, and creative AI assistant. "
            "You provide clear, accurate, and insightful responses. "
            "If the user asks for code, provide production-ready, well-commented code. "
            "Maintain a professional yet friendly tone."
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "👋 Hello! I’m your Smart AI Telegram Bot.\n"
            "💡 I can chat, answer questions, and even help with code. How can I assist you today?"
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return

        user_text = update.message.text
        chat_id = update.effective_chat.id

        await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

        try:
            # Use GeminiClient for general chat responses
            ai_reply = await self.gemini.generate_chat_response(user_text, self.system_prompt)

            if len(ai_reply) > 4000:
                for i in range(0, len(ai_reply), 4000):
                    await update.message.reply_text(ai_reply[i:i+4000])
            else:
                await update.message.reply_text(ai_reply)

        except Exception as e:
            logger.error(f"Error calling AI: {e}")
            await update.message.reply_text("❌ Sorry, I encountered an error while thinking. Please try again.")

    def run(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        self.logger.info("Bot is running...")
        self.app.run_polling()
