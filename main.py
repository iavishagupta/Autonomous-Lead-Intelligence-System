from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from lead_flow import run_lead_pipeline


app = FastAPI(title="Autonomous Lead Intelligence API")


class LeadInput(BaseModel):
    name: str
    job_title: str
    company: str
    email: str
    use_case: str


class LeadRequest(BaseModel):
    leads: List[LeadInput]


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/run-lead-intelligence")
def run_lead_intelligence(request: LeadRequest):
    try:
        leads = [lead.dict() for lead in request.leads]
        result = run_lead_pipeline(leads)

        return {
            "status": "success",
            "qualified_leads": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))