import os
import yaml
from pydantic import BaseModel, Field
from typing import Optional, List
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai import Agent, Crew, Task, Process
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

files = {
    "agents": os.path.join(BASE_DIR, "yamlFiles", "lead_qualification_agents.yaml"),
    "tasks": os.path.join(BASE_DIR, "yamlFiles", "lead_qualification_tasks.yaml")
}

configs = {}
for config_type, file_path in files.items():
    with open(file_path, "r") as file:
        configs[config_type] = yaml.safe_load(file)

agents_config = configs["agents"]
tasks_config = configs["tasks"]

#Pydantic Models
class LeadPersonalInfo(BaseModel):
    name: str
    job_title: str
    role_relevance: int = Field(..., ge=0, le=10)
    professional_background: Optional[str] = None

class CompanyInfo(BaseModel):
    company_name: str
    industry: str
    company_size: int
    revenue: Optional[int] = Field(..., description="It must be an integer only")
    market_presence: int = Field(..., ge=0, le=10)

class LeadScore(BaseModel):
    score: int = Field(..., ge=0, le=100)
    scoring_criteria: List[str]
    validation_notes: Optional[str] = None

class LeadScoringResult(BaseModel):
    personal_info: LeadPersonalInfo
    company_info: CompanyInfo
    lead_score: LeadScore

#Agents
lead_data_collector = Agent(
    config=agents_config["lead_data_collector"],
    tools=[ScrapeWebsiteTool(), SerperDevTool()]
)

cultural_fit_analyzer = Agent(
    config=agents_config["cultural_fit_analyzer"]
)

scorer_validator = Agent(
    config=agents_config["scorer_validator"]
)

#Tasks
lead_data_collection = Task(
    config=tasks_config["lead_data_collection"],
    agent=lead_data_collector
)

cultural_fit_analysis = Task(
    config=tasks_config["cultural_fit_analysis"],
    agent=cultural_fit_analyzer
)

scoring_and_validation = Task(
    config=tasks_config["scoring_and_validation"],
    agent=scorer_validator,
    output_pydantic=LeadScoringResult
)

#Crew
lead_crew = Crew(
    agents=[
        lead_data_collector,
        cultural_fit_analyzer,
        scorer_validator
    ],
    tasks=[
        lead_data_collection,
        cultural_fit_analysis,
        scoring_and_validation
    ],
    process=Process.sequential
)

print("Lead Qualification Crew Activated(New)!!!")
