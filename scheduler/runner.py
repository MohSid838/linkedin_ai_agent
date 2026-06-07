import schedule
import time
import json
from pathlib import Path

from core.orchestrator import run_pipeline


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def job():
    try:
        print("\n🚀 Starting LinkedIn content generation...")

        result = run_pipeline()

        print("\n📌 Topic:")
        print(result.get("best_topic"))

        print("\n📝 Post:")
        print(result.get("post"))

        print("\n🏷️ Hashtags:")
        print(result.get("hashtags", []))

        print("\n🖼️ Image:")
        print(result.get("image_path"))

        output = {
            "topic": result.get("best_topic"),
            "post": result.get("post"),
            "hashtags": result.get("hashtags", []),
            "image_prompt": result.get("image_prompt"),
            "image_path": result.get("image_path")
        }

        posts_file = OUTPUT_DIR / "posts.jsonl"

        with open(posts_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(output, ensure_ascii=False) + "\n")

        print(f"\n✅ Saved to {posts_file}")

    except Exception as e:
        print(f"\n❌ Job failed: {e}")


# Run every day at 10:00 AM
schedule.every().day.at("10:00").do(job)


print("🚀 LinkedIn Scheduler Started")
print("⏰ Scheduled: Every day at 10:00")

# Uncomment the next line if you want to test immediately
job()

while True:
    schedule.run_pending()
    time.sleep(60)