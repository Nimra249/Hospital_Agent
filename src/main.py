import os
import sys
from dotenv import load_dotenv

# Force stdout/stderr to use UTF-8 to prevent encoding errors on Windows when printing unicode/emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Add the workspace root to python path to prevent import issues
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env variables before other imports
load_dotenv()

from src.crew import HospitalOPDWorkflowCrew

def print_receipt(result):
    """Prints the final OPD receipt/ticket in a visually appealing format."""
    print("\n" + "="*60)
    print("           HOSPITAL OPD TOKEN SYSTEM CLEARANCE          ")
    print("="*60)
    
    # Try parsing as Pydantic model
    if hasattr(result, 'pydantic') and result.pydantic:
        data = result.pydantic
        
        # Token intake
        print("\n[COUNTER 1: PATIENT INTAKE]")
        print(f"  Token Number  : {data.patient_intake.token_number}")
        print(f"  Patient Name  : {data.patient_intake.patient_name}")
        print(f"  Age / Gender  : {data.patient_intake.patient_age} / {data.patient_intake.patient_gender}")
        print(f"  Complaint     : {data.patient_intake.symptoms_complaint}")
        
        # Verification
        print("\n[COUNTER 2: IDENTITY & HISTORY VERIFICATION]")
        print(f"  CNIC / ID     : {data.verification.cnic_checked}")
        print(f"  ID Verified   : {'Yes' if data.verification.identity_verified else 'No'}")
        print(f"  Past History  : {data.verification.medical_history_summary}")
        if data.verification.critical_alerts:
            print("  ⚠️ CRITICAL ALERTS:")
            for alert in data.verification.critical_alerts:
                print(f"    - {alert}")
        else:
            print("  Alerts        : None reported")
            
        # Slip
        print("\n[COUNTER 3: CLINICAL TRIAGE VISIT SLIP]")
        print(f"  Department    : {data.visit_slip.assigned_department}")
        print(f"  Assigned Doc  : {data.visit_slip.assigned_doctor}")
        print(f"  Urgency Level : {data.visit_slip.urgency_level}")
        print(f"  Triage Notes  : {data.visit_slip.triage_notes}")
        
        # Billing
        print("\n[COUNTER 4: BILLING & CHECKOUT]")
        print(f"  Receipt No    : {data.billing.receipt_number}")
        print(f"  Consultation  : {data.billing.consultation_fee} PKR")
        print(f"  Status        : {data.billing.payment_status}")
        print(f"  Clearance     : {'✅ APPROVED - Proceed to clinic' if data.billing.final_clearance else '❌ BLOCKED'}")
        
    else:
        print("\n[RAW OUTPUT FROM AGENTS]")
        print(str(result))
        
    print("\n" + "="*60 + "\n")

def run_workflow(inputs):
    print("\nInitializing Hospital OPD Multi-Agent System...")
    print(f"Inputs: {inputs}\n")
    
    workflow = HospitalOPDWorkflowCrew()
    result = workflow.kickoff(inputs=inputs)
    
    print_receipt(result)

def main():
    print("="*60)
    print("         Hospital OPD Automated Token System (CrewAI)       ")
    print("="*60)
    print("Choose an option:")
    print("1. Ahmad Khan (Existing patient, Hypertension, Penicillin Allergy)")
    print("2. Ali Raza (Existing child patient, Asthma, Peanut Allergy)")
    print("3. John Doe (New patient, no history, complaining of chest pain)")
    print("4. Input custom patient details interactively")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        inputs = {
            "patient_name": "Ahmad Khan",
            "patient_age": 45,
            "patient_gender": "Male",
            "symptoms_complaint": "Complaining of severe headache and mild chest tightness for past 2 days.",
            "patient_cnic": "42101-1234567-1"
        }
    elif choice == "2":
        inputs = {
            "patient_name": "Ali Raza",
            "patient_age": 8,
            "patient_gender": "Male",
            "symptoms_complaint": "Experiencing wheezing and shortness of breath since this morning after playing outdoors.",
            "patient_cnic": "35202-5555555-3"
        }
    elif choice == "3":
        inputs = {
            "patient_name": "John Doe",
            "patient_age": 35,
            "patient_gender": "Male",
            "symptoms_complaint": "Sharp knee pain and swelling after falling down from the stairs.",
            "patient_cnic": "99999-9999999-9"
        }
    elif choice == "4":
        print("\nEnter Patient Details:")
        name = input("Patient Name: ").strip()
        age = int(input("Patient Age: ").strip() or "30")
        gender = input("Patient Gender (Male/Female/Other): ").strip()
        complaint = input("Symptoms / Health Complaint: ").strip()
        cnic = input("CNIC/ID (format XXXXX-XXXXXXX-X or dummy): ").strip()
        
        inputs = {
            "patient_name": name,
            "patient_age": age,
            "patient_gender": gender,
            "symptoms_complaint": complaint,
            "patient_cnic": cnic
        }
    else:
        print("Invalid choice. Exiting.")
        return
        
    run_workflow(inputs)

if __name__ == "__main__":
    main()
