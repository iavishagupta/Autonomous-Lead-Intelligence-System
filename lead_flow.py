from crewai import Flow
from crewai.flow.flow import listen, start

from EmailEngagementCrew import email_crew
from LeadQualificationCrew import lead_crew


QUALIFICATION_THRESHOLD = 60


class AutonomousLeadIntelligenceSystem(Flow):
    def __init__(self, leads, host_company):
        super().__init__()
        self.leads = leads
        self.host_company = host_company

    @start()
    def fetch_leads(self):
        return [
            {
                "lead_data": lead,
                "host_company": self.host_company
            }
            for lead in self.leads
        ]

    @listen(fetch_leads)
    def score_leads(self, crew_inputs):
        task_outputs = lead_crew.kickoff_for_each(crew_inputs)

        analyzed_leads = []

        for task_output in task_outputs:
            lead_result = getattr(task_output, "pydantic", None)

            if lead_result:
                lead_dict = lead_result.dict()
                score = lead_dict["lead_score"]["score"]

                lead_dict["qualification"] = {
                    "is_qualified": score >= QUALIFICATION_THRESHOLD,
                    "threshold": QUALIFICATION_THRESHOLD,
                    "status": "Qualified" if score >= QUALIFICATION_THRESHOLD else "Rejected",
                    "reason": lead_dict["lead_score"].get(
                        "validation_notes",
                        "No validation notes provided."
                    )
                }

                lead_dict["generated_email"] = None
                analyzed_leads.append(lead_dict)

        return analyzed_leads

    @listen(score_leads)
    def write_email_for_qualified(self, analyzed_leads):
        qualified_leads = [
            lead for lead in analyzed_leads
            if lead["qualification"]["is_qualified"]
        ]

        if not qualified_leads:
            return analyzed_leads

        email_inputs = [
            {
                "lead_data": lead,
                "host_company": self.host_company
            }
            for lead in qualified_leads
        ]

        email_results = email_crew.kickoff_for_each(email_inputs)

        final_emails = [output.raw for output in email_results]

        email_index = 0

        for lead in analyzed_leads:
            if lead["qualification"]["is_qualified"]:
                lead["generated_email"] = final_emails[email_index]
                email_index += 1

        return analyzed_leads


def run_lead_pipeline(leads, host_company):
    flow = AutonomousLeadIntelligenceSystem(
        leads=leads,
        host_company=host_company
    )
    return flow.kickoff()
