from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_code_with_openai(code_snippets, user_goal, previous_mistakes=""):
    prompt = f"""You are an expert LeetCode coach and mentor.

Use relevant emojis throughout your response to make it more engaging and visually appealing.

User's current focus area: {user_goal}

Here is the code the user pushed this week:

{code_snippets}

Previous mistakes the user has made (if any):
{previous_mistakes}

IMPORTANT: If the user has made similar mistakes in previous weeks, specifically call them out and explain how to finally break the pattern. Reference past mistakes directly when relevant.

Please analyze the code and respond in this exact format:

## Weekly Summary
[Short encouraging overview]

## Strengths
- Bullet points of what they did well

## Areas for Improvement
- Specific, actionable feedback

## Mistake Patterns Detected
- List any recurring mistakes (especially ones from previous weeks)

## Recommended Problems for Next Week
1. Problem Name - Difficulty - Link
2. ...

## Overall Feedback
[Motivating closing message]

Keep the tone supportive but honest. Be specific and reference actual code patterns when possible."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",                    
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.7
    )
    
    return response.choices[0].message.content