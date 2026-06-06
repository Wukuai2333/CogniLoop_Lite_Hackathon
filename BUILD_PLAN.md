# CogniLoop Lite — Build Plan

## Current Goal

Build a clean local Streamlit MVP for CogniLoop Lite.

The MVP should include:

1. Home page
2. Static Cognee tutorial
3. Timeline / checklist guide
4. Conversation-first workflow placeholder
5. Customize your own Cognee page
6. README
7. `.env.example`
8. `.gitignore`

The app should be local-first and BYOK.

Do not build real Cognee API integration yet unless the static MVP is complete.

---

## Build Rules

### 1. Use Git Properly

Initialize Git first.

Create small commits after each milestone.

Suggested commits:

```text
init: create project structure
docs: add project spec and build plan
chore: add gitignore and env example
feat: add Streamlit app shell
feat: add Cognee tutorial page
feat: add checklist page
feat: add conversation-first placeholder
feat: add customize page
docs: add README setup instructions
```

Do not commit:

```text
.env
.venv/
API keys
logs/
local database files
cache files
```

---

## 2. First File Structure

Create this structure:

```text
cogniloop-lite/
│
├── app.py
├── README.md
├── PROJECT_SPEC.md
├── BUILD_PLAN.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── pages/
│   ├── home.py
│   ├── tutorial.py
│   ├── checklist.py
│   ├── conversation_first.py
│   └── customize.py
│
├── components/
│   ├── layout.py
│   ├── checklist_components.py
│   └── info_cards.py
│
├── content/
│   ├── tutorial_content.py
│   ├── checklist_content.py
│   └── prompt_examples.py
│
├── data/
│   ├── cognee_intro.md
│   ├── cognee_installation.md
│   ├── cognee_quickstart.md
│   └── sponsor_docs_placeholder.md
│
├── tutorials/
│   ├── install_cognee.md
│   ├── api_key_setup.md
│   ├── troubleshooting.md
│   └── customize_your_own_cognee.md
│
└── utils/
    ├── env.py
    └── progress.py
```

If this is too much for the first pass, still keep:

```text
app.py
pages/
components/
content/
utils/
README.md
.env.example
.gitignore
```

---

## 3. Implementation Order

### Step 1: Repo Setup

Create:

* `.gitignore`
* `.env.example`
* `requirements.txt`
* `README.md`
* `PROJECT_SPEC.md`
* `BUILD_PLAN.md`

Then commit:

```text
init: create project docs and setup files
```

---

### Step 2: Streamlit App Shell

Create:

* `app.py`
* sidebar navigation
* page routing
* basic layout

Pages:

* Home
* Cognee Tutorial
* Checklist
* Conversation-first Workflow
* Customize Your Own Cognee

Then commit:

```text
feat: add Streamlit app shell
```

---

### Step 3: Static Cognee Tutorial

Create the tutorial page with:

* What is Cognee?
* Requirements
* Windows installation
* macOS/Linux installation
* Test installation
* API key setup
* Troubleshooting table

Then commit:

```text
feat: add static Cognee tutorial page
```

---

### Step 4: Checklist Page

Create checklist stages:

1. Setup Cognee
2. Understand the Hackathon Task
3. Define the Project Scope
4. Customize Cognee
5. Conversation-first Alignment
6. Prepare Final Demo

Use `st.session_state` for progress.

Then commit:

```text
feat: add timeline checklist page
```

---

### Step 5: Conversation-first Placeholder

Create a form with:

* What are you trying to build?
* Who is your target user?
* What have you already done?
* What is blocking you?
* What kind of help do you want?
* What output do you expect?

For now, generate a static summary without API calls.

Then commit:

```text
feat: add conversation-first workflow placeholder
```

---

### Step 6: Customize Page

Create instructions:

* Replace files in `/data`
* Add your own API key
* Run future `ingest.py`
* Run app
* Modify assistant role

Then commit:

```text
feat: add Cognee customization guide
```

---

### Step 7: README

Update README with:

* overview
* setup
* run command
* no-key mode
* BYOK mode
* safety notes
* troubleshooting

Then commit:

```text
docs: update README with setup and usage
```

---

## 4. MVP Acceptance Checklist

The MVP is complete when:

* [ ] App runs with `streamlit run app.py`
* [ ] Static pages work without API key
* [ ] No API key is hard-coded
* [ ] `.env` is ignored by Git
* [ ] Checklist state works locally
* [ ] README explains how to run the project
* [ ] README explains BYOK
* [ ] Project structure is modular
* [ ] Codex did not put everything into one large file
* [ ] Git history has meaningful commits

---

## 5. Future Extensions

After MVP is stable, add:

1. real Cognee installation smoke test
2. `ingest.py`
3. Cognee-powered document Q&A
4. API key detection
5. local progress export
6. prompt reflection with model output
7. optional mentor dashboard

Do not add these before the static MVP works.
