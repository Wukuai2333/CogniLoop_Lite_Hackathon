# CogniLoop Lite

CogniLoop Lite is a local-first Streamlit MVP for Cognee onboarding. It helps hackathon participants install Cognee, follow a guided checklist, clarify their task before working with an agent, and learn how to customize the template with their own documents.

## MVP Scope

- Home page
- Static Cognee tutorial
- Cognee docs navigator with hackathon learning routes, notes, bookmarks, and Markdown export
- Timeline checklist with local saved progress, optional notes, and Markdown export
- Local `.env`-only AI Assistant test helper
- Page-level Q&A history for asking about copied text from any page
- Conversation-first workflow placeholder
- Customize Your Own Cognee guide
- BYOK-ready `.env.example`

The static pages do not call Cognee APIs and do not require an API key.
The AI Assistant page stays disabled until a key is present in local `.env` or existing environment variables.

The assistant demo ingests local Markdown files from `/data`, including Cognee onboarding notes and a small business crisis mini dataset. Replace these files with your own project materials to turn the app into a project-specific Cognee template.

The `cognee_*.md` files are short local summaries/placeholders written for this MVP. They are not copies of the official Cognee documentation. Use the Docs Navigator and the official links for authoritative details.

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

## Template Workflow

1. Replace or add Markdown files in `data`.
2. Copy `.env.example` to `.env` and add your own key locally.
3. Open AI Assistant and initialize `/data`.
4. Ask test questions against local Cognee memory.
5. Use page-level Ask Assistant panels to save Q&A history.
6. Export notes and Q&A history for your README, pitch, or demo script.

## No-key Mode

The tutorial, checklist, conversation-first placeholder, and customization guide all work without an API key.

## BYOK Mode

Assistant test features require a local API key through `.env`.
CogniLoop Lite should not collect API keys through the web UI.

Copy `.env.example` to `.env` and set:

```env
LLM_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
```

Never commit `.env` or share your API key.

## API Key Safety Boundary

- The app should not ask users to paste API keys into a Streamlit page.
- No browser-session password input should be used for API keys.
- Assistant features should be local-first, BYOK, and `.env` only.
- Assistant features should be described as a lightweight test helper that users can skip completely.

## Troubleshooting

- `streamlit` not found: activate `.venv`, then run `pip install -r requirements.txt`.
- `python not found`: install Python 3.10+ and add it to PATH.
- API key missing: static pages still work; future assistant features need `.env`.
