from pydantic import BaseModel, Field
from typing import List, Optional

class TokenCounterOutput(BaseModel):
    """Output structure for the initial Token Counter Counter."""
    patient_name: str = Field(..., description="The name of the patient.")
    patient_age: int = Field(..., description="The age of the patient.")
    patient_gender: str = Field(..., description="The gender of the patient.")
    symptoms_complaint: str = Field(..., description="The patient's main medical complaints or symptoms.")
    token_number: str = Field(..., description="A unique sequentially generated token ID like T-1001.")

class VerificationCounterOutput(BaseModel):
    """Output structure for the Identity & History Verification Counter."""
    identity_verified: bool = Field(..., description="Boolean indicating whether patient ID/CNIC was verified.")
    cnic_checked: str = Field(..., description="The patient's verified CNIC or national ID number.")
    medical_history_found: bool = Field(..., description="Whether a past history was found for this patient.")
    medical_history_summary: str = Field(..., description="Summary of patient's past medical records, surgeries, or visits.")
    critical_alerts: List[str] = Field(default=[], description="List of allergies, drug reactions, or critical warning flags.")

class SlipCounterOutput(BaseModel):
    """Output structure for the Doctor Slip Counter."""
    assigned_department: str = Field(..., description="The clinical department recommended for the patient (e.g. Cardiology, Pediatrics).")
    assigned_doctor: str = Field(..., description="The recommended doctor name based on symptoms and availability.")
    triage_notes: str = Field(..., description="Clinical triage assessment notes summarising symptoms and routing logic.")
    urgency_level: str = Field(..., description="Urgency categorization: 'Routine', 'Urgent', or 'Emergency'.")

class PaymentCounterOutput(BaseModel):
    """Output structure for the Billing & Receipt Counter."""
    consultation_fee: float = Field(..., description="The fee calculated for the specific doctor and department.")
    payment_status: str = Field(..., description="The status of payment, usually 'Paid' upon successful clearance.")
    receipt_number: str = Field(..., description="A generated invoice or receipt serial number like REC-5001.")
    final_clearance: bool = Field(..., description="Whether the patient is cleared to proceed to the doctor.")

class OPDWorkflowOutput(BaseModel):
    """The final structured summary containing details from all 4 OPD counters."""
    patient_intake: TokenCounterOutput = Field(..., description="Details from Token Counter.")
    verification: VerificationCounterOutput = Field(..., description="Details from Verification Counter.")
    visit_slip: SlipCounterOutput = Field(..., description="Details from Slip Counter.")
    billing: PaymentCounterOutput = Field(..., description="Details from Payment Counter.")
