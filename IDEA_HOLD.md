# Idea Hold

## Prompt Generation from Checklist Notes

Later, CogniLoop Lite can use the structured checklist notes to generate stronger prompts for participants.

Possible flow:

1. Users move through the reading-style checklist.
2. Each optional checkbox and note field captures project context.
3. The app combines notes from one stage or all stages.
4. If the user has added their own API key in `.env`, a future assistant can generate:
   - a project summary,
   - a current-stage diagnosis,
   - a next-step recommendation,
   - a better prompt for Codex or another agent.

This should wait until the static MVP is stable because prompt generation requires BYOK API access.

## Dynamic Docs Companion

The official Cognee docs are already strong, so CogniLoop Lite should not clone them wholesale.
Instead, it can add a hackathon layer:

1. Pull or reference the official docs index.
2. Let users choose a route such as Fast Start, Hackathon MVP, Agent Memory Demo, or Custom Docs Q&A.
3. Turn docs pages into learning steps with expected deliverables.
4. Connect route progress to checklist notes and bookmarks.
5. Later, use BYOK mode to generate project-specific prompts from the selected route and notes.
