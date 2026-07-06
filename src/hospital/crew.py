import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Tool imports — each tool lives in its own dedicated file
from hospital.tools.patient_history_tool import search_patient_history
from hospital.tools.opd_fee_tool import calculate_opd_fee

# Schema imports — all Pydantic output models live in opd_schemas.py
from hospital.schemas.opd_schemas import (
    TokenCounterOutput,
    VerificationCounterOutput,
    SlipCounterOutput,
    OPDWorkflowOutput
)

@CrewBase
class HospitalOPDWorkflowCrew:
    """Hospital OPD Automated Token System (CrewAI)"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Configure LLM based on environment variables
        llm_model = os.getenv("LLM_MODEL", "gemini/gemini-1.5-flash")
        llm_temp = float(os.getenv("LLM_TEMPERATURE", "0.3"))
        llm_tokens = int(os.getenv("LLM_MAX_TOKENS", "2048"))
        
        self.llm = LLM(
            model=llm_model,
            temperature=llm_temp,
            max_tokens=llm_tokens
        )

    @agent
    def token_registrar(self) -> Agent:
        return Agent(
            config=self.agents_config['token_registrar'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def verification_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['verification_auditor'],
            tools=[search_patient_history],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def triage_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['triage_coordinator'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def billing_officer(self) -> Agent:
        return Agent(
            config=self.agents_config['billing_officer'],
            tools=[calculate_opd_fee],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def issue_token_task(self) -> Task:
        return Task(
            config=self.tasks_config['issue_token_task'],
            output_pydantic=TokenCounterOutput
        )

    @task
    def verify_identity_history_task(self) -> Task:
        return Task(
            config=self.tasks_config['verify_identity_history_task'],
            output_pydantic=VerificationCounterOutput
        )

    @task
    def generate_visit_slip_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_visit_slip_task'],
            output_pydantic=SlipCounterOutput
        )

    @task
    def process_payment_receipt_task(self) -> Task:
        return Task(
            config=self.tasks_config['process_payment_receipt_task'],
            output_pydantic=OPDWorkflowOutput
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Hospital OPD Workflow Crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )

    def kickoff(self, inputs: dict):
        """Executes the sequential workflow."""
        return self.crew().kickoff(inputs=inputs)
