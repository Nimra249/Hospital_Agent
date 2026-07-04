from crewai import Task
from src.agents import (
    token_counter_agent,
    verification_counter_agent,
    slip_counter_agent,
    payment_counter_agent
)
from src.schemas import (
    TokenCounterOutput,
    VerificationCounterOutput,
    SlipCounterOutput,
    PaymentCounterOutput,
    OPDWorkflowOutput
)

# 1. Token Counter Task
issue_token_task = Task(
    description=(
        "Gather the basic details of the incoming patient from the inputs (patient_name, patient_age, "
        "patient_gender, and symptoms_complaint). Assign a unique sequential OPD Token Number (e.g., T-1001 "
        "if no previous, or next integer equivalent) to this patient. Format the profile as requested."
    ),
    expected_output="A structured JSON object representing the patient intake profile with a Token ID.",
    agent=token_counter_agent,
    output_pydantic=TokenCounterOutput
)

# 2. Verification Counter Task
verify_identity_history_task = Task(
    description=(
        "Verify the patient's identity using their CNIC provided in inputs ({patient_cnic}). "
        "Use the 'Search Patient Medical History Database' tool with the exact CNIC. "
        "If a past record is found, pull their medical history and compile a summary of their past visits, "
        "and list any critical allergy or chronic health alerts. If no record is found, treat them as a new patient "
        "with empty history and no alerts. Set identity_verified to True if the query executes successfully."
    ),
    expected_output="A structured JSON object with identity verification status, medical history summary, and alerts.",
    agent=verification_counter_agent,
    output_pydantic=VerificationCounterOutput
)

# 3. Slip Counter Task
generate_visit_slip_task = Task(
    description=(
        "Analyze the patient's symptoms/complaints from the token desk, along with their medical history and critical "
        "alerts from the verification desk. Determine the best clinical department (e.g. Cardiology, Pediatrics, "
        "General Medicine, Orthopedics, Gynecology, Dermatology, ENT, etc.) and recommend a doctor. "
        "Assign an urgency level: 'Routine', 'Urgent', or 'Emergency' (e.g., if there is a severe condition/alert "
        "or severe symptoms, mark Urgent/Emergency). Write a short clinical routing note explaining your decision."
    ),
    expected_output="A clinical visit slip recommending department, doctor, urgency, and clinical routing notes.",
    agent=slip_counter_agent,
    output_pydantic=SlipCounterOutput
)

# 4. Payment Counter Task
process_payment_receipt_task = Task(
    description=(
        "Read the outputs of the preceding counters: Token Counter, Verification Counter, and Slip Counter. "
        "Calculate the consultation fee using the 'Calculate OPD Consultation Fee' tool based on department and urgency. "
        "Simulate payment collection (mark payment_status as 'Paid' and generate a receipt number e.g. REC-5001). "
        "Compile and return a unified 'OPDWorkflowOutput' object containing all the details gathered from the entire OPD process: "
        "1. patient_intake (from Token Counter)"
        "2. verification (from Verification Counter)"
        "3. visit_slip (from Slip Counter)"
        "4. billing (calculated payment receipt details with final_clearance=True)"
    ),
    expected_output="A final unified OPDWorkflowOutput containing full patient intake, verification status, clinic slip, and billing receipt.",
    agent=payment_counter_agent,
    output_pydantic=OPDWorkflowOutput
)
