import os
import yaml
from crewai import Crew, Agent, Task, Process, LLM
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv["OPENAI_API_KEY"]
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "agents": os.path.join(BASE_DIR, "yamlFiles", "email_engagement_agents.yaml"),
    "tasks": os.path.join(BASE_DIR, "yamlFiles", "email_engagement_tasks.yaml")
}

configs = {}
for ctype, path in FILES.items():
    with open(path, "r") as f:
        configs[ctype] = yaml.safe_load(f)

agents_config = configs["agents"]
tasks_config = configs["tasks"]

specialist_llm = LLM(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0.4,
    max_tokens=200
)

strategist_llm = LLM(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0.3,
    max_tokens=150
)

# Agents
email_content_specialist = Agent(config=agents_config["email_content_specialist"],
                                 llm=specialist_llm)
engagement_strategist = Agent(config=agents_config["engagement_strategist"],
                              llm=specialist_llm)

# Tasks
email_drafting = Task(
    config=tasks_config["email_drafting"],
    agent=email_content_specialist
)

engagement_optimization = Task(
    config=tasks_config["engagement_optimization"],
    agent=engagement_strategist
)

# Crew
email_crew = Crew(
    agents=[email_content_specialist, engagement_strategist],
    tasks=[email_drafting, engagement_optimization],
    memory=False,
    verbose=False,
    process=Process.sequential
)

print("Email Engagement Crew Activated (Optimized)!")


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# files = {
#     "agents": os.path.join(BASE_DIR, "yamlFiles", "email_engagement_agents.yaml"),
#     "tasks": os.path.join(BASE_DIR, "yamlFiles", "email_engagement_tasks.yaml")
# }

# configs = {}
# for config_type, file_path in files.items() :
#     with open(file_path, "r") as file:
#         configs[config_type] = yaml.safe_load(file)

# agents_config = configs["agents"]
# tasks_config = configs["tasks"]
# agents_config, tasks_config

# email_content_specialist=Agent(
#     config=agents_config["email_content_specialist"]
# )
# engagement_strategist=Agent(
#     config=agents_config['engagement_strategist']
# )

# email_drafting=Task(
#     config=tasks_config["email_drafting"],
#     agent=email_content_specialist
# ) 
# engagement_optimization=Task(
#     config=tasks_config["engagement_optimization"],
#     agent=engagement_strategist
# )

# email_crew = Crew(
#         agents=[email_content_specialist,engagement_strategist],
#         tasks=[email_drafting, engagement_optimization]
#     )