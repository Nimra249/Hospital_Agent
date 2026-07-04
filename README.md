# Hospital OPD Token System

This project is a multi-agent system designed using **CrewAI** to automate the 4 sequential counters of a Hospital Out Patient Department (OPD).

## System Counters & Agents

1. **Token Counter Agent**: Intake of basic patient info, issues a sequential token number.
2. **Verification Counter Agent**: Verifies patient identity (CNIC/ID) and retrieves/checks history (allergies, chronic conditions).
3. **Slip Counter Agent**: Determines department/doctor based on symptoms and generates the visit slip.
4. **Payment Counter Agent**: Computes consultation fees, processes payment, and issues a final printed receipt/ticket.

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` (already done for this environment) and configure your API keys.

3. **Run the Workflow**:
   ```bash
   python src/main.py
   ```

## Project Structure

```
Hospital/
├── requirements.txt
├── .env
├── src/
    ├── main.py        # CLI Entrypoint to run the OPD workflow
    ├── crew.py        # Wires agents and tasks into a sequential Crew
    ├── agents.py      # CrewAI Agent definitions
    ├── tasks.py       # CrewAI Task definitions
    ├── tools.py       # Simulated database/billing tools
    └── schemas.py     # Pydantic schemas for structured outputs
```
