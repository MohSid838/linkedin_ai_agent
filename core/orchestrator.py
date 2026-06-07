from core.topics import get_topic
from core.llm import generate_content
from tools.telegram_bot import send_post_for_approval
import json
import asyncio
import re


def clean_json(raw_output: str):
    """
    Safely extract JSON from LLM output
    """

    cleaned = raw_output.strip()

    # remove code block wrappers
    cleaned = re.sub(r"^```json", "", cleaned)
    cleaned = re.sub(r"^```", "", cleaned)
    cleaned = re.sub(r"```$", "", cleaned)

    cleaned = cleaned.strip()

    return cleaned


def clean_post_text(post: str, hashtags: list):

    """
    Build final LinkedIn-ready post
    Ensures NO duplication of hashtags
    """

    post = post.strip()

    # remove accidental hashtag sections inside post
    post = re.split(r"🏷️\s*Hashtags:.*", post, flags=re.IGNORECASE)[0].strip()

    # remove trailing hashtags if already embedded
    post = re.sub(r"(#[A-Za-z0-9_]+\s*)+$", "", post).strip()

    # attach hashtags ONLY ONCE
    if hashtags:
        hashtag_str = " ".join([f"#{tag.strip().replace('#','')}" for tag in hashtags])
        post = f"{post}\n\n{hashtag_str}"

    return post.strip()


def run_pipeline():

    topic_data = get_topic()

    print(f"🎯 Role: {topic_data['role']}")
    print(f"📌 Topic: {topic_data['topic']}")

    raw_output = generate_content(topic_data)

    try:
        cleaned_json = clean_json(raw_output)
        data = json.loads(cleaned_json)

    except Exception as e:

        print("❌ JSON Parse Error:", e)

        data = {
            "role": topic_data["role"],
            "topic": topic_data["topic"],
            "post": raw_output,
            "hashtags": [],
            "score": 0
        }

    # ---------------- FINAL POST CLEANING ----------------
    data["post"] = clean_post_text(
        data.get("post", ""),
        data.get("hashtags", [])
    )

    # ---------------- SEND TO TELEGRAM ----------------
    asyncio.run(send_post_for_approval(data))

    return data