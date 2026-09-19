/* EcoSort engine (JavaScript port of the Python pipeline, offline mode).
 * Mirrors ecosort/retriever.py, privacy.py and pipeline.py so the static website
 * behaves like the Python app. Keep the two in sync (scripts/check_engine.js tests parity).
 */
(function (root) {
  "use strict";

  const STOP = new Set(["a","an","the","of","in","on","to","my","this","that","is","it","and","or","with",
    "used","old","broken","empty","waste","item","throw","thrown","dispose","where","what","how","do","does",
    "i","we","put","into","bin","some","piece","from","canteen","hostel","campus","small","big","large",
    "dirty","clean","half","eaten"]);

  function tokenize(text) {
    text = String(text).toLowerCase().replace(/\bcan (i|we|you)\b/g, " ");
    const out = [];
    for (let t of (text.match(/[a-z]+/g) || [])) {
      if (STOP.has(t)) continue;
      if (t.endsWith("ies") && t.length > 4) t = t.slice(0, -3) + "y";
      else if (t.endsWith("s") && !t.endsWith("ss") && t.length > 3) t = t.slice(0, -1);
      out.push(t);
    }
    return out;
  }

  function features(tokens) {           // unigrams + bigrams, like sklearn ngram_range=(1,2)
    const f = tokens.slice();
    for (let i = 0; i < tokens.length - 1; i++) f.push(tokens[i] + " " + tokens[i + 1]);
    return f;
  }

  function sanitize(text) {
    text = String(text || "")
      .replace(/[\w.+-]+@[\w-]+\.[\w.-]+/g, " ")
      .replace(/(?<!\d)(?:\+?\d[\s-]?){10,13}(?!\d)/g, " ")
      .replace(/\s+/g, " ").trim();
    return text.slice(0, 200);
  }

  class Retriever {
    constructor(chunks) {
      this.chunks = chunks;
      const docs = chunks.map(c => features(tokenize([c.title, ...c.keywords, c.why].join(" "))));
      const df = new Map();
      for (const d of docs) for (const f of new Set(d)) df.set(f, (df.get(f) || 0) + 1);
      const n = docs.length;
      this.idf = new Map();
      for (const [f, c] of df) this.idf.set(f, Math.log((1 + n) / (1 + c)) + 1);
      this.vecs = docs.map(d => this._vector(d));
    }
    _vector(feats) {
      const tf = new Map();
      for (const f of feats) if (this.idf.has(f)) tf.set(f, (tf.get(f) || 0) + 1);
      const v = new Map(); let norm = 0;
      for (const [f, c] of tf) { const w = (1 + Math.log(c)) * this.idf.get(f); v.set(f, w); norm += w * w; }
      norm = Math.sqrt(norm) || 1;
      for (const [f, w] of v) v.set(f, w / norm);
      return v;
    }
    search(query, k = 3) {
      const toks = tokenize(query);
      if (!toks.length) return [];
      const q = this._vector(features(toks));
      const scored = this.vecs.map((v, i) => {
        let s = 0; for (const [f, w] of q) if (v.has(f)) s += w * v.get(f);
        return { chunk: this.chunks[i], score: s, i };
      }).filter(x => x.score > 0);
      scored.sort((a, b) => b.score - a.score || a.i - b.i);
      return scored.slice(0, k);
    }
  }

  class EcoSort {
    constructor(kb, opts = {}) {
      this.retriever = new Retriever(kb.chunks);
      this.ambiguous = (kb.ambiguous || []).map(s => s.toLowerCase());
      this.minScore = opts.minScore ?? 0.15;
      this.topK = opts.topK ?? 3;
    }
    _notSure(item, why, score = 0, evidence = []) {
      return { item, stream: "Not sure", confident: false, score,
        why: why || "I could not find this item in my sources, so I will not guess.",
        dispose: "Please ask the campus sustainability desk.", source: "-", evidence };
    }
    ask(query) {
      const item = sanitize(query);
      if (!item) return this._notSure(item, "Please type the name of an item.");
      const low = item.toLowerCase();
      if (this.ambiguous.some(p => low.includes(p)))
        return this._notSure(item, "Where this goes depends on its condition (for example soiled or plastic-lined) or on local rules, so I will not guess.");
      const hits = this.retriever.search(item, this.topK);
      const evidence = hits.map(h => ({ title: h.chunk.title, stream: h.chunk.stream, score: h.score }));
      if (!hits.length || hits[0].score < this.minScore)
        return this._notSure(item, null, hits.length ? hits[0].score : 0, evidence);
      const top = hits[0].chunk;
      return { item, stream: top.stream, confident: true, score: Math.round(hits[0].score * 1000) / 1000,
        why: top.why, dispose: top.dispose, source: top.source, evidence };
    }
  }

  const api = { tokenize, sanitize, Retriever, EcoSort };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.EcoSortEngine = api;
})(typeof window !== "undefined" ? window : globalThis);
