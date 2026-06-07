from core.orchestrator import run_pipeline
import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Generate content
result = run_pipeline()

print("\n🎯 Role:")
print(result.get("role"))

print("\n📌 Topic:")
print(result.get("topic"))

print("\n⭐ Score:")
print(result.get("score"))

print("\n📝 Post Preview:")
print(result.get("post", "")[:300] + "...")

print("\n🏷️ Hashtags:")
print(", ".join(result.get("hashtags", [])))

# Save with timestamp
filename = OUTPUT_DIR / f"post_{datetime.now():%Y%m%d_%H%M%S}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved: {filename}")

# Keep only latest 20 posts
files = sorted(
    OUTPUT_DIR.glob("post_*.json"),
    key=lambda f: f.stat().st_mtime,
    reverse=True
)

for old_file in files[20:]:
    old_file.unlink()
    print(f"🗑️ Deleted old file: {old_file}")