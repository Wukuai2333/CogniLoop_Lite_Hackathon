# CogniLoop Lite Mentor Brief

## One-sentence pitch

CogniLoop Lite is an early prototype of an event-ready learning companion that helps hackathon participants understand Cognee, follow a structured onboarding path, save their thinking, and optionally test a local Cognee-powered assistant with their own API key.

## Product Narrative

CogniLoop Lite is not trying to replace the official Cognee documentation. The official docs remain the source of truth for installation, quickstart, concepts, configuration, and deeper technical details.

The product adds a companion layer on top of those docs:

- It translates Cognee documentation into event-specific learning paths.
- It helps beginners understand what to read first and why it matters.
- It turns setup and project planning into checklists, notes, bookmarks, and exportable artifacts.
- It demonstrates how Cognee can store lightweight learning materials and sample project documents, then support a simple recall-based assistant.

This is intentionally an early prototype. The current Cognee dataset is small and simple: a few local Markdown files summarizing Cognee onboarding concepts plus a small sample business crisis dataset. The point is not to show a large production RAG system yet. The point is to show a workflow template: put event materials into `data`, initialize them into Cognee memory, ask questions, and export the learning trail.

## Three Main Goals

### 1. Help Cognee gain visibility during the hackathon

CogniLoop Lite makes Cognee easier to encounter in a fast event setting. Instead of asking beginners to read documentation from scratch, it gives them a guided route:

- What is Cognee?
- How do I install it?
- What docs should I read for my use case?
- How can I test remember, cognify, and recall?
- How might Cognee fit into my hackathon project?

This helps Cognee feel immediately usable rather than abstract.

### 2. Help participants get started quickly

Hackathon participants often do not have time to fully understand a new technical tool before building. CogniLoop Lite supports fast onboarding by giving them:

- A beginner-friendly tutorial.
- A docs navigator organized by goal.
- A timeline checklist with progress tracking.
- Notes under each step.
- Exportable project notes.
- A local AI Assistant test page for users who want to try Cognee with their own key.

The product reduces the "where do I start?" problem.

### 3. Introduce CogniLoop as an education product direction

CogniLoop Lite also tests a broader product idea: learning companions for short, intense onboarding contexts outside the classroom.

Potential contexts include:

- Hackathons.
- Workshops.
- Industry onboarding.
- Internal training.
- Tool adoption sessions.
- Bootcamps.
- Sponsor technology onboarding.

The hypothesis is that people need more than static documentation. They need a guided path, a place to write notes, a way to ask contextual questions, and a way to turn learning into usable project output.

## Additional Narrative Angles

### Docs-to-workflow transformation

CogniLoop Lite shows how documentation can become an interactive workflow. Instead of a passive reading experience, users move through stages, take notes, bookmark important points, and export a project brief.

### Local-first safety

The hosted demo can run without collecting API keys. Full AI features are designed for local use through `.env`, where users bring their own key. This keeps the public demo safer and makes it easier to present as a template.

### Beginner-friendly RAG template

The project gives participants a minimal pattern they can copy:

1. Put Markdown files in `data`.
2. Initialize them into Cognee.
3. Ask questions against the local dataset.
4. Replace the sample data with their own hackathon materials.

### Learning trace as output

The product captures a participant's progress, notes, bookmarks, and Q&A history. This can later become a project brief, implementation prompt, demo script, or README material.

## How to Present Each Page

### Home

Purpose: Give the audience the product framing.

What to say:

"This is the overview page. It explains that CogniLoop Lite has two modes: a hosted guide that works without an API key, and a local full template where participants clone the project and add their own `.env` to test Cognee."

What to show:

- Project mode cards.
- Publish Mode section.
- Recommended Workflow.
- Use This As a Template section.

Key message:

CogniLoop Lite is both a learning companion and a reusable starter template.

### Cognee Tutorial

Purpose: Help beginners install and verify Cognee.

What to say:

"This page turns basic setup into a readable beginner path. It is not replacing Cognee docs; it gives participants a first route through setup and verification."

What to show:

- Python version guidance.
- Virtual environment setup.
- Cognee installation.
- Import test.
- Troubleshooting notes.

