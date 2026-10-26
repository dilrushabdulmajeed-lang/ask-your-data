"""Chat UI for the ask-your-data agent. Run: streamlit run app/streamlit_app.py"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent.agent import _client, ask, build_schema_doc  # noqa: E402

st.set_page_config(page_title="Ask your data", page_icon="📊", layout="centered")
st.title("📊 Ask your data")
st.caption("Plain-English questions about Google Ads, the e-commerce store and the checkout A/B test. "
           "Answers come from read-only SQL on ClickHouse, with the query shown.")


@st.cache_resource
def schema_doc() -> str:
    return build_schema_doc()


EXAMPLES = [
    "Which campaign had the lowest ROAS in September 2026?",
    "What's the repeat purchase rate for White Friday Promo customers vs everyone else?",
    "How many At Risk customers do we have, and how much have they spent in total?",
    "Did the checkout redesign A/B test improve completion on iOS?",
]

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.subheader("Try asking")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex
    total = sum(h["result"].cost_usd for h in st.session_state.history)
    st.divider()
    st.metric("Session cost", f"${total:.3f}")


def render(result) -> None:
    if result.error:
        st.error(result.error)
        return
    st.markdown(result.answer)
    if result.value is not None:
        st.metric("Answer", f"{result.value:,.2f} {result.unit or ''}".strip())
    if result.sql:
        with st.expander("SQL used"):
            st.code(result.sql, language="sql")
            try:
                res = _client().query(result.sql)
                st.dataframe(pd.DataFrame(res.result_rows[:200], columns=res.column_names), hide_index=True)
            except Exception as exc:
                st.caption(f"Could not re-run query: {exc}")
    st.caption(f"{len(result.queries)} queries · {result.latency_s}s · ${result.cost_usd:.3f}")


for h in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(h["question"])
    with st.chat_message("assistant"):
        render(h["result"])

question = st.chat_input("Ask a question about your data") or st.session_state.pop("pending", None)
if question:
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Querying ClickHouse..."):
            result = ask(question, schema_doc=schema_doc())
        render(result)
    st.session_state.history.append({"question": question, "result": result})
    st.rerun()
