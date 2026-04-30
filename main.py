from github_monitor import get_recent_commits
from openai_analyzer import analyze_code_with_openai
from email_sender import send_weekly_email
from progress_tracker import load_progress, save_progress
from goals import load_goals
from datetime import datetime
import os

def run_weekly_analysis():
    print("🔍 Checking for new code pushes...")
    
    code_changes = get_recent_commits(os.getenv("REPO_NAME"), days=7)
    
    if not code_changes:
        print("No new code pushes found this week.")
        return
    
    combined_code = "\n\n".join([f"File: {item['filename']}\n{item['content']}" 
                                  for item in code_changes])
    
    # Load current goal from user_goals.json
    user_goal = load_goals()["current_goal"]
    print(f"Current focus area: {user_goal}")
    
    print("🧠 Sending code to OpenAI for analysis...")
    analysis = analyze_code_with_openai(combined_code, user_goal)
    
    print("📧 Sending weekly email...")
    send_weekly_email(analysis)
    
    # Save progress to user_progress.json
    progress = load_progress()
    progress["weekly_summaries"].append({
        "date": str(datetime.now().date()),
        "goal": user_goal,
        "problems_analyzed": len(code_changes),
        "full_feedback": analysis
    })
    save_progress(progress)
    print("✅ Progress saved to user_progress.json")
    
    print("✅ Weekly analysis complete!")

if __name__ == "__main__":
    run_weekly_analysis()