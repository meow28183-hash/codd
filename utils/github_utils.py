import os
import logging
from git import Repo

class GitHubManager:
    def __init__(self, pat: str = None):
        self.pat = pat or os.getenv("GITHUB_PAT")
        self.logger = logging.getLogger(__name__)

    def push_to_github(self, local_path: str, repo_url: str, commit_message: str = "Update from AI Dev Bot"):
        try:
            auth_url = repo_url
            if self.pat and "github.com" in repo_url:
                auth_url = repo_url.replace("https://", f"https://{self.pat}@")

            if not os.path.exists(os.path.join(local_path, ".git")):
                repo = Repo.init(local_path)
                repo.create_remote('origin', auth_url)
            else:
                repo = Repo(local_path)
                if 'origin' not in repo.remotes:
                    repo.create_remote('origin', auth_url)
                else:
                    repo.remotes.origin.set_url(auth_url)

            repo.git.add(A=True)
            repo.index.commit(commit_message)
            # Try pushing to main or master
            try:
                repo.remotes.origin.push('master')
            except:
                repo.remotes.origin.push('main')
            return True, "Successfully pushed to GitHub."
        except Exception as e:
            self.logger.error(f"GitHub push failed: {e}")
            return False, str(e)

    def clone_repo(self, repo_url: str, local_path: str):
        try:
            auth_url = repo_url
            if self.pat and "github.com" in repo_url:
                auth_url = repo_url.replace("https://", f"https://{self.pat}@")
            
            Repo.clone_from(auth_url, local_path)
            return True, "Repository cloned successfully."
        except Exception as e:
            self.logger.error(f"GitHub clone failed: {e}")
            return False, str(e)
