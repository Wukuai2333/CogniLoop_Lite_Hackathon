DOC_ROUTES = [
    {
        "name": "Fast Start",
        "best_for": "Participants who need a clean first run as quickly as possible.",
        "outcome": "A working local environment and a first remember / recall smoke test.",
        "steps": [
            {
                "title": "Installation",
                "url": "https://docs.cognee.ai/getting-started/installation",
                "why": "Set up Python, a virtual environment, Cognee, and provider configuration.",
                "deliverable": "Confirm Python 3.10-3.14 and install Cognee in a clean environment.",
            },
            {
                "title": "Quickstart",
                "url": "https://docs.cognee.ai/getting-started/quickstart",
                "why": "Run the smallest useful Cognee example and see memory retrieval work.",
                "deliverable": "Run a remember / recall script and capture the output.",
            },
        ],
    },
    {
        "name": "Hackathon MVP",
        "best_for": "Teams building a small demo around custom docs or sponsor materials.",
        "outcome": "A scoped demo plan with docs, ingestion assumptions, and test questions.",
        "steps": [
            {
                "title": "Installation",
                "url": "https://docs.cognee.ai/getting-started/installation",
                "why": "Make the local setup reproducible before adding hackathon-specific files.",
                "deliverable": "Document the install path and API key mode.",
            },
            {
                "title": "Quickstart",
                "url": "https://docs.cognee.ai/getting-started/quickstart",
                "why": "Understand the minimum Cognee loop before customizing it.",
                "deliverable": "Write one project-specific remember / recall use case.",
            },
            {
                "title": "Loaders",
                "url": "https://docs.cognee.ai/core-concepts/further-concepts/loaders",
                "why": "Check which document formats fit the materials your team has.",
                "deliverable": "List the files you will add and any optional extras needed.",
            },
            {
                "title": "Setup Configuration",
                "url": "https://docs.cognee.ai/setup-configuration/overview",
                "why": "Choose provider and embedding settings without hard-coding secrets.",
                "deliverable": "Create a local .env plan for BYOK mode.",
            },
        ],
    },
    {
        "name": "Agent Memory Demo",
        "best_for": "Teams showing how an assistant can remember project or user context.",
        "outcome": "A demo story that explains memory, retrieval, and agent usefulness.",
        "steps": [
            {
                "title": "Quickstart",
                "url": "https://docs.cognee.ai/getting-started/quickstart",
                "why": "Start from the core memory operations before adding agent behavior.",
                "deliverable": "Explain remember and recall in your own project language.",
            },
            {
                "title": "Core Concepts",
                "url": "https://docs.cognee.ai/core-concepts/overview",
                "why": "Understand the architecture well enough to explain it to judges.",
                "deliverable": "Write a plain-English description of how Cognee supports your app.",
            },
            {
                "title": "Agent Memory Quickstart",
                "url": "https://docs.cognee.ai/guides/agent-memory-quickstart",
                "why": "Connect Cognee memory to an agent-style workflow.",
                "deliverable": "Draft the agent memory scenario you want to demonstrate.",
            },
        ],
    },
    {
        "name": "Custom Docs Q&A",
        "best_for": "Teams building a question-answering helper over docs, notes, or PDFs.",
        "outcome": "A grounded Q&A plan with test questions and source materials.",
        "steps": [
            {
                "title": "Loaders",
                "url": "https://docs.cognee.ai/core-concepts/further-concepts/loaders",
                "why": "Match your source files to Cognee-supported loaders.",
                "deliverable": "Choose a small set of documents for the first demo.",
            },
            {
                "title": "Cognify",
                "url": "https://docs.cognee.ai/core-concepts/main-operations/cognify",
                "why": "Understand how raw data becomes structured memory.",
                "deliverable": "Describe what needs to happen after documents are added.",
            },
            {
                "title": "Setup Configuration",
                "url": "https://docs.cognee.ai/setup-configuration/overview",
                "why": "Prepare model and embedding configuration for BYOK mode.",
                "deliverable": "Write the configuration variables your demo will need.",
            },
        ],
    },
]
