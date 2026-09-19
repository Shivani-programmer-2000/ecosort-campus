"""HTML and CSS for the Streamlit app. The look matches the static website (docs/index.html)."""

from __future__ import annotations

import html as _h

STREAMS = ["Wet", "Dry", "Sanitary", "Special care"]
EXAMPLES = ["banana peel", "tube light", "used tea bag", "sanitary pad", "old phone charger"]

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Instrument+Sans:wght@400;500;600&display=swap');
:root{--bg:#F1F5F0;--surface:#fff;--wash:#E3EBE5;--ink:#14211A;--muted:#4F5F56;--line:#CBD6CE;--brand:#0F4C3A;
--wet:#1C7F4B;--dry:#2A66BD;--sanitary:#B05A0C;--special:#8A4286;--none:#56655D;
--display:"Bricolage Grotesque","Trebuchet MS",system-ui,sans-serif;--body:"Instrument Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.stApp,.stApp p,.stApp li,.stApp label,.stApp button,.stApp input,.stApp summary{font-family:var(--body)}
.stApp{background:var(--bg);color:var(--ink)}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],#MainMenu,footer{display:none !important}
.block-container{max-width:1080px;padding:1rem 1.25rem 3rem}
.eco *{box-sizing:border-box}
.eco h1,.eco h2,.eco h3{font-family:var(--display);color:var(--ink);line-height:1.08;margin:0;padding:0;letter-spacing:-0.02em;text-wrap:balance}
.eco p{margin:0 0 1em}
.eco{font-size:1.0625rem;line-height:1.6;color:var(--ink)}
.eco-brand{font-family:var(--display);font-weight:800;font-size:1.25rem;letter-spacing:-.02em;padding:.6rem 0 1.2rem}
.eco-h1{font-size:clamp(2.6rem,6vw,4.6rem) !important;font-weight:800;max-width:12ch}
.eco-lede{font-size:1.2rem;color:var(--muted);max-width:46ch;margin:1.2rem 0 1.4rem !important}
.eco-fine{font-size:.9rem;color:var(--muted);margin-top:1.2rem;max-width:46ch}

