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

    # Ensure data directories exist
    os.makedirs("data/projects", exist_ok=True)
    os.makedirs("data/zips", exist_ok=True)

    bot = AIDevBot(token, gemini_key)
    bot.run()

if __name__ == "__main__":
    main()
