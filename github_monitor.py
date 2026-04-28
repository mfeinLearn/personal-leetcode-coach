from github import Github
import os
from datetime import datetime, timedelta

def get_recent_commits(repo_name, days=7):
    g = Github(os.getenv("GH_TOKEN"))
    repo = g.get_repo(repo_name)
    since = datetime.now() - timedelta(days=days)
    commits = repo.get_commits(since=since)
    
    files_changed = []
    for commit in commits:
        for file in commit.files:
            if file.filename.endswith(('.py', '.java', '.cpp', '.js')):
                files_changed.append({
                    'filename': file.filename,
                    'content': file.patch or file.raw_url
                })
    return files_changed