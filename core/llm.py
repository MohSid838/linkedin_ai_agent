import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=api_key)


# -----------------------------
# 1. Generate new post
# -----------------------------
def generate_content(topic_data):

    role = topic_data["role"]
    topic = topic_data["topic"]

    prompt = f"""
You are a senior LinkedIn content strategist.

Target Audience:
{role}

Topic:
{topic}

Create a LinkedIn post.

Return ONLY valid JSON:

{{
  "role": "{role}",
  "topic": "{topic}",
  "post": "",
  "hashtags": [],
  "score": 0
}}

Rules:
- 150–250 words
- Professional tone
- Problem → Solution → Value format
- 5 hashtags
- Score 1–10 based on engagement
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


# -----------------------------
# 2. Smart regeneration (improve post)
# -----------------------------
def improve_content(topic_data, previous_post, feedback):

    role = topic_data["role"]
    topic = topic_data["topic"]

    prompt = f"""
You are a senior LinkedIn content strategist.

Improve this LinkedIn post.

Target Audience:
{role}

Topic:
{topic}

Previous Post:
{previous_post}

Feedback:
{feedback}

Return ONLY valid JSON:

{{
  "role": "{role}",
  "topic": "{topic}",
  "post": "",
  "hashtags": [],
  "score": 0
}}

Rules:
- Make it clearer and more engaging
- Improve hook (first 2 lines)
- Add better structure
- Increase practical value
- 150–250 words
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content