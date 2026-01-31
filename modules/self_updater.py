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
