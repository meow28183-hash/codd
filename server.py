from flask import Flask
import threading
import os
import main

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Manus AI Bot is running!", 200

def run_bot():
    main.main()

if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Run the Flask server
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
