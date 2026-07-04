from crewai import Crew, Process
from src.agents import (
    token_counter_agent,
    verification_counter_agent,
    slip_counter_agent,
    payment_counter_agent
)
from src.tasks import (
    issue_token_task,
    verify_identity_history_task,
    generate_visit_slip_task,
    process_payment_receipt_task
)

class HospitalOPDWorkflowCrew:
    """
    Hospital OPD Token Workflow Crew.
    Wires up the 4 sequential counter agents and tasks:
    1. Token Counter
    2. Verification Counter
    3. Slip Counter
    4. Payment Counter
    """
    def __init__(self):
        self.crew = Crew(
            agents=[
                token_counter_agent,
                verification_counter_agent,
                slip_counter_agent,
                payment_counter_agent
            ],
            tasks=[
                issue_token_task,
                verify_identity_history_task,
                generate_visit_slip_task,
                process_payment_receipt_task
            ],
            process=Process.sequential,
            verbose=True
        )

    def kickoff(self, inputs: dict):
        """
        Executes the sequential workflow.
        Required inputs keys:
            - patient_name (str)
            - patient_age (int)
            - patient_gender (str)
            - symptoms_complaint (str)
            - patient_cnic (str)
        """
        return self.crew.kickoff(inputs=inputs)
