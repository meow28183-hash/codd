import os
import logging
import asyncio
from dotenv import load_dotenv
from core.bot import AIDevBot
from modules.self_updater import SelfUpdater
from core.gemini import GeminiClient

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def daily_task(updater: SelfUpdater):
    """
    Runs the self-improvement task once every 24 hours.
    """
    while True:
        try:
            logging.info("Checking for daily self-improvement...")
            success, suggestion = await updater.daily_self_improvement()
            if success:
                logging.info(f"Successfully applied daily improvement: {suggestion}")
            else:
                logging.error(f"Daily improvement failed: {suggestion}")
        except Exception as e:
            logging.error(f"Error in daily task: {e}")
        
        # Wait for 24 hours
        await asyncio.sleep(24 * 3600)

async def run_bot():
    load_dotenv()
    
    token = os.getenv("TELEGRAM_TOKEN")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not token or not gemini_key:
        logging.error("TELEGRAM_TOKEN and GEMINI_API_KEY must be set in .env file")
        return

    # Ensure data directories exist
    os.makedirs("data/projects", exist_ok=True)
    os.makedirs("data/zips", exist_ok=True)

    bot = AIDevBot(token, gemini_key)
    updater = SelfUpdater(bot.gemini)
    
    # Start the daily improvement task in the background
    asyncio.create_task(daily_task(updater))
    
    # Run the bot
    # Note: python-telegram-bot's run_polling is blocking, so we use it as the main entry
    bot.run()

def main():
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
