import streamlit as st

from components.info_cards import metric_cards, step_card
from components.layout import page_header


def render() -> None:
    page_header("CogniLoop Lite", "A local-first Cognee learning companion for hackathon onboarding and RAG demos.")

    metric_cards(
        [
            ("Project mode", "Local-first"),
            ("AI access", ".env BYOK"),
            ("Cognee flow", "add + cognify + recall"),
        ]
    )

    st.write(
        "CogniLoop Lite now works as a beginner-friendly learning companion and local demo workspace. "
        "Participants can follow official Cognee docs, plan their hackathon workflow, initialize local documents "
        "into Cognee memory, ask questions, and export their notes."
    )

    st.subheader("Why Cognee Matters Here")
    st.markdown(
        "Cognee's strongest value is not simply that it can be installed with `pip`. "
        "Its real advantage is preserving context across sequential work. In a hackathon, participants move through "
        "setup, docs reading, project scoping, implementation, debugging, and demo preparation. Important context often "
        "gets lost between those steps. Cognee helps turn that fragile context into durable, queryable memory."
    )
    st.markdown(
        "The product story can be understood as **Capture -> Model -> Recall**. Cognee can capture materials such as "
        "files, databases, APIs, chat logs, and project notes; model raw data into entities, relationships, rules, and "
        "graph memory; then expose that long-lived memory to agents and runtimes such as Claude Code, LangGraph, MCP "
        "clients, or custom applications."
    )
    st.info(
        "CogniLoop Lite is a small prototype of this idea. Our current dataset is intentionally simple, but the pattern "
        "is the important part: event materials and participant notes can become a shared memory layer that future agents "
        "can query, extend, and reuse."
    )

    st.subheader("Publish Mode")
    publish_cols = st.columns(2)
    with publish_cols[0]:
        step_card(
            "Hosted guide",
            "Deploy the app publicly with `.env.example` only. Visitors can use the tutorial, docs navigator, checklist, "
            "and setup instructions without seeing or entering any API key.",
        )
    with publish_cols[1]:
        step_card(
            "Local full demo",
            "Participants clone the repo, copy `.env.example` to `.env`, add their own key locally, then initialize `data` "
            "and test Cognee-powered assistant flows on their machine.",
        )

    st.subheader("Recommended Workflow")
    steps = [
        ("Learn", "Use Cognee Tutorial and Docs Navigator to understand setup, concepts, and official references."),
        ("Plan", "Use Task Progress Checklist and Conversation-first Workflow to define your target user, scope, blockers, and demo."),
        ("Initialize", "Add Markdown files to `data`, then initialize them from AI Assistant with Cognee `add()` and `cognify()`."),
        ("Ask", "Use AI Assistant or the page-level Ask panel to query local Cognee memory and save Q&A history."),
        ("Export", "Download checklist notes, docs route notes, and Q&A history for your README or demo script."),
        ("Customize", "Replace sample data, update prompts, and keep your API key in local `.env` only."),
    ]

    cols = st.columns(2)
    for index, (title, body) in enumerate(steps):
        with cols[index % 2]:
            step_card(f"{index + 1}. {title}", body)

    st.info(
        "Static learning pages work without an API key. Cognee-powered assistant features are optional local tests "
        "and can be skipped completely."
    )
