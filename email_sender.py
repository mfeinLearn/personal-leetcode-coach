import resend
import os
from datetime import datetime

resend.api_key = os.getenv("RESEND_API_KEY")

def send_weekly_email(analysis_result, user_name="there"):
    subject = f"Your Weekly LeetCode Coaching Report – {datetime.now().strftime('%B %d, %Y')}"
    
    # Fixed: Use regular string + replace instead of f-string with backslash
    html_body = analysis_result.replace('\n', '<br>')
    
    html_content = f"""
    <h2>Hi {user_name},</h2>
    <p>Here's your personalized LeetCode summary for this week:</p>
    
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; font-family: Arial, sans-serif; line-height: 1.6;">
        {html_body}
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