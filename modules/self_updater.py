import os
import sys
import logging
import subprocess
from core.gemini import GeminiClient

class SelfUpdater:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini = gemini_client
        self.logger = logging.getLogger(__name__)

    async def update_module(self, module_path: str, instruction: str):
        if not os.path.exists(module_path):
            return False, f"Module {module_path} not found."

        with open(module_path, 'r') as f:
            current_code = f.read()

        new_code = await self.gemini.analyze_and_fix(current_code, f"Instruction: {instruction}")
        
        try:
            compile(new_code, module_path, 'exec')
        except Exception as e:
            return False, f"Generated code has syntax errors: {e}"

        with open(f"{module_path}.bak", 'w') as f:
            f.write(current_code)

        with open(module_path, 'w') as f:
            f.write(new_code)

        return True, "Module updated successfully."

    def restart_bot(self):
        self.logger.info("Restarting bot...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    async def daily_self_improvement(self):
        """
        Suggests and applies a new feature to the bot itself.
        """
        self.logger.info("Starting daily self-improvement...")
        
        # Ask Long Cat AI for a suggestion
        prompt = "Suggest one small but useful new feature or improvement for an AI Developer Telegram Bot. Return ONLY the suggestion as a short sentence."
        try:
            response = self.gemini.client.chat.completions.create(
                model=self.gemini.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            suggestion = response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Failed to get suggestion from Long Cat AI: {e}")
            return False, str(e)
        
        self.logger.info(f"Gemini suggested: {suggestion}")
        
        # For now, we'll target a specific module to improve, e.g., utils/logger.py or adding a new utility
        # In a more advanced version, Gemini could decide which file to edit.
        # Let's try to improve the logger or add a new helper.
        target_file = "utils/logger.py"
        success, message = await self.update_module(target_file, f"Implement this improvement: {suggestion}")
        
        if success:
            self.logger.info(f"Daily improvement applied: {suggestion}")
            return True, suggestion
        else:
            self.logger.error(f"Daily improvement failed: {message}")
            return False, message
