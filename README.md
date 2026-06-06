# CogniLoop Lite

CogniLoop Lite is a local-first Streamlit MVP for Cognee onboarding. It helps hackathon participants install Cognee, follow a guided checklist, clarify their task before working with an agent, and learn how to customize the template with their own documents.

## MVP Scope

- Home page
- Static Cognee tutorial
- Cognee docs navigator with hackathon learning routes, notes, bookmarks, and Markdown export
- Timeline checklist with local saved progress, optional notes, and Markdown export
- Conversation-first workflow placeholder
- Customize Your Own Cognee guide
- BYOK-ready `.env.example`

The static MVP does not call Cognee APIs and does not require an API key.

## Setup

```powershell
cd "CogniLoop Lite"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Cognee currently requires Python 3.10 through 3.14. Check your version before creating the environment:

```powershell
python --version
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

## Run

```powershell
streamlit run app.py
```

## No-key Mode

The tutorial, checklist, conversation-first placeholder, and customization guide all work without an API key.

## BYOK Mode

Future assistant features will require your own local API key. Copy `.env.example` to `.env` and set:

```env
LLM_API_KEY=your_api_key_here
```

Never commit `.env` or share your API key.

## Troubleshooting

- `streamlit` not found: activate `.venv`, then run `pip install -r requirements.txt`.
- `python not found`: install Python 3.10+ and add it to PATH.
- API key missing: static pages still work; future assistant features need `.env`.
