"""Build the static website: docs/index.html (single self-contained file).

    python scripts/build_site.py

Inlines site/engine.js and data/knowledge_base.json into site/template.html, so the
website always uses the same knowledge base as the Python app. Host docs/ on GitHub Pages.
After deploying the Streamlit app, put its https URL in site/config.json ("app_url") and rebuild
to add an "Open the Granite-powered app" link to the page.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
template = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
engine = (ROOT / "site" / "engine.js").read_text(encoding="utf-8")
kb = json.loads((ROOT / "data" / "knowledge_base.json").read_text(encoding="utf-8"))

# Keep only what the website needs, and make the JSON safe to inline in a <script> tag.
kb_js = json.dumps({"ambiguous": kb.get("ambiguous", []), "chunks": kb["chunks"]}, ensure_ascii=False)
kb_js = kb_js.replace("</", "<\\/")

cfg = json.loads((ROOT / "site" / "config.json").read_text(encoding="utf-8"))
app_url = (cfg.get("app_url") or "").strip()
live = f' <a href="{app_url}" rel="noopener">Open the Granite-powered app.</a>' if app_url.startswith("https://") else ""

html = (template.replace("/*__ENGINE__*/", engine).replace("/*__KB__*/", kb_js).replace("<!--LIVE_APP-->", live))
assert "__ENGINE__" not in html and "__KB__" not in html

out = ROOT / "docs" / "index.html"
out.write_text(html, encoding="utf-8")
print(f"Wrote {out.relative_to(ROOT)} ({len(html) / 1024:.0f} KB)")
