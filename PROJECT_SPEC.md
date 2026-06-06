# CogniLoop Lite — Project Specification

## 1. Product Name

**CogniLoop Lite**

## 2. Product Positioning

CogniLoop Lite is a **Cognee-based onboarding and learning companion** for hackathon participants.

It helps participants:

1. Understand what Cognee is.
2. Install and configure Cognee.
3. Follow a guided tutorial/checklist to start using Cognee.
4. Use a conversation-first workflow to clarify their task before asking the agent to work.
5. Customize the demo with their own documents and their own API key.

This project is not intended to be a full learning analytics platform. It is a lightweight, practical onboarding tool and reference implementation.

---

## 3. Core Design Principle

### Local-first + BYOK

CogniLoop Lite should be designed as a **local-first BYOK tool**.

BYOK means **Bring Your Own Key**.

The static tutorial and checklist should work without an API key.

The Cognee-powered assistant features should require participants to use their own API key through a local `.env` file.

The project should not expose, store, or share any user API key.

---

## 4. Target Users

Primary users:

* Hackathon participants who need to quickly learn how to install and use Cognee.
* Participants who want to customize a Cognee-based workflow for their own project.

Secondary users:

* Mentors or organizers who want to guide participants through onboarding.
* Developers who want a small reference demo for Cognee onboarding.

---

## 5. Product Structure

CogniLoop Lite includes five modules:

1. Static Cognee Tutorial
2. Timeline / Checklist Guide
3. Conversation-first Workflow
4. BYOK Cognee-powered Assistant
5. Customize Your Own Cognee Demo

For the first build, prioritize Modules 1 and 2.

---

# Module 1: Static Cognee Tutorial

## Goal

Help participants understand and install Cognee from scratch.

This module should be available without an API key.

## Content Sections

### 1. What is Cognee?

Explain Cognee briefly:

* Cognee helps transform documents and data into AI memory.
* It can ingest materials, organize knowledge, and support retrieval-based question answering.
* Participants can use it as a backend for their own AI applications.

### 2. Installation Requirements

Show the requirements:

* Python 3.10+
* `uv` or `pip`
* terminal access
* optional OpenAI API key for interactive AI features

### 3. Windows Installation

Include commands:

```powershell
mkdir your-project-name
cd your-project-name

pip install uv
uv venv
.venv\Scripts\Activate.ps1

uv pip install cognee
```

If PowerShell blocks virtual environment activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. macOS / Linux Installation

Include commands:

```bash
mkdir your-project-name
cd your-project-name

pip install uv
uv venv
source .venv/bin/activate

uv pip install cognee
```

### 5. Test Installation

Include command:

```bash
python -c "import cognee; print('Cognee installed successfully')"
```

Expected output:

```text
Cognee installed successfully
```

### 6. API Key Setup

Explain:

To use the AI companion and Cognee-powered features, participants should create a `.env` file based on `.env.example`.

Example:

```env
LLM_API_KEY=your_api_key_here
```

Important note:

* Do not commit `.env` to GitHub.
* Do not share your API key.
* Static tutorial and checklist do not require an API key.
* Interactive assistant features require the participant’s own API key.

### 7. Minimal Cognee Demo

Include a minimal example script later, but for the first UI build, it is enough to reserve a section for:

* remember
* recall
* ask a question
* see retrieved answer

### 8. Troubleshooting

Include a troubleshooting table:

| Problem                  | Likely Cause                                      | Suggested Fix                                                              |
| ------------------------ | ------------------------------------------------- | -------------------------------------------------------------------------- |
| `python not found`       | Python is not installed or not in PATH            | Install Python 3.10+ and check “Add to PATH”                               |
| `uv not recognized`      | uv is not installed or terminal was not restarted | Run `pip install uv` and reopen terminal                                   |
| venv activation blocked  | PowerShell execution policy issue                 | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `No module named cognee` | Cognee installed outside the active environment   | Activate `.venv`, then reinstall Cognee                                    |
| API key missing          | `.env` not created or wrong variable name         | Create `.env` and set `LLM_API_KEY`                                        |
| quota / billing error    | API key has no available quota                    | Check billing or use no-key mode                                           |

---

# Module 2: Timeline / Checklist Guide

## Goal

Provide a guided progress structure for participants.

This module should help participants know:

* where they are,
* what they have completed,
* what they should do next,
* when they may need help.

This module should also work without an API key.

## Design

The checklist should be organized by stages.

Each stage should include:

1. Stage title
2. Short goal
3. Checklist items
4. Optional tutorial link or explanation
5. Optional “Ask Companion about this step” button placeholder

For the first build, the “Ask Companion” button can be a placeholder. Later it can connect to Module 3 or Module 4.

---

## Stage 1: Setup Cognee

Goal:

Participants should finish basic installation and confirm Cognee works locally.

Checklist:

* [ ] I checked my Python version.
* [ ] I created a project folder.
* [ ] I created and activated a virtual environment.
* [ ] I installed Cognee.
* [ ] I ran the import test successfully.
* [ ] I understand where to put my API key if I want to use AI features.

---

## Stage 2: Understand the Hackathon Task

Goal:

Participants should clarify what they are trying to build before coding.

Checklist:

