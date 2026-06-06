import streamlit as st


def metric_cards(items: list[tuple[str, str]]) -> None:
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        with column:
            st.metric(label, value)


def step_card(title: str, body: str) -> None:
    with st.container(border=True):
        st.subheader(title)
        st.write(body)
