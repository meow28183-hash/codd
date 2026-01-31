import os
import logging
import asyncio
from dotenv import load_dotenv
from core.bot import AIDevBot
from modules.self_updater import SelfUpdater

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

def main():
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
    
    # Use the post_init hook to start the background task
    async def post_init(application):
        asyncio.create_task(daily_task(updater))

    bot.app.post_init = post_init
    
    # Run the bot
    bot.run()

if __name__ == "__main__":
    main()
