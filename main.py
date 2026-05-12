from typing import List, Optional
import json

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from lead_flow import run_lead_pipeline
from company_store import save_host_company, get_host_company


app = FastAPI(title="Autonomous Lead Intelligence API")


class HostCompanyInput(BaseModel):
    company_name: str
    industry: str
    mission: str
    cultural_values: List[str]
    strategic_goals: List[str]
    company_size: int
    revenue: Optional[str] = None
    market_presence: int


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/host-company")
async def create_or_update_host_company(file: UploadFile = File(...)):
    try:
        content = await file.read()
        company_data = json.loads(content)

        validated_company = HostCompanyInput(**company_data)
        saved_company = save_host_company(validated_company.dict())

        return {
            "status": "success",
            "message": "Host company profile saved",
            "host_company": saved_company
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
async def run_lead_intelligence(file: UploadFile = File(...)):
    try:
        host_company = get_host_company()

        if not host_company:
            raise HTTPException(
                status_code=400,
                detail="Host company profile is missing. Upload it first using POST /host-company"
            )

        content = await file.read()
        leads_payload = json.loads(content)

        leads = leads_payload.get("leads", [])

        if not leads:
            raise HTTPException(
                status_code=400,
                detail="No leads found in uploaded JSON"
            )

        result = run_lead_pipeline(leads, host_company)

        return {
            "status": "success",
            "analyzed_leads": result,
            "summary": {
                "total_leads": len(result),
                "qualified_leads": sum(
                    1 for lead in result
                    if lead.get("qualification", {}).get("is_qualified") is True
                ),
                "rejected_leads": sum(
                    1 for lead in result
                    if lead.get("qualification", {}).get("is_qualified") is False
                )
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
