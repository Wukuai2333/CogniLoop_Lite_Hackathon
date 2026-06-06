import streamlit as st

from components.info_cards import metric_cards, step_card
from components.layout import page_header


def render() -> None:
    page_header("CogniLoop Lite", "A local-first Cognee starter kit for hackathon onboarding and RAG demos.")

    metric_cards(
        [
            ("Project mode", "Local-first"),
            ("AI access", ".env BYOK"),
            ("Cognee flow", "add + cognify + recall"),
        ]
    )

    st.write(
        "CogniLoop Lite now works as both a beginner-friendly learning companion and a reusable template. "
        "Participants can follow official Cognee docs, plan their hackathon workflow, initialize local documents "
        "into Cognee memory, ask questions, and export their notes."
    )

    st.subheader("Publish Mode")
    publish_cols = st.columns(2)
    with publish_cols[0]:
        step_card(
            "Hosted guide",
            "Deploy the app publicly with `.env.example` only. Visitors can use the tutorial, docs navigator, checklist, "
            "and template instructions without seeing or entering any API key.",
        )
    with publish_cols[1]:
        step_card(
            "Local full template",
            "Participants clone the repo, copy `.env.example` to `.env`, add their own key locally, then initialize `data` "
            "and test Cognee-powered assistant flows on their machine.",
        )

    st.subheader("Recommended Workflow")
    steps = [
        ("Learn", "Use Cognee Tutorial and Docs Navigator to understand setup, concepts, and official references."),
        ("Plan", "Use Checklist and Conversation-first Workflow to define your target user, scope, blockers, and demo."),
        ("Initialize", "Add Markdown files to `data`, then initialize them from AI Assistant with Cognee `add()` and `cognify()`."),
        ("Ask", "Use AI Assistant or the page-level Ask panel to query local Cognee memory and save Q&A history."),
        ("Export", "Download checklist notes, docs route notes, and Q&A history for your README or demo script."),
        ("Customize", "Replace sample data, update prompts, and keep your API key in local `.env` only."),
    ]

    cols = st.columns(2)
    for index, (title, body) in enumerate(steps):
        with cols[index % 2]:
            step_card(f"{index + 1}. {title}", body)

    st.subheader("Use This As a Template")
    st.markdown(
        "1. Copy the project folder.\n"
        "2. Put your own Markdown notes or sponsor docs in `data`.\n"
        "3. Create local `.env` from `.env.example`.\n"
        "4. Open AI Assistant and initialize `/data`.\n"
        "5. Ask test questions and save useful Q&A.\n"
        "6. Replace the sample business crisis dataset when your own materials are ready."
    )

    st.info(
        "Static learning pages work without an API key. Cognee-powered assistant features are optional local tests "
        "and can be skipped completely."
    )
