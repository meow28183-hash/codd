import os
import logging
from dotenv import load_dotenv
from core.bot import AIDevBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    load_dotenv()
    
    token = os.getenv("TELEGRAM_TOKEN")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not token or not gemini_key:
        logging.error("TELEGRAM_TOKEN and GEMINI_API_KEY must be set in .env file")
        return

    bot = AIDevBot(token, gemini_key)
    
    # Run the bot
    bot.run()

if __name__ == "__main__":
    main()
