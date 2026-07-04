import os
from crewai import Agent, LLM
from src.tools import search_patient_history, calculate_opd_fee

# Configure LLM based on environment variables
# CrewAI LLM will automatically pick up GEMINI_API_KEY or OPENAI_API_KEY from environment.
llm_model = os.getenv("LLM_MODEL", "gemini/gemini-1.5-flash")
llm_temp = float(os.getenv("LLM_TEMPERATURE", "0.3"))
llm_tokens = int(os.getenv("LLM_MAX_TOKENS", "2048"))

llm = LLM(
    model=llm_model,
    temperature=llm_temp,
    max_tokens=llm_tokens
)

# 1. Token Counter Agent
token_counter_agent = Agent(
    role="OPD Token Registrar",
    goal="Gather patient's basic information (name, age, gender, and symptoms) and issue a sequential OPD Token ID (e.g. T-100X).",
    backstory=(
        "You are the front desk receptionist at the OPD Token Counter. Your primary task is to greet patients, "
        "record their basic registration details (name, age, gender, main health complaint), and issue a structured "
        "intake token. You work efficiently under pressure to keep queue times short."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# 2. Verification Counter Agent
verification_counter_agent = Agent(
    role="Identity & Medical History Auditor",
    goal="Verify patient identity using CNIC and fetch past medical history, noting allergies and warnings.",
    backstory=(
        "You manage Counter 2 (Verification). Your responsibility is to verify the patient's CNIC "
        "and look up their previous clinical files in the database. You must search for patient history "
        "and flag any drug allergies, critical health warnings, or chronic conditions to ensure patient safety."
    ),
    tools=[search_patient_history],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# 3. Slip Counter Agent
slip_counter_agent = Agent(
    role="OPD Clinical Triage Coordinator",
    goal="Analyze complaints and history to determine the right clinical department, doctor, and urgency tier.",
    backstory=(
        "You operate Counter 3 (Slip Counter). You act as a triage specialist who reviews symptoms "
        "and medical history. Based on clinical assessment, you decide whether they should go to Cardiology, "
        "Pediatrics, General Medicine, Orthopedics, etc., assign the best doctor, and establish if the case "
        "is Routine, Urgent, or a direct ER Emergency."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# 4. Payment Counter Agent
payment_counter_agent = Agent(
    role="OPD Billing & Clearance Officer",
    goal="Calculate fees, process simulated payment, and print the final cleared OPD consultation receipt.",
    backstory=(
        "You are the cashier at Counter 4 (Payment Counter). Your job is to compute the exact consultation fee "
        "for the assigned doctor and clinic department (using the fee tool). You collect the payment virtually "
        "and issue a finalized receipt token that summarizes the entire process and grants clearance."
    ),
    tools=[calculate_opd_fee],
    llm=llm,
    verbose=True,
    allow_delegation=False
)
