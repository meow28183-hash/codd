# Manus AI - The Intelligent Self-Updating Developer

Manus is a state-of-the-art AI-powered developer that lives in your Telegram. It can generate projects from scratch, fix existing ones, and even update its own code to become smarter over time.

## 🚀 Features
- **Manus Intelligence**: Powered by advanced LLMs to provide expert-level coding and architectural advice.
- **Telegram-triggered**: Starts working immediately upon receiving a project idea.
- **Background processing**: Continuous generation of multi-file projects.
- **Self-Update**: Can modify its own modules safely when instructed.
- **GitHub Integration**: Clone, fix, and push projects to GitHub.
- **Auto-Fix**: Analyzes errors and applies fixes automatically.
- **Web Interface**: Includes a health check endpoint for cloud deployment.

## 🛠 Setup

### 1. Environment Variables
Create a `.env` file or set the following secrets:
- `TELEGRAM_TOKEN`: Your bot token from @BotFather.
- `GEMINI_API_KEY`: Your API key for the LLM provider.
- `GITHUB_PAT`: (Optional) Personal Access Token for GitHub operations.

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Running
```bash
python server.py
```

## 🌐 Deployment
This app is designed to be deployed as a **Web Service** on platforms like **Render**.
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python server.py`
- **Health Check Path**: `/`

## 💡 Usage Examples
- "Create a Flask blog app with login and posts"
- "Add search and tag filtering to my project"
- "How's my project going?" (Status check)
- "Add logging to yourself" (Self-update)
