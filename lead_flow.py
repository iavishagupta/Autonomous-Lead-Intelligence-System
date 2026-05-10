from crewai import Flow
from crewai.flow.flow import listen, start

from EmailEngagementCrew import email_crew
from LeadQualificationCrew import lead_crew


class AutonomousLeadIntelligenceSystem(Flow):
    def __init__(self, leads):
        super().__init__()
        self.leads = leads

    @start()
    def fetch_leads(self):
        return self.leads

    @listen(fetch_leads)
    def score_leads(self, leads):
        task_outputs = lead_crew.kickoff_for_each(leads)

        all_lead_results = []
        for task_output in task_outputs:
            lead_result = getattr(task_output, "pydantic", None)
            if lead_result:
                all_lead_results.append(lead_result)

        return all_lead_results

    @listen(score_leads)
    def filter_leads(self, all_lead_results):
        filtered = [
            lead_result
            for lead_result in all_lead_results
            if lead_result.lead_score.score > 70
        ]

        return [lead.dict() for lead in filtered]

    @listen(filter_leads)
    def write_email(self, filtered_dicts):
        email_results = email_crew.kickoff_for_each(filtered_dicts)

        final_emails = [output.raw for output in email_results]

        for lead, email_text in zip(filtered_dicts, final_emails):
            lead["generated_email"] = email_text

        return filtered_dicts


def run_lead_pipeline(leads):
    flow = AutonomousLeadIntelligenceSystem(leads)
    return flow.kickoff()