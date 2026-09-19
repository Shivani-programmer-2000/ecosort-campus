"""EcoSort Campus: Streamlit web app.   Run:  streamlit run app.py

The look matches the static website in docs/index.html. All HTML and CSS live in ecosort/ui.py.
"""

import streamlit as st

from ecosort import EcoSort, ui
from ecosort.config import Settings
from ecosort.feedback import FeedbackCounter

st.set_page_config(page_title="EcoSort Campus: which bin does it go in?", page_icon="♻️",
                   layout="wide", initial_sidebar_state="collapsed")

MAX_PER_SESSION = 60  # keeps a public demo from being hammered


@st.cache_resource
def get_bot() -> EcoSort:
    return EcoSort(Settings.from_env())


bot = get_bot()
fb = FeedbackCounter(bot.settings.feedback_path)
ss = st.session_state
ss.setdefault("asked", 0)
ss.setdefault("answer", None)
ss.setdefault("fb_done", False)
ss.setdefault("pending", None)


def run(query: str) -> None:
    if ss["asked"] >= MAX_PER_SESSION:
        st.toast("Demo limit reached for this session. Reload the page to continue.")
        return
    ss["asked"] += 1
    ss["answer"] = bot.ask(query)
    ss["fb_done"] = False


def pick_example() -> None:
    choice = ss.get("example")
    if choice:
        ss["item_box"] = choice
        ss["pending"] = choice
        ss["example"] = None


if ss["pending"]:
    run(ss["pending"])
    ss["pending"] = None

st.markdown(ui.CSS, unsafe_allow_html=True)
st.html(ui.header())

left, right = st.columns([1.05, 1], gap="large")

with left:
    st.html(ui.hero_copy())
    with st.form("ask", border=False):
        c_in, c_btn = st.columns([4, 1.3], vertical_alignment="center")
        query = c_in.text_input("Item to sort", key="item_box",
                                placeholder="For example: banana peel", label_visibility="collapsed")
        submitted = c_btn.form_submit_button("Sort it", type="primary")
    if submitted:
        run(query)
    try:
        st.pills("Try an example", ui.EXAMPLES, key="example", on_change=pick_example,
                 label_visibility="collapsed", wrap=True)
    except TypeError:  # older Streamlit without the wrap option
        st.pills("Try an example", ui.EXAMPLES, key="example", on_change=pick_example,
                 label_visibility="collapsed")
    st.html(ui.fine_print())

answer = ss["answer"]
with right:
    st.markdown(ui.bins(answer.stream if answer and answer.confident else None), unsafe_allow_html=True)
    st.html(ui.answer_card(answer))
    if answer is not None:
        if answer.note:
            st.caption(answer.note)
        with st.expander("How EcoSort got this"):
            if answer.evidence:
                for t in answer.evidence:
                    st.write(f"- {t}")
            else:
                st.write("No passage in the knowledge base matched this item.")
            st.write(f"Match score {answer.score}. An answer needs at least {bot.settings.min_score}.")
        if ss["fb_done"]:
            st.caption("Thanks. Saved as an anonymous counter only.")
        else:
            with st.container(key="fb"):
                c0, c1, c2, _ = st.columns([2.6, 1, 1, 2.4], vertical_alignment="center")
                c0.markdown("Was this useful?")
                if c1.button("Yes", key="fb_yes"):
                    fb.record("helpful" if answer.confident else "not_sure")
                    ss["fb_done"] = True
                    st.rerun()
                if c2.button("No", key="fb_no"):
                    fb.record("not_helpful")
                    ss["fb_done"] = True
                    st.rerun()

st.html(ui.sections(bot.settings.author))
