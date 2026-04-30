from github_monitor import get_recent_commits
# from claude_analyzer import analyze_code_with_claude
from openai_analyzer import analyze_code_with_openai
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
    # analysis = analyze_code_with_claude(combined_code, user_goal, previous_mistakes)
    analysis = analyze_code_with_openai(combined_code, user_goal, previous_mistakes)
    
    print("📧 Sending weekly email...")
    send_weekly_email(analysis)
    
    print("✅ Weekly analysis complete!")

if __name__ == "__main__":
    run_weekly_analysis()