import asyncio
import logging
import os
import shutil
import zipfile
from typing import Dict, Any, List
from telegram import Bot
from core.gemini import GeminiClient

def create_zip(source_dir: str, output_filename: str) -> str:
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    shutil.make_archive(output_filename.replace('.zip', ''), 'zip', source_dir)
    return output_filename

class ProjectProcessor:
    def __init__(self, gemini_client: GeminiClient, telegram_bot: Bot, chat_id: int):
        self.gemini = gemini_client
        self.bot = telegram_bot
        self.chat_id = chat_id
        self.logger = logging.getLogger(__name__)
        self.active_projects = {}

    async def start_new_project(self, project_id: str, goal: str):
        self.active_projects[project_id] = {
            "goal": goal,
            "status": "starting",
            "files_generated": 0,
            "total_files": 0,
            "path": f"data/projects/{project_id}"
        }
        os.makedirs(self.active_projects[project_id]["path"], exist_ok=True)
        
        await self.bot.send_message(self.chat_id, f"✅ Project generation started: {project_id}\nWorking in the background...")
        
        # Run generation in background
        asyncio.create_task(self._generate_project(project_id))

    async def _generate_project(self, project_id: str):
        try:
            project = self.active_projects[project_id]
            structure = await self.gemini.generate_project_structure(project["goal"])
            if not structure:
                raise Exception("Failed to generate project structure.")
                
            project["total_files"] = len(structure)
            project["status"] = "generating"
            
            context = f"Project Structure: {list(structure.keys())}"
            
            for file_path, description in structure.items():
                full_path = os.path.join(project["path"], file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                content = await self.gemini.generate_file_content(file_path, context, project["goal"])
                with open(full_path, "w") as f:
                    f.write(content)
                
                project["files_generated"] += 1
                if project["files_generated"] % 5 == 0:
                    await self.bot.send_message(self.chat_id, f"📊 Progress for {project_id}: {project['files_generated']}/{project['total_files']} files done.")

            project["status"] = "completed"
            zip_path = create_zip(project["path"], f"data/zips/{project_id}.zip")
            
            await self.bot.send_message(self.chat_id, f"📦 Project ready: {project_id}")
            with open(zip_path, "rb") as f:
                await self.bot.send_document(self.chat_id, f, filename=f"{project_id}.zip")
                
        except Exception as e:
            self.logger.error(f"Error generating project {project_id}: {e}")
            await self.bot.send_message(self.chat_id, f"❌ Error generating project {project_id}: {str(e)}")

    async def get_status(self, project_id: str = None) -> str:
        if not self.active_projects:
            return "No active projects."
        
        if project_id and project_id in self.active_projects:
            p = self.active_projects[project_id]
            return f"📊 Project Progress: {project_id} {int(p['files_generated']/p['total_files']*100 if p['total_files'] > 0 else 0)}% complete, {p['files_generated']}/{p['total_files']} files generated."
        
        report = "📊 Current Projects:\n"
        for pid, p in self.active_projects.items():
            report += f"- {pid}: {p['status']} ({p['files_generated']}/{p['total_files']})\n"
        return report