/* Streamlit widgets restyled */
[data-testid="stForm"]{border:0 !important;padding:0 !important;background:transparent}
[data-testid="stTextInputRootElement"],div[data-baseweb="input"]{background:#fff !important;border:2px solid var(--line) !important;border-radius:12px !important}
[data-testid="stTextInputRootElement"]:focus-within,div[data-baseweb="input"]:focus-within{border-color:var(--brand) !important;box-shadow:0 0 0 3px rgba(31,111,235,.25)}
div[data-baseweb="input"] > div,div[data-baseweb="base-input"]{background:transparent !important}
[data-testid="InputInstructions"]{display:none !important}
[data-testid="stTextInput"] input{font-size:1.1rem !important;padding:.85rem 1rem !important;color:var(--ink) !important;background:transparent !important}
[data-testid="stFormSubmitButton"] button,[data-testid="stBaseButton-primaryFormSubmit"]{background:var(--brand) !important;color:#fff !important;border:0 !important;border-radius:12px !important;padding:.75rem 1.6rem !important;font-weight:600 !important;font-size:1.05rem !important;min-height:0}
[data-testid="stFormSubmitButton"] button:hover{filter:brightness(1.12)}
[data-testid="stPills"] button,button[kind="pills"],button[kind="pillsActive"]{border:1px solid var(--line) !important;border-radius:999px !important;background:transparent !important;color:var(--ink) !important;font-size:.95rem !important;padding:.2rem .85rem !important}
[data-testid="stPills"] button:hover{background:var(--wash) !important}
[data-testid="stExpander"]{border:1px solid var(--line) !important;border-radius:12px !important;background:transparent}
[data-testid="stExpander"] summary,[data-testid="stExpander"] p,[data-testid="stExpander"] li{color:var(--muted);font-size:.95rem}
.st-key-fb button{border:1px solid var(--line) !important;border-radius:8px !important;background:transparent !important;color:var(--ink) !important;padding:.15rem .8rem !important;min-height:0}
.st-key-fb button:hover{background:var(--wash) !important}
.st-key-fb button{white-space:nowrap}
.st-key-fb [data-testid="stHorizontalBlock"]{flex-wrap:nowrap !important;gap:.5rem}
.st-key-fb p{margin:0;white-space:nowrap;font-size:.95rem;color:var(--muted)}

/* Bins */
.eco-bins{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(.4rem,2vw,1rem);margin:0 0 1.4rem}
.bin{text-align:center;--c:var(--none)}
.bin svg{width:100%;max-width:150px;height:auto;overflow:visible}
.bin .body{fill:var(--c);fill-opacity:.16;stroke:var(--c);stroke-width:3;stroke-linejoin:round}
.bin .slat{stroke:var(--c);stroke-opacity:.5;stroke-width:3;stroke-linecap:round}
.bin .lid{fill:var(--c);transform-origin:16px 36px}
.bin .drop{fill:var(--ink);opacity:0}
.bin.is-open .lid{animation:lift .45s cubic-bezier(.3,1.4,.5,1) both}
.bin.is-open .body{fill-opacity:.55}
.bin.is-open .drop{animation:drop .5s ease-out .1s both}
@keyframes lift{from{transform:rotate(0)}to{transform:rotate(-32deg)}}
@keyframes drop{0%{opacity:1;transform:translateY(-46px)}70%{opacity:1}100%{opacity:0;transform:translateY(8px)}}
.bin-name{font-family:var(--display);font-weight:800;font-size:clamp(.72rem,2.5vw,1.05rem);color:var(--c);margin-top:.3rem;white-space:nowrap;overflow:visible}
.bin.is-open .bin-name{text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:5px}
[data-s="Wet"]{--c:var(--wet)}[data-s="Dry"]{--c:var(--dry)}[data-s="Sanitary"]{--c:var(--sanitary)}[data-s="Special care"]{--c:var(--special)}

/* Answer card */
.eco-answer{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:1.4rem 1.5rem;min-height:9rem;margin-bottom:.8rem}
.eco-answer.empty{color:var(--muted);display:flex;align-items:center;background:transparent;border-style:dashed}
.eco-echo{color:var(--muted);font-size:.95rem;margin-bottom:.5rem !important}
.eco-badge{display:inline-block;font-family:var(--display);font-weight:800;font-size:1.5rem;color:#fff;background:var(--c,var(--none));border-radius:10px;padding:.1rem .8rem;margin:0 0 1rem !important}
.eco-answer dl{margin:0;display:grid;grid-template-columns:8.5rem 1fr;gap:.5rem 1rem}
.eco-answer dl,.eco-answer dt,.eco-answer dd{padding:0}
.eco-answer dt{color:var(--muted);font-weight:500}
.eco-answer dd{margin:0}

/* Page sections */
.eco-band{padding:3.5rem 0 2.5rem;border-top:1px solid var(--line);margin-top:1.5rem}
.eco-band h2{font-size:clamp(1.9rem,4.5vw,3rem) !important;font-weight:800;max-width:20ch;margin-bottom:1rem}
.eco-intro{color:var(--muted);max-width:58ch;margin-bottom:2rem !important}
.eco-streams{border-top:1px solid var(--line);margin-bottom:0}
.eco-row{display:grid;grid-template-columns:13rem 1fr 1fr;gap:1rem 2rem;padding:1.4rem 0;border-bottom:1px solid var(--line);align-items:baseline}
.eco-row h3{font-size:1.7rem !important;color:var(--c,var(--none));font-weight:800}
.eco-row .lbl{display:block;color:var(--muted);font-size:.9rem}
.eco-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,1fr);gap:1.2rem;counter-reset:s}
.eco-steps li{counter-increment:s;position:relative;padding-top:3rem;margin:0}
.eco-steps li::before{content:counter(s);position:absolute;top:0;left:0;width:2.2rem;height:2.2rem;border-radius:50%;display:grid;place-items:center;font-family:var(--display);font-weight:800;background:var(--brand);color:#fff}
.eco-steps li::after{content:"";position:absolute;top:1.1rem;left:2.6rem;right:-1rem;height:2px;background:var(--line)}
.eco-steps li:last-child::after{display:none}
.eco-steps h3{font-size:1.15rem !important;margin-bottom:.4rem}
.eco-steps p{font-size:.97rem;color:var(--muted);margin:0}
.eco .eco-guard{margin-top:2rem !important;background:var(--wash);border-radius:14px;padding:1.1rem 1.4rem;max-width:720px}
.eco-two,.eco-principles{display:grid;grid-template-columns:1fr 1fr;gap:2rem 3rem}
.eco-two h3,.eco-principles h3{font-size:1.4rem !important;margin-bottom:.4rem}
.eco-two p,.eco-principles p{color:var(--muted);margin:0}
.eco-foot{border-top:1px solid var(--line);padding:2rem 0 1rem;color:var(--muted);font-size:.95rem}
.eco-foot p{max-width:70ch}
@media(max-width:860px){
 .eco-row{grid-template-columns:1fr;gap:.4rem}
 .eco-steps{grid-template-columns:1fr;gap:1.6rem}
 .eco-steps li{padding:0 0 0 3.2rem}
 .eco-steps li::after{top:2.4rem;left:1.05rem;right:auto;width:2px;height:calc(100% + .2rem)}
 .eco-two,.eco-principles{grid-template-columns:1fr;gap:2rem}
 .eco-answer dl{grid-template-columns:1fr;gap:.1rem}
 .eco-answer dd{margin-bottom:.7rem}
}
@media(prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important}}
</style>"""

_BIN_SVG = (
    '<svg viewBox="0 0 120 150" role="img" focusable="false" aria-hidden="true">'
    '<path class="body" d="M20 40 H100 L94 138 Q93.5 146 86 146 H34 Q26.5 146 26 138 Z"/>'
    '<line class="slat" x1="47" y1="58" x2="49" y2="128"/><line class="slat" x1="60" y1="58" x2="60" y2="128"/>'
    '<line class="slat" x1="73" y1="58" x2="71" y2="128"/><circle class="drop" cx="60" cy="30" r="8"/>'
    '<g class="lid"><rect x="16" y="28" width="88" height="12" rx="5"/><rect x="48" y="21" width="24" height="9" rx="4.5"/></g></svg>'
)


def header() -> str:
    return '<div class="eco"><div class="eco-brand">EcoSort Campus</div></div>'


def hero_copy() -> str:
    return (
        '<div class="eco"><h1 class="eco-h1">Which bin does it go in?</h1>'
        '<p class="eco-lede">Type any item. EcoSort answers from India\'s four-stream waste rules, shows where the '
        'answer came from, and tells you when it is not sure.</p></div>'
    )


def fine_print() -> str:
    return (
        '<div class="eco"><p class="eco-fine">Advisory only. The knowledge base is a small sample, so check your own '
        'campus and municipal rules. Nothing you type is stored: only anonymous feedback counters are kept.</p></div>'
    )


def bins(open_stream: str | None) -> str:
    cells = "".join(
        f'<div class="bin{" is-open" if s == open_stream else ""}" data-s="{s}">{_BIN_SVG}'
        f'<div class="bin-name">{s}</div></div>'
        for s in STREAMS
    )
    return f'<div class="eco"><div class="eco-bins">{cells}</div></div>'


def answer_card(a) -> str:
    """a is an ecosort.pipeline.Answer, or None for the empty state."""
    if a is None:
        return '<div class="eco"><div class="eco-answer empty">Your answer will appear here.</div></div>'
    e = _h.escape
    data = f' data-s="{e(a.stream)}"' if a.confident else ""
    echo = f'<p class="eco-echo">For &ldquo;{e(a.item)}&rdquo;</p>' if a.item else ""
    return (
        f'<div class="eco"><div class="eco-answer"{data}>{echo}'
        f'<p class="eco-badge">{e(a.stream)}</p>'
        f'<dl><dt>Why</dt><dd>{e(a.why)}</dd><dt>How to dispose</dt><dd>{e(a.dispose)}</dd>'
        f'<dt>Source</dt><dd>{e(a.source)}</dd></dl></div></div>'
    )


def sections(author: str) -> str:
    e = _h.escape
    rows = [
        ("Wet", "Kitchen scraps, fruit and vegetable peels, meat, flowers", "Composting or bio-methanation"),
        ("Dry", "Plastic, paper, metal, glass, wood, rubber", "A Material Recovery Facility for sorting and recycling"),
        ("Sanitary", "Used diapers, sanitary pads, tampons, condoms", "Wrapped securely and stored separately"),
        ("Special care", "Paint cans, bulbs, batteries, mercury thermometers, expired medicines", "Designated collection centres"),
    ]
    streams = "".join(
        f'<div class="eco-row" data-s="{s}"><h3>{s}</h3><p><span class="lbl">What goes in</span>{a}</p>'
        f'<p><span class="lbl">Where it goes</span>{b}</p></div>'
        for s, a, b in rows
    )
    steps = [
        ("You type an item", "Email addresses and phone numbers are removed before anything else happens."),
        ("Ambiguity check", "A used tissue or a greasy pizza box depends on its condition, so EcoSort does not guess."),
        ("Retrieval", "The closest passages in the rules and the campus guide are found. With a Granite key, these passages are also handed to the model to write the answer (RAG); without one, the passages are used directly."),
        ("Confidence check", 'A weak match becomes "Not sure" instead of a confident mistake.'),
        ("Answer with source", "The stream, the reason, how to dispose of it, and where that came from."),
    ]
    steps_html = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in steps)
    principles = [
        ("Fairness", "Plain language, no login and no cost. The knowledge base is meant to be extended with items from many regions and households, then tested."),
        ("Transparency", 'Every answer shows its stream, reason and source. Open "How EcoSort got this" to see the passages and the match score.'),
        ("Ethics", "Advice only. It never monitors or penalises people, and hazardous or unclear cases go to a person at the campus sustainability desk."),
        ("Privacy", "No accounts, no names. Personal details typed by mistake are stripped, and feedback is kept only as anonymous counters."),
    ]
    prin = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in principles)
    return (
        '<div class="eco">'
        '<section class="eco-band"><h2>Four streams, one rule</h2>'
        '<p class="eco-intro">The Solid Waste Management Rules, 2026 have required four-stream segregation at source since '
        '1 April 2026. It replaced the older wet and dry split.</p>'
        f'<div class="eco-streams">{streams}</div></section>'
        '<section class="eco-band"><h2>How an answer is made</h2>'
        '<p class="eco-intro">EcoSort never answers from memory. Every answer is built from a passage it can point to, and '
        'three checks decide whether it answers at all.</p>'
        f'<ol class="eco-steps">{steps_html}</ol>'
        '<p class="eco-guard">When IBM Granite is connected, the model writes the answer from the retrieved passages, and its '
        'stream must match the evidence or the answer becomes "Not sure". Without Granite, the app answers straight from the '
        'best passage (offline mode).</p></section>'
        '<section class="eco-band"><h2>Built with IBM Bob, ready for IBM Granite</h2><div class="eco-two">'
        '<div><h3>Bob builds it</h3><p>IBM Bob is the AI development partner used while building the project: planning the '
        'architecture, drafting code and tests, writing documentation and reviewing for security. A person reads and approves '
        'every change.</p></div>'
        '<div><h3>Granite (optional)</h3><p>The app can use IBM Granite models through watsonx.ai or Ollama, with '
        'retrieval-augmented generation. Without keys it runs in offline mode and answers straight from the knowledge base. '
        'The source code, tests and evaluation are in the project repository.</p></div></div></section>'
        f'<section class="eco-band"><h2>Responsible by design</h2><div class="eco-principles">{prin}</div></section>'
        '<footer class="eco-foot"><p>EcoSort Campus supports SDG 12, Responsible Consumption and Production, with SDG 11 and '
        'SDG 13 as secondary goals. It is a student project for the 1M1B, IBM SkillsBuild and AICTE AI for Sustainability '
        f'Virtual Internship.</p><p>{e(author)}</p></footer></div>'
    )
