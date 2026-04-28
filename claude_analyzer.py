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