from core.llm import generate_content

topics = [
    "AI agents in automation",
    "Cloud cost optimization in 2026",
    "Future of data engineering"
]

result = generate_content(topics)

print("\n🔥 RAW OUTPUT:\n")
print(result)