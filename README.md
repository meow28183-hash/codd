_# Telegram-Triggered Always-On Self-Updating AI Developer + Supervisor Bot

This bot is a complete AI-powered developer that lives in your Telegram. It can generate projects from scratch, fix existing ones, and even update its own code.

## Features
- **Telegram-triggered**: Starts working immediately upon receiving a project idea.
- **Background processing**: Continuous generation of multi-file projects.
- **Gemini API Integration**: Uses Google's Gemini 1.5 Pro for high-quality code generation and analysis.
- **Self-Update**: Can modify its own modules safely when instructed.
- **GitHub Integration**: Clone, fix, and push projects to GitHub.
- **Auto-Fix**: Analyzes errors and applies fixes automatically.
- **ZIP Delivery**: Sends completed projects as ZIP files via Telegram.

## Setup

### 1. Environment Variables
Create a `.env` file or set the following secrets:
- `TELEGRAM_TOKEN`: Your bot token from @BotFather.
- `GEMINI_API_KEY`: Your API key from Google AI Studio.
- `GITHUB_PAT`: (Optional) Personal Access Token for GitHub operations.

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Running
```bash
python main.py
```

## Deployment
- **GitHub Actions**: Use the provided workflow in `.github/workflows/bot.yml`.
- **Always-on**: Can be deployed to Replit or Render for continuous background processing.

## Usage Examples
- "Create a Flask blog app with login and posts"
- "Add search and tag filtering to my project"
- "How's my project going?" (Status check)
- "Add logging to yourself" (Self-update)
_
