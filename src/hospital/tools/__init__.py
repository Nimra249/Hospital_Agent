from crewai.tools import tool
from typing import Dict, Any

# Mock Database for Patient Histories
MOCK_PATIENT_DB: Dict[str, Dict[str, Any]] = {
    "42101-1234567-1": {
        "name": "Ahmad Khan",
        "cnic": "42101-1234567-1",
        "history": "Diagnosed with Hypertension in 2021. Managed on daily Amlodipine 5mg. Last visited Cardiology department 6 months ago.",
        "allergies": ["Penicillin", "Sulfa drugs"],
        "critical_conditions": ["Chronic Hypertension"]
    },
    "42201-9876543-2": {
        "name": "Sana Ahmed",
        "cnic": "42201-9876543-2",
        "history": "Underwent laparoscopic Appendectomy in April 2023 at this hospital. Post-op recovery was uneventful.",
        "allergies": [],
        "critical_conditions": []
    },
    "35202-5555555-3": {
        "name": "Ali Raza",
        "cnic": "35202-5555555-3",
        "history": "Diagnosed with Childhood Asthma. Uses Albuterol inhaler as needed. Visited Pediatrics ER twice last year during winter.",
        "allergies": ["Peanuts", "Dust Mites"],
        "critical_conditions": ["Asthma"]
    }
}

@tool("Search Patient Medical History Database")
def search_patient_history(cnic: str) -> str:
    """
    Searches the hospital database for past medical records, surgeries, chronic illnesses, and allergies.
    Args:
        cnic (str): The patient's 15-character CNIC number (format: XXXXX-XXXXXXX-X).
    Returns:
        str: String description of the patient's medical history details or a message stating no history exists.
    """
    # Clean the CNIC format slightly (just in case)
    cnic_clean = cnic.strip()
    
    if cnic_clean in MOCK_PATIENT_DB:
        record = MOCK_PATIENT_DB[cnic_clean]
        allergies_str = ", ".join(record["allergies"]) if record["allergies"] else "None reported"
        conditions_str = ", ".join(record["critical_conditions"]) if record["critical_conditions"] else "None reported"
        
        return (
            f"--- PATIENT RECORD FOUND ---\n"
            f"Verified Name: {record['name']}\n"
            f"CNIC: {record['cnic']}\n"
            f"Medical History: {record['history']}\n"
            f"Allergies: {allergies_str}\n"
            f"Chronic Conditions: {conditions_str}\n"
        )
    else:
        return (
            f"--- NO PATIENT RECORD FOUND ---\n"
            f"CNIC: {cnic_clean}\n"
            f"Note: This patient has no past history registered in our hospital system. Treat as a new patient."
        )

@tool("Calculate OPD Consultation Fee")
def calculate_opd_fee(department: str, urgency: str) -> float:
    """
    Calculates the fee for the consultation based on the assigned clinical department and level of urgency.
    Args:
        department (str): The clinical department (e.g. Cardiology, Pediatrics, General Medicine, Orthopedics).
        urgency (str): The urgency tier of the visit (Routine, Urgent, Emergency).
    Returns:
        float: Calculated fee amount in local currency (PKR).
    """
    # Base fee lookup by department
    base_fees = {
        "cardiology": 2000.0,
        "pediatrics": 1500.0,
        "general medicine": 1000.0,
        "orthopedics": 1800.0,
        "dermatology": 1500.0,
        "ophthalmology": 1400.0,
        "gynecology": 1800.0,
        "ent": 1300.0
    }
    
    dept_lower = department.lower().strip()
    base_fee = base_fees.get(dept_lower, 1200.0) # default fee if department not listed
    
    # Premium added based on urgency level
    urgency_lower = urgency.lower().strip()
    if urgency_lower == "emergency":
        premium = 1000.0
    elif urgency_lower == "urgent":
        premium = 500.0
    else:
        premium = 0.0
        
    return base_fee + premium
