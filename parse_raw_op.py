import re
from typing import List
from LeadQualificationCrew import LeadScoringResult, LeadPersonalInfo, CompanyInfo, LeadScore

def parse_crew_raw(raw_text: str) -> LeadScoringResult:
    # --- Personal Info ---
    name_match = re.search(r"\*\*Lead Name:\*\* (.+)", raw_text)
    job_match = re.search(r"\*\*Job Title:\*\* (.+)", raw_text)
    role_match = re.search(r"Role Relevance.*Score: (\d+)", raw_text)
    background_match = re.search(r"Professional Background: (.+)", raw_text, re.DOTALL)
    
    personal_info = LeadPersonalInfo(
        name=name_match.group(1).strip() if name_match else "",
        job_title=job_match.group(1).strip() if job_match else "",
        role_relevance=int(role_match.group(1)) if role_match else 0,
        professional_background=background_match.group(1).strip() if background_match else None
    )
    
    # --- Company Info ---
    company_name_match = re.search(r"\*\*Company Name:\*\* (.+)", raw_text)
    industry_match = re.search(r"Industry: (.+)", raw_text)
    company_size_match = re.search(r"Company Size.*Score: (\d+)", raw_text)
    revenue_match = re.search(r"Revenue: \$(\d+\.?\d*)", raw_text)
    market_match = re.search(r"Market Presence.*Score: (\d+)", raw_text)
    
    company_info = CompanyInfo(
        company_name=company_name_match.group(1).strip() if company_name_match else "",
        industry=industry_match.group(1).strip() if industry_match else "",
        company_size=int(company_size_match.group(1)) if company_size_match else 0,
        revenue=float(revenue_match.group(1)) if revenue_match else None,
        market_presence=int(market_match.group(1)) if market_match else 0
    )
    
    # --- Lead Score ---
    score_match = re.search(r"\*\*Final Lead Score:\*\* (\d+)", raw_text)
    criteria_matches = re.findall(r"\d+\.\s\*\*(.+?) \(0-10\):\*\*", raw_text)
    validation_notes_match = re.search(r"\*\*Validation Notes:\*\*\n(.+?)(\n\n|\Z)", raw_text, re.DOTALL)
    
    lead_score = LeadScore(
        score=int(score_match.group(1)) if score_match else 0,
        scoring_criteria=[c.strip() for c in criteria_matches] if criteria_matches else [],
        validation_notes=validation_notes_match.group(1).strip() if validation_notes_match else None
    )
    
    return LeadScoringResult(
        personal_info=personal_info,
        company_info=company_info,
        lead_score=lead_score
    )

print("Parser Initialized!!!")