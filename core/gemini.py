import google.generativeai as genai
import os
import json
import logging
from typing import List, Dict, Any

class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.logger = logging.getLogger(__name__)

    async def generate_project_structure(self, prompt: str) -> Dict[str, Any]:
        system_prompt = """
        You are an expert software architect. Given a project idea, generate a complete file structure.
        Return ONLY a JSON object where keys are file paths and values are brief descriptions of what each file should contain.
        Example: {"main.py": "Entry point", "utils/helper.py": "Helper functions"}
        """
        response = self.model.generate_content(f"{system_prompt}\n\nProject Idea: {prompt}")
        try:
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()
            return json.loads(text)
        except Exception as e:
            self.logger.error(f"Failed to parse project structure: {e}")
            return {}

    async def generate_file_content(self, file_path: str, context: str, project_goal: str) -> str:
        prompt = f"""
        Project Goal: {project_goal}
        File Path: {file_path}
        Context: {context}
        
        Generate the complete, production-ready code for this file. 
        Include necessary imports, comments, and follow best practices.
        Return ONLY the code content. If you use markdown blocks, I will strip them.
        """
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            # Strip language identifier if present
            lines = text.split('\n')
            if lines[0].startswith("```"):
                text = '\n'.join(lines[1:-1])
        return text

    async def analyze_and_fix(self, code: str, error: str = None) -> str:
        prompt = f"""
        Analyze the following code and provide a fix or improvement.
        Code:
        {code}
        
        Error (if any): {error}
        
        Return the complete corrected code.
        """
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            lines = text.split('\n')
            if lines[0].startswith("```"):
                text = '\n'.join(lines[1:-1])
        return text
