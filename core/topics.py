import random

TOPICS = {

    "Data Engineer": [
        "BigQuery Partitioning",
        "BigQuery Clustering",
        "Apache Airflow Best Practices",
        "ETL vs ELT",
        "Data Quality Frameworks",
        "Data Lake vs Data Warehouse",
        "dbt Transformations",
        "Real-Time Data Pipelines",
        "Apache Spark Optimization",
        "Data Governance"
    ],

    "AI Engineer": [
        "AI Agents",
        "Multi-Agent Systems",
        "RAG Architecture",
        "Prompt Engineering",
        "Vector Databases",
        "LangChain Workflows",
        "MCP Architecture",
        "LLM Evaluation",
        "AI Automation",
        "Agent Memory Design"
    ],

    "Data Scientist": [
        "Feature Engineering",
        "Model Monitoring",
        "A/B Testing",
        "Time Series Forecasting",
        "Machine Learning Pipelines",
        "Model Explainability",
        "MLOps",
        "Data Drift Detection"
    ],

    "BI Developer": [
        "Power BI Performance",
        "DAX Optimization",
        "Dashboard Design",
        "Executive KPIs",
        "Data Storytelling",
        "Power Query Techniques",
        "Semantic Models"
    ]
}


def get_topic():
    role = random.choice(list(TOPICS.keys()))
    topic = random.choice(TOPICS[role])

    return {
        "role": role,
        "topic": topic
    }