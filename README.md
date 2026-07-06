# Hospital OPD Automated Token System (CrewAI)

This project implements a multi-agent system using **CrewAI** to automate the 4 sequential counters of a Hospital Out Patient Department (OPD). The project follows CrewAI's professional project structure, utilising a `config/` folder for agent and task definitions, a `pyproject.toml` configuration, custom tools, and structured outputs.

## Project Structure

```text
Hospital/
├── pyproject.toml                # Poetry configuration & project dependency definitions
├── README.md                     # Documentation with detailed commands
├── .env                          # Configuration file for API keys (e.g., Gemini, OpenAI)
├── .env.example                  # Template configuration file for environment variables
└── src/
    └── hospital/
        ├── __init__.py           # Hospital package initializer
        ├── main.py               # Main CLI entry point (interactive runner)
        ├── crew.py               # Wires agents and tasks using @CrewBase & decorators
        ├── tools.py              # Custom tools & mock database definitions
        ├── schemas.py            # Pydantic schemas for counter output structures
        └── config/
            ├── agents.yaml       # YAML configuration defining agent roles, goals, and backstories
            └── tasks.yaml        # YAML configuration defining task descriptions and expected outputs
```

## System Workflow & Counter Agents

The system simulates a sequential flow through the following 4 counters:
1. **Counter 1: OPD Token Registrar** (`token_registrar` agent)
   - Receives patient basic info (name, age, gender, symptoms) and issues a sequential token ID (e.g. `T-1001`).
2. **Counter 2: Identity & Medical History Auditor** (`verification_auditor` agent)
   - Verifies identity using CNIC/ID and retrieves past medical history, noting allergies and warnings.
3. **Counter 3: OPD Clinical Triage Coordinator** (`triage_coordinator` agent)
   - Analyzes symptoms and history to determine the right clinical department, doctor, and urgency tier.
4. **Counter 4: OPD Billing & Clearance Officer** (`billing_officer` agent)
   - Calculates doctor fees based on department/urgency, simulates payment, and prints the cleared OPD receipt.

---

## Detailed Command Guide

Below is the list of all command operations available for configuring, running, and managing this project.

### 1. Installation & Environment Setup

#### Option A: Direct Installation (Virtual Environment)
To set up a local virtual environment and install all package requirements:
```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows (cmd):
venv\Scripts\activate.bat
# On Windows (Powershell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt
```

#### Option B: Poetry-Based Setup (Recommended)
This project contains a standard `pyproject.toml` file. You can install all project dependencies and manage the environment using Poetry:
```bash
# Install dependencies and setup environment
poetry install
```

---

### 2. Environment Variables Configuration

Before running the workflow, copy the example configuration file to `.env` and enter your API keys.
```bash
# On Windows (Command Prompt)
copy .env.example .env

# On Windows (PowerShell)
Copy-Item .env.example .env

# On macOS/Linux
cp .env.example .env
```
Open the generated `.env` file and set your API keys:
```env
# If using Gemini (default/recommended):
GEMINI_API_KEY=your_gemini_api_key_here

# If using OpenAI:
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 3. Running the OPD Automated System

You can run the interactive CLI tool where you can choose a predefined patient profile or insert details custom-tailored:

#### Running via Direct Python
```bash
python src/hospital/main.py
```

#### Running via Poetry CLI Scripts
This package is preconfigured with CLI command mappings. You can run the application directly from Poetry:
```bash
# Launch the main interactive OPD workflow
poetry run hospital

# Alternative mapped command alias
poetry run run-crew
```

#### Running via CrewAI CLI
If you have the `crewai` CLI tool installed globally:
```bash
crewai run
```

---

### 4. Code Quality & Maintenance Commands

#### Dependency Locking (Poetry)
If you modify package definitions in `pyproject.toml`, run the following commands:
```bash
# Update and lock dependencies
poetry lock

# Update packages to their latest allowed versions
poetry update
```

#### Code Formatting
To format the python code according to standard guidelines:
```bash
# Install black if not already present
pip install black

# Run formatting checks across the source tree
black src/
```

#### Checking for Configuration Errors
To verify that poetry configuration files do not contain syntax errors:
```bash
poetry check
```
