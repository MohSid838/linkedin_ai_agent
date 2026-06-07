from dotenv import load_dotenv
import os

load_dotenv()

print("OPENAI_KEY_RAW:", os.getenv("OPENAI_API_KEY"))
print("KEY LENGTH:", len(os.getenv("OPENAI_API_KEY") or ""))