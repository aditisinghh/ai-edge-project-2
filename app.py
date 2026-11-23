"""Streamlit app for the site-screening agent.

    streamlit run app.py

Type a request (candidate counties or an open question), watch the agent's tool calls live,
then read and download the memo.
"""
import json
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Data Center Site Screener", page_icon="⚡", layout="wide")

EXAMPLES = [
    "Compare Loudoun VA, El Paso TX and Grant WA for a 100 MW AI campus.",
    "Where should we look for our next campus in Texas? Industrial power under 7 cents.",
    "We're considering Fort Bend TX and DeKalb GA. Which should go to diligence first?",
    "Screen Washington County for a data center.",
]

with st.sidebar:
    st.header("Settings")
    key = st.text_input("Anthropic API key", value=os.getenv("ANTHROPIC_API_KEY", ""), type="password",
                        help="Stored only for this session. Or set ANTHROPIC_API_KEY in .env")
    eia = st.text_input("EIA API key (optional)", value=os.getenv("EIA_API_KEY", ""), type="password",
                        help="For live monthly power prices. Without it the agent uses 2024 prices.")
    base_url = st.text_input("API base URL", value=os.getenv("ANTHROPIC_BASE_URL", ""),
                             help="Leave blank for Anthropic. MIT Parley: https://parley.api.mit.edu")
    default_model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")
    model = st.text_input("Model", value=default_model,
                          help="e.g. claude-sonnet-5-5, claude-opus-5-5, claude-haiku-5-5 (use the names your provider lists)")
    st.caption("Data: Project 1 county model + EIA-861, LBNL Queued Up, NOAA, USDA, WRI, Census, IM3, Compute Atlas. "
               "Contiguous US only.")

st.title("⚡ Data Center Site Screener")
st.write("An AI analyst that screens US counties for a data center campus and writes a cited memo for your site team.")

choice = st.selectbox("Try an example, or write your own below", ["(write my own)"] + EXAMPLES)
request = st.text_area("Request", value="" if choice == "(write my own)" else choice, height=90)

if st.button("Run screening", type="primary", disabled=not request.strip()):
    if not key:
        st.error("Add your Anthropic API key in the sidebar first.")
        st.stop()
    os.environ["ANTHROPIC_API_KEY"] = key
    if eia:
        os.environ["EIA_API_KEY"] = eia
    import anthropic

    from agent.agent import SiteAgent

    left, right = st.columns([1, 2])
    with left:
        st.subheader("Agent steps")
        log = st.container()

    def show(step):
        if step.kind == "tool":
            with log.expander(f"🔧 {step.name}({', '.join(f'{k}={v}' for k, v in step.input.items())})"):
                try:
                    st.json(json.loads(step.output))
                except json.JSONDecodeError:
                    st.code(step.output)

    with st.spinner("Screening counties..."):
        result = SiteAgent(client=anthropic.Anthropic(api_key=key, base_url=base_url or None), model=model).run(request, on_step=show)

    with right:
        st.subheader("Screening memo")
        st.markdown(result.memo)
        st.download_button("Download memo (.md)", result.memo, file_name="site_screening_memo.md")
    st.caption(f"{len(result.tool_calls)} tool calls · {result.seconds:.0f} s · "
               f"{result.input_tokens:,} in / {result.output_tokens:,} out tokens · ≈ ${result.cost_usd:.3f} · {result.model}")
