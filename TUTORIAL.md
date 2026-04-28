# How to Build Your Personal LeetCode Improvement Coding Buddy Bot

# LeetCode Coding Buddy

An AI-powered LeetCode coaching bot that monitors your GitHub pushes, analyzes your code with Claude, tracks mistake patterns, and sends personalized weekly improvement summaries via email.

---

## Features

- Monitors your GitHub repository for new code pushes
- Uses **Claude 3.5 Sonnet** for intelligent code analysis
- Detects recurring mistake patterns
- Sends a professional weekly email summary every Sunday
- Tracks long-term progress and mistake history
- Supports dynamic goal setting (monthly check-ins)
- Fully automated using GitHub Actions (free)

---

## Getting Started

Follow the steps below to build and deploy your own LeetCode Coding Buddy.

### 1. Get Your Anthropic API Key

1. Go to [https://console.anthropic.com](https://console.anthropic.com)
2. Create an account and generate a new API key
3. Copy the key (starts with `sk-ant-...`)

### 2. Project Setup

```bash
mkdir leetcode-coding-buddy
cd leetcode-coding-buddy
git init
python -m venv venv
source venv/bin/activate          # On Windows use: venv\Scripts\activate
```

---

### 3. Install Required Libraries

Create a file named `requirements.txt` and add the following:

```
requests
python-dotenv
anthropic
resend
PyGithub
```

Then install the dependencies:

```
pip install -r requirements.txt
```

### 4. Project Structure

Create the following files and folders:

```
leetcode-coding-buddy/
├── .env
├── requirements.txt
├── main.py
├── github_monitor.py
├── claude_analyzer.py
├── email_sender.py
├── progress_tracker.py
├── goals.py
├── config.py
├── user_progress.json
├── user_goals.json
└── .github/
    └── workflows/
        └── weekly-summary.yml
```

### 5. Configuration Files

Create `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
```

Create `.env` (replace with your own values):

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
REPO_NAME=yourusername/leetcode-solutions
YOUR_EMAIL=your@email.com
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 6. Core Code Files

`github_monitor.py`

```python

from github import Github
import os
from datetime import datetime, timedelta

def get_recent_commits(repo_name, days=7):
    g = Github(os.getenv("GITHUB_TOKEN"))
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
```

`claude_analyzer.py`

```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_code_with_claude(code_snippets, user_goal, previous_mistakes=""):
    prompt = f"""You are an expert LeetCode coach and mentor.

User's current focus area: {user_goal}

Here is the code the user pushed this week:

{code_snippets}

Previous mistakes the user has made (if any):
{previous_mistakes}

Please analyze the code and respond in this exact format:

## Weekly Summary
[Short encouraging overview]

## Strengths
- Bullet points of what they did well

## Areas for Improvement
- Specific, actionable feedback

## Mistake Patterns Detected
- List any recurring mistakes

## Recommended Problems for Next Week
1. Problem Name - Difficulty - Link
2. ...

## Overall Feedback
[Motivating closing message]

Keep the tone supportive but honest. Be specific and reference actual code patterns when possible."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

```

### 7. Email Sender

`email_sender.py`

```python
import resend
import os
from datetime import datetime

resend.api_key = os.getenv("RESEND_API_KEY")

def send_weekly_email(analysis_result, user_name="there"):
    subject = f"Your Weekly LeetCode Coaching Report – {datetime.now().strftime('%B %d, %Y')}"

    html_content = f"""
    <h2>Hi {user_name},</h2>
    <p>Here's your personalized LeetCode summary for this week:</p>

    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
        {analysis_result.replace('\n', '<br>')}
    </div>

    <p style="margin-top: 30px;">
        <strong>Quick Feedback:</strong><br>
        Was this analysis helpful?
    </p>

    <p>Keep up the great work!</p>
    <p><strong>Your Coding Buddy</strong><br><em>Powered by Claude</em></p>
    """

    params = {
        "from": "LeetCode Buddy <onboarding@resend.dev>",
        "to": [os.getenv("YOUR_EMAIL")],
        "subject": subject,
        "html": html_content,
    }
    resend.Emails.send(params)
    print("✅ Weekly email sent successfully!")

```

### 8. Main Script

`main.py`

```python
from github_monitor import get_recent_commits
from claude_analyzer import analyze_code_with_claude
from email_sender import send_weekly_email
from progress_tracker import get_recent_mistakes
import os

def run_weekly_analysis():
    print("🔍 Checking for new code pushes...")
    code_changes = get_recent_commits(os.getenv("REPO_NAME"), days=7)

    if not code_changes:
        print("No new code pushes found this week.")
        return

    combined_code = "\n\n".join([f"File: {item['filename']}\n{item['content']}"
                                  for item in code_changes])

    user_goal = "Graphs"
    previous_mistakes = get_recent_mistakes()

    print("🧠 Sending code to Claude for analysis...")
    analysis = analyze_code_with_claude(combined_code, user_goal, previous_mistakes)

    print("📧 Sending weekly email...")
    send_weekly_email(analysis)

    print("✅ Weekly analysis complete!")

if __name__ == "__main__":
    run_weekly_analysis()

```

### 9. GitHub Actions Workflow

Create the file `.github/workflows/weekly-summary.yml`:

```yaml
name: Weekly LeetCode Summary

on:
  schedule:
    - cron: "0 10 * * 0"
  workflow_dispatch:

jobs:
  weekly-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run Weekly Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          REPO_NAME: ${{ secrets.REPO_NAME }}
          YOUR_EMAIL: ${{ secrets.YOUR_EMAIL }}
          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
        run: python main.py
```

### 10. Add GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions and add the following secrets:

```
ANTHROPIC_API_KEY
GITHUB_TOKEN
REPO_NAME
YOUR_EMAIL
RESEND_API_KEY
```

### 11. Progress Tracking & Mistake Logs

`progress_tracker.py`

```python
import json
import os
from datetime import datetime

DATA_FILE = "user_progress.json"

def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"mistakes": [], "weekly_summaries": []}

def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_mistake(mistake_description):
    data = load_progress()
    data["mistakes"].append({
        "date": str(datetime.now().date()),
        "description": mistake_description
    })
    save_progress(data)

def get_recent_mistakes(limit=5):
    data = load_progress()
    return "\n".join([m["description"] for m in data["mistakes"][-limit:]])
```

### 12. Dynamic Goals (Monthly Check-in)

`goals.py`

```
import json
import os
from datetime import datetime

GOALS_FILE = "user_goals.json"

def load_goals():
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "r") as f:
            return json.load(f)
    return {"current_goal": "Graphs", "last_updated": str(datetime.now().date())}

def save_goal(new_goal):
    data = {"current_goal": new_goal, "last_updated": str(datetime.now().date())}
    with open(GOALS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def should_ask_new_goal():
    data = load_goals()
    last = datetime.strptime(data["last_updated"], "%Y-%m-%d")
    return (datetime.now() - last).days >= 30
```

### 13. How to Test Locally

Run the following command:

```bash
python main.py
```

Check your email inbox for the weekly report.

14. Deployment
    The project is already configured to run automatically every Sunday using GitHub Actions (completely free).
    Alternative free hosting platforms:

Railway
Render
PythonAnywhere

15. gitignore

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Virtual environments
venv/
.venv/
ENV/
env/
ENV.bak/
env.bak/

# IDE / Editor folders
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables (IMPORTANT - never commit your API keys)
.env
.env.local
.env.*.local

# Local data files (user-specific progress and goals)
user_progress.json
user_goals.json

# macOS
.DS_Store

# Windows
Thumbs.db
ehthumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
```

How to use it:

Create a new file in your project root called .gitignore
Paste the content above into it
Save the file

License
MIT License

Built with ❤️ using Claude AI and Grok
