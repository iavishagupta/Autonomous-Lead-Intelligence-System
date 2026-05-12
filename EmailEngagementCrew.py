import os
import yaml

from dotenv import load_dotenv
from crewai import Crew, Agent, Task, Process, LLM


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "agents": os.path.join(BASE_DIR, "yamlFiles", "email_engagement_agents.yaml"),
    "tasks": os.path.join(BASE_DIR, "yamlFiles", "email_engagement_tasks.yaml"),
}

configs = {}

for config_type, file_path in FILES.items():
    with open(file_path, "r", encoding="utf-8") as file:
        configs[config_type] = yaml.safe_load(file)

agents_config = configs["agents"]
tasks_config = configs["tasks"]


specialist_llm = LLM(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0.4,
    max_tokens=200,
)

strategist_llm = LLM(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0.3,
    max_tokens=150,
)


email_content_specialist = Agent(
    config=agents_config["email_content_specialist"],
    llm=specialist_llm,
)

engagement_strategist = Agent(
    config=agents_config["engagement_strategist"],
    llm=strategist_llm,
)


email_drafting = Task(
    config=tasks_config["email_drafting"],
    agent=email_content_specialist,
)

engagement_optimization = Task(
    config=tasks_config["engagement_optimization"],
    agent=engagement_strategist,
)


email_crew = Crew(
    agents=[
        email_content_specialist,
        engagement_strategist,
    ],
    tasks=[
        email_drafting,
        engagement_optimization,
    ],
    memory=False,
    verbose=False,
    process=Process.sequential,
)

print("Email Engagement Crew Activated!")
