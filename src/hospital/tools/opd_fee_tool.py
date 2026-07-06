from crewai.tools import tool

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
