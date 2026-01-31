from openai import OpenAI
import os
import json
import logging
from typing import List, Dict, Any

class GeminiClient:
    """
    Renamed to GeminiClient to maintain compatibility with existing code, 
    but now uses Long Cat AI API.
    """
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            # base_url="https://api.longcat.chat/openai" # Removed non-standard API base_url
            # The default OpenAI API base_url will be used, which is configured for Gemini in this environment.
        )
        self.model_name = "gpt-4.1-mini" # Using a more capable model available in the environment
        self.logger = logging.getLogger(__name__)

    async def generate_project_structure(self, prompt: str) -> Dict[str, Any]:
        system_prompt = """
        You are an expert software architect. Given a project idea, generate a complete file structure.
        Return ONLY a JSON object where keys are file paths and values are brief descriptions of what each file should contain.
        Example: {"main.py": "Entry point", "utils/helper.py": "Helper functions"}
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Project Idea: {prompt}"}
                ],
                response_format={"type": "json_object"}
            )
            text = response.choices[0].message.content.strip()
            return json.loads(text)
        except Exception as e:
            self.logger.error(f"Failed to parse project structure: {e}")
            # Fallback for models that might not support response_format
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Project Idea: {prompt}"}
                    ]
                )
                text = response.choices[0].message.content.strip()
                if text.startswith("```json"):
                    text = text[7:-3].strip()
                elif text.startswith("```"):
                    text = text[3:-3].strip()
                return json.loads(text)
            except Exception as e2:
                self.logger.error(f"Fallback also failed: {e2}")
            return {}

    async def generate_chat_response(self, user_message: str, system_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Failed to generate chat response: {e}")
            return "I apologize, but I encountered an error trying to generate a response." 

    async def generate_file_content(self, file_path: str, context: str, project_goal: str) -> str:
        prompt = f"""
        Project Goal: {project_goal}
        File Path: {file_path}
        Context: {context}
        
        Generate the complete, production-ready code for this file. 
        Include necessary imports, comments, and follow best practices.
        Return ONLY the code content. Do not include markdown blocks.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = response.choices[0].message.content.strip()
            if text.startswith("```"):
                lines = text.split('\n')
                if lines[0].startswith("```"):
                    text = '\n'.join(lines[1:-1])
            return text
        except Exception as e:
            self.logger.error(f"Failed to generate file content: {e}")
            return f"# Error generating content: {str(e)}"

    async def analyze_and_fix(self, code: str, error: str = None) -> str:
        prompt = f"""
        Analyze the following code and provide a fix or improvement.
        Code:
        {code}
        
        Error (if any): {error}
        
        Return the complete corrected code. Do not include markdown blocks.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            text = response.choices[0].message.content.strip()
            if text.startswith("```"):
                lines = text.split('\n')
                if lines[0].startswith("```"):
                    text = '\n'.join(lines[1:-1])
            return text
        except Exception as e:
            self.logger.error(f"Failed to analyze and fix: {e}")
            return code
