CHECKLIST_STAGES = [
    {
        "id": "setup",
        "title": "Stage 1: Setup Cognee",
        "goal": "Finish basic installation and confirm Cognee works locally.",
        "items": [
            {
                "text": "I checked my Python version.",
                "detail": "Cognee currently requires Python 3.10 through 3.14. If your Python is older, install a supported version before creating the virtual environment.",
                "prompt": "Record the Python version you checked and whether it is compatible.",
            },
            {
                "text": "I created a project folder.",
                "detail": "Use a clean local folder so tutorial files, data files, and future ingestion scripts stay together.",
                "prompt": "Write the folder path or any naming decision you made.",
            },
            {
                "text": "I created and activated a virtual environment.",
                "detail": "A virtual environment keeps Cognee dependencies separate from the rest of your machine.",
                "prompt": "Note the command you used and whether activation worked.",
            },
            {
                "text": "I installed Cognee.",
                "detail": "Install Cognee inside the active virtual environment with pip or uv.",
                "prompt": "Record the install command and any warnings or errors.",
            },
            {
                "text": "I ran the import test successfully.",
                "detail": "The import test confirms that Python can find Cognee in the active environment.",
                "prompt": "Paste the test result or describe what happened.",
            },
            {
                "text": "I understand where to put my API key if I want to use AI features.",
                "detail": "Static pages do not need an API key. Future AI features should read your own key from a local .env file.",
                "prompt": "Write whether you plan to use no-key mode or BYOK mode.",
            },
        ],
    },
    {
        "id": "task",
        "title": "Stage 2: Understand the Hackathon Task",
        "goal": "Clarify what the team is trying to build before coding.",
        "items": [
            {
                "text": "I understand the main hackathon goal.",
                "detail": "Restate the challenge in your own words before deciding what to build.",
                "prompt": "Write the main goal in one or two sentences.",
            },
            {
                "text": "I understand the required tools or sponsor technologies.",
                "detail": "List the technologies you must use and the technologies that are optional.",
                "prompt": "Name the required tools and what each one contributes.",
            },
            {
                "text": "I know what problem my team wants to solve.",
                "detail": "A clear problem helps keep the project from drifting into too many features.",
                "prompt": "Describe the user pain or workflow problem.",
            },
            {
                "text": "I know who the target user is.",
                "detail": "Pick a specific user role so design decisions have a stable audience.",
                "prompt": "Write the target user and their context.",
            },
            {
                "text": "I know what output or demo we need to present.",
                "detail": "Define the final demo artifact early, such as a working app, guided workflow, or short scenario.",
                "prompt": "Describe what judges or mentors should see in the demo.",
            },
        ],
    },
    {
        "id": "scope",
        "title": "Stage 3: Define the Project Scope",
        "goal": "Narrow the project to a realistic MVP.",
        "items": [
            {
                "text": "I wrote a one-sentence project goal.",
                "detail": "Example: Our project helps first-time Cognee users understand sponsor documentation and get step-by-step onboarding support.",
                "prompt": "Write your one-sentence project goal.",
            },
            {
                "text": "I identified the target user.",
                "detail": "The target user should be specific enough that you can imagine their first session.",
                "prompt": "Write who the project is for and why they need it.",
            },
            {
                "text": "I listed the materials or documents my project needs.",
                "detail": "Cognee becomes useful when it has relevant documents, notes, docs, or examples to organize.",
                "prompt": "List the documents, links, notes, or data you need.",
            },
            {
                "text": "I chose one simple use case for the first demo.",
                "detail": "Choose one workflow that can be shown quickly and reliably.",
                "prompt": "Describe the first demo use case.",
            },
            {
                "text": "I know what the minimum working version should do.",
                "detail": "The MVP should be small enough to finish and clear enough to explain.",
                "prompt": "Define the minimum working behavior.",
            },
        ],
    },
    {
        "id": "customize",
        "title": "Stage 4: Customize Cognee",
        "goal": "Replace the sample materials with project-specific materials.",
        "items": [
            {
                "text": "I added my own documents to the /data folder.",
                "detail": "Keep sample and project materials easy to inspect. Avoid secrets or private keys in data files.",
                "prompt": "List the files you added or plan to add.",
            },
            {
                "text": "I reviewed the sample ingestion script.",
                "detail": "Future ingestion should be understandable before it runs over your project materials.",
                "prompt": "Note what the ingestion script should read and store.",
            },
            {
                "text": "I ran the ingestion script.",
                "detail": "This is reserved for a later Cognee-powered build. For now, describe the expected command.",
                "prompt": "Write the command or intended ingestion flow.",
            },
            {
                "text": "I asked at least three test questions.",
                "detail": "Good test questions should cover setup, project context, and an edge case.",
                "prompt": "Draft three questions you want the assistant to answer later.",
            },
            {
                "text": "I checked whether the answers are grounded in the uploaded materials.",
                "detail": "Grounded answers should cite or clearly reflect the documents you provided.",
                "prompt": "Write how you would judge whether an answer is grounded.",
            },
        ],
    },
    {
        "id": "alignment",
        "title": "Stage 5: Conversation-first Alignment",
        "goal": "Align the task with the agent before asking it to work.",
        "items": [
            {
                "text": "I explained what I am trying to build.",
                "detail": "The agent needs the product goal before it can choose useful next actions.",
                "prompt": "Write the build goal as if briefing a teammate.",
            },
            {
                "text": "I described my current progress.",
                "detail": "Progress context prevents the agent from repeating work you already finished.",
                "prompt": "Summarize what is already done.",
            },
            {
                "text": "I described my current blocker.",
                "detail": "A blocker can be technical, conceptual, scope-related, or demo-related.",
                "prompt": "Name the blocker and why it matters.",
            },
            {
                "text": "I told the agent what kind of help I want.",
                "detail": "Be explicit: planning, debugging, implementation, writing, explanation, or review.",
                "prompt": "Write the type of help you want next.",
            },
            {
                "text": "I reviewed the agent summary before moving forward.",
                "detail": "Confirming the summary keeps the human and agent aligned before work mode.",
                "prompt": "Write what the agent summary must include.",
            },
        ],
    },
    {
        "id": "demo",
        "title": "Stage 6: Prepare Final Demo",
        "goal": "Prepare a clear, short explanation of the project.",
        "items": [
            {
                "text": "I can explain what my project does in one sentence.",
                "detail": "A one-sentence explanation is the anchor for the whole demo.",
                "prompt": "Write the one-sentence explanation.",
            },
            {
                "text": "I can explain how my project uses Cognee.",
                "detail": "Make the Cognee role concrete: memory, retrieval, onboarding, document Q&A, or workflow support.",
                "prompt": "Describe exactly where Cognee fits.",
            },
            {
                "text": "I can show the main user workflow.",
                "detail": "A demo workflow should be short, visible, and easy to follow.",
                "prompt": "Outline the demo steps.",
            },
            {
                "text": "I can explain what documents or materials were used.",
                "detail": "Judges should know what knowledge the assistant is using.",
                "prompt": "List the materials and why they matter.",
            },
            {
                "text": "I can explain the value of the project.",
                "detail": "Value should connect back to the target user and the problem.",
                "prompt": "Write the value proposition.",
            },
            {
                "text": "I prepared a short demo script.",
                "detail": "A script keeps the final presentation calm and reproducible.",
                "prompt": "Draft the demo script or talking points.",
            },
        ],
    },
]
