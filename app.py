"""Streamlit web app.  Run:  streamlit run app.py"""

import streamlit as st

from ecosort import EcoSort
from ecosort.config import Settings
from ecosort.feedback import FeedbackCounter
from ecosort.vision import VisionUnavailable, describe_image

COLOURS = {"Wet": "#3E8E5A", "Dry": "#2F6DB5", "Sanitary": "#C26A12", "Special care": "#8E4585", "Not sure": "#5A6B62"}

st.set_page_config(page_title="EcoSort Campus", page_icon="♻️", layout="centered")


@st.cache_resource
def get_bot() -> EcoSort:
    return EcoSort(Settings.from_env())


bot = get_bot()
fb = FeedbackCounter(bot.settings.feedback_path)

st.title("♻️ EcoSort Campus")
st.caption("Which of the four waste streams does this item belong to? "
           "SDG 12 · Responsible Consumption and Production")

with st.sidebar:
    st.subheader("About")
    st.write("EcoSort answers only from its knowledge base (SWM Rules 2026 plus a campus bin guide). "
             "If it does not know, it says **Not sure**.")
    if bot.mode == "offline":
        st.write("**Mode:** offline (answers straight from the knowledge base)")
        if bot.settings.llm_provider != "offline":
            st.warning("Granite is not connected, so the app is running offline.")
    else:
        st.write(f"**Mode:** IBM Granite via `{bot.mode}`")
    st.write("**Privacy:** no login, no names. Photos stay in memory. "
             "Only three anonymous feedback counters are stored.")
    c = fb.counts()
    st.write(f"Feedback so far: 👍 {c['helpful']} · 👎 {c['not_helpful']} · ❔ {c['not_sure']}")

query = st.text_input("Type an item", placeholder="e.g. banana peel, tube light, plastic bottle")
photo = st.file_uploader("...or upload a photo (experimental, needs a local vision model)",
                         type=["jpg", "jpeg", "png"])

item = query
if photo is not None and not query:
    try:
        with st.spinner("Looking at your photo..."):
            item = describe_image(photo.getvalue(), bot.settings)
        st.info(f"I think this is: **{item}**")
    except VisionUnavailable as e:
        st.warning(str(e))
        item = ""

MAX_PER_SESSION = 60  # keeps a public demo from being hammered
st.session_state.setdefault("asked", 0)

if item and st.session_state["asked"] >= MAX_PER_SESSION:
    st.info("You have reached the demo limit for this session. Reload the page to continue.")
    item = ""

if item:
    st.session_state["asked"] += 1
    a = bot.ask(item)
    colour = COLOURS.get(a.stream, COLOURS["Not sure"])
    st.markdown(
        f"<div style='padding:1rem;border-radius:12px;border:2px solid {colour}'>"
        f"<span style='background:{colour};color:white;padding:2px 12px;border-radius:12px;"
        f"font-weight:700'>{a.stream.upper()}</span>"
        f"<p style='margin:.8rem 0 .2rem'><b>Why:</b> {a.why}</p>"
        f"<p style='margin:.2rem 0'><b>How to dispose:</b> {a.dispose}</p>"
        f"<p style='margin:.2rem 0;opacity:.7'><b>Source:</b> {a.source}</p></div>",
        unsafe_allow_html=True,
    )
    if a.note:
        st.caption(a.note)
    with st.expander("How did I get this answer?"):
        st.write("Passages retrieved from the knowledge base:")
        for t in a.evidence or ["(none matched)"]:
            st.write(f"- {t}")
        st.write(f"Retrieval score: `{a.score}` (minimum to answer: `{bot.settings.min_score}`)")

    col1, col2, _ = st.columns([1, 1, 4])
    if col1.button("👍 Helpful"):
        fb.record("helpful" if a.confident else "not_sure")
        st.toast("Thanks! Only a counter was updated.")
    if col2.button("👎 Not helpful"):
        fb.record("not_helpful")
        st.toast("Thanks! Only a counter was updated.")

st.divider()
st.caption("Advisory tool. Local bin colours and collection rules may differ; "
           "when in doubt, ask the campus sustainability desk.")
