from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from lead_flow import run_lead_pipeline
from company_store import save_host_company, get_host_company


app = FastAPI(title="Autonomous Lead Intelligence API")


class LeadInput(BaseModel):
    name: str
    job_title: str
    company: str
    email: str
    use_case: str


class HostCompanyInput(BaseModel):
    company_name: str
    industry: str
    mission: str
    cultural_values: List[str]
    strategic_goals: List[str]
    company_size: int
    revenue: Optional[str] = None
    market_presence: int


class LeadRequest(BaseModel):
    leads: List[LeadInput]


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/host-company")
def create_or_update_host_company(company: HostCompanyInput):
    saved_company = save_host_company(company.dict())

    return {
        "status": "success",
        "message": "Host company profile saved",
        "host_company": saved_company
    }


@app.get("/host-company")
def read_host_company():
    company = get_host_company()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="No host company profile saved yet"
        )

    return {
        "status": "success",
        "host_company": company
    }


@app.post("/run-lead-intelligence")
def run_lead_intelligence(request: LeadRequest):
    try:
        host_company = get_host_company()

        if not host_company:
            raise HTTPException(
                status_code=400,
                detail="Host company profile is missing. Save it first using POST /host-company"
            )

        leads = [lead.dict() for lead in request.leads]
        result = run_lead_pipeline(leads, host_company)

        return {
            "status": "success",
            "qualified_leads": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