* [ ] I understand the main hackathon goal.
* [ ] I understand the required tools or sponsor technologies.
* [ ] I know what problem my team wants to solve.
* [ ] I know who the target user is.
* [ ] I know what output or demo we need to present.

---

## Stage 3: Define the Project Scope

Goal:

Participants should narrow the project to a realistic MVP.

Checklist:

* [ ] I wrote a one-sentence project goal.
* [ ] I identified the target user.
* [ ] I listed the materials or documents my project needs.
* [ ] I chose one simple use case for the first demo.
* [ ] I know what the “minimum working version” should do.

Example project goal:

```text
Our project helps first-time Cognee users understand sponsor documentation and get step-by-step onboarding support.
```

---

## Stage 4: Customize Cognee

Goal:

Participants should replace the sample materials with their own materials.

Checklist:

* [ ] I added my own documents to the `/data` folder.
* [ ] I reviewed the sample ingestion script.
* [ ] I ran the ingestion script.
* [ ] I asked at least three test questions.
* [ ] I checked whether the answers are grounded in the uploaded materials.

---

## Stage 5: Conversation-first Alignment

Goal:

Participants should align the task with the agent before asking it to work.

Checklist:

* [ ] I explained what I am trying to build.
* [ ] I described my current progress.
* [ ] I described my current blocker.
* [ ] I told the agent what kind of help I want.
* [ ] I reviewed the agent’s summary before moving forward.

Core idea:

Before the agent starts working, it should first clarify:

* Goal
* Context
* Constraints
* Current progress
* Expected output

Only after this alignment should the agent enter work mode.

---

## Stage 6: Prepare Final Demo

Goal:

Participants should prepare a clear, short explanation of their project.

Checklist:

* [ ] I can explain what my project does in one sentence.
* [ ] I can explain how my project uses Cognee.
* [ ] I can show the main user workflow.
* [ ] I can explain what documents or materials were used.
* [ ] I can explain the value of the project.
* [ ] I prepared a short demo script.

---

# Module 3: Conversation-first Workflow

## Goal

Help users clarify their task before the AI agent starts working.

This is one of the main learning-support ideas of CogniLoop Lite.

## Workflow

1. User enters their task.
2. Agent asks clarification questions.
3. User provides goal, context, constraints, current progress, and expected output.
4. Agent summarizes its understanding.
5. User confirms or edits the summary.
6. Agent enters work mode.

## Required Input Fields

The interface should include:

* What are you trying to build?
* Who is your target user?
* What materials or tools are required?
* What have you already done?
* What is blocking you right now?
* What kind of help do you want?
* What output do you expect?

## Expected Output

The agent should produce:

* Shared understanding
* Current stage
* Main blocker
* Suggested next step
* Suggested better prompt

---

# Module 4: BYOK Cognee-powered Assistant

## Goal

Allow participants to ask questions based on Cognee documentation, sponsor tool documentation, and their own materials.

## API Key Policy

This module requires the participant’s own API key.

The app should make this clear:

```text
To use the AI companion and Cognee-powered features, please add your own API key to the local .env file.
This project does not store or share your API key.
```

## Features

Potential features:

* Ask about Cognee installation
* Ask about sponsor documentation
* Ask for help on current checklist step
* Ask for prompt improvement
* Ask for next-step guidance
* Ask questions based on user-provided documents

---

# Module 5: Customize Your Own Cognee

## Goal

Show participants how to adapt the demo to their own projects.

## Instructions

Participants should be able to:

1. Replace files in `/data`.
2. Add their own API key to `.env`.
3. Run the ingestion script.
4. Run the app.
5. Modify the assistant role or prompt.
6. Ask questions based on their own materials.

## Example Customizations

| Use Case            | Materials to Add                               |
| ------------------- | ---------------------------------------------- |
| Study assistant     | class notes, lecture slides, textbook excerpts |
| Sponsor tool helper | sponsor documentation, API docs, tutorials     |
| Legal assistant     | legal documents, policy files                  |
| Startup advisor     | business resources, pitch templates            |
| Research assistant  | papers, notes, datasets                        |

---

# First Build Scope

For the first build, focus only on:

1. Home page
2. Module 1: Static Cognee Tutorial
3. Module 2: Timeline / Checklist Guide
4. Placeholder for Module 3: Conversation-first Workflow
5. `.env.example`
6. README

Do not build complex database integration yet.

Do not build mentor dashboard yet.

Do not require API key for static tutorial and checklist.

Do not expose or hard-code API keys.

---

# Suggested Tech Stack

Use:

* Python
* Streamlit
* Local files
* Optional JSON file for checklist progress
* `.env.example` for API key setup

Avoid for MVP:

* user authentication
* hosted public deployment
* external database
* complex dashboard
* shared API key

---

# Success Criteria

The first MVP is successful if a participant can:

1. Open the app locally.
2. Read the Cognee installation tutorial.
3. Follow the checklist.
4. Understand when they need their own API key.
5. Understand how to customize the demo with their own materials.
6. Understand the conversation-first workflow concept.

The demo is successful if it clearly shows that CogniLoop Lite is both:

1. a practical Cognee onboarding tool, and
2. a prototype of a learning companion that helps users clarify tasks and move step by step.