Key message:

This page lowers setup friction for first-time Cognee users.

### Docs Navigator

Purpose: Convert official Cognee docs into hackathon-specific routes.

What to say:

"The official Cognee docs are detailed, but participants need to know which docs matter for their current goal. Docs Navigator recommends routes like Fast Start, Hackathon MVP, Agent Memory Demo, or Custom Docs Q&A."

What to show:

- Different learning routes.
- Official docs links.
- Why each route matters.
- Notes and bookmarks.
- Export feature.

Key message:

This is the companion layer: docs become an event workflow.

### Checklist

Purpose: Track participant progress through the event.

What to say:

"This is a reading-style timeline checklist. Each step has a clear task, optional notes, progress tracking, bookmarks, and export. The goal is to help participants keep their thinking organized during a short event."

What to show:

- Stage navigation.
- Mark as done.
- Notes under each substep.
- Auto-save status.
- Bookmarks grouped by stage.
- Export full progress.

Key message:

Participants leave with structured notes instead of scattered memory.

### AI Assistant

Purpose: Demonstrate the local Cognee-powered assistant flow.

What to say:

"This page is optional. In the hosted demo, we do not ask users to enter an API key. For the full test, participants clone the repo, create their own `.env`, initialize the local `data` folder, and ask questions against Cognee memory."

What to show:

- Safety notice.
- `.env.example` guidance.
- Dataset preview.
- Initialize `/data` documents.
- Ask: "What is Cognee and how does it help hackathon participants?"
- Result card and raw result expander.

Important caveat:

"The dataset is intentionally small right now. We are using Cognee to store simple local materials, not claiming this is a large production knowledge base yet."

Key message:

This is a minimal Cognee template: add documents, cognify them, recall answers.

### Conversation-first Workflow

Purpose: Teach participants how to ask better questions before building.

What to say:

"This page helps participants clarify goal, audience, constraints, and output before asking an agent or starting code. It supports better project scoping."

What to show:

- Goal clarification.
- Context gathering.
- Constraints and assumptions.
- Output definition.

Key message:

Better prompts and better projects start with better context.

### Customize Your Own Cognee

Purpose: Help participants adapt the template.

What to say:

"This page tells participants how to turn the demo into their own project. Replace the sample Markdown files, update the questions, keep secrets in `.env`, and use Cognee as a local memory layer."

What to show:

- How to replace `data`.
- How to create `.env` from `.env.example`.
- How to reset/reinitialize local storage.
- How to use the exported notes.

Key message:

The project is meant to be copied and modified.

### Ask Assistant About This Page

Purpose: Save contextual Q&A across pages.

What to say:

"Every page has a page-level assistant panel. Users can paste selected text, ask a question, and save the Q&A history locally. This is a first step toward contextual learning support."

What to show:

- Paste selected/copied text.
- Ask question.
- Saved Q&A history.
- Download Q&A.

Key message:

Learning support should be attached to the workflow, not hidden in a separate chatbot.

## Suggested Demo Flow

1. Start on Home and explain the two modes: hosted guide and local full template.
2. Open Docs Navigator and show how official Cognee docs become hackathon routes.
3. Open Checklist and show progress, notes, bookmarks, and export.
4. Open AI Assistant and explain the safety boundary: no API key input in the public page; full test uses local `.env`.
5. If running locally with a key, initialize `/data` and ask the default question.
6. Open Customize page and explain how participants can replace the sample dataset.
7. End by saying this is a prototype of a broader education/onboarding product for short, high-intensity learning events.

## What This Prototype Proves

- Cognee can be introduced through a guided workflow instead of only static documentation.
- Participants can use a local-first template to test document memory and recall.
- Hackathon learning can produce reusable artifacts: notes, bookmarks, Q&A, and project briefs.
- CogniLoop can become a product category for event-based onboarding and rapid skill acquisition.

## What This Prototype Does Not Claim Yet

- It is not a complete production RAG platform.
- It does not yet use a large or complex knowledge base.
- It does not collect user API keys through the hosted website.
- It does not replace official Cognee documentation.
- It is an early experiment in making documentation more actionable, interactive, and beginner-friendly.

