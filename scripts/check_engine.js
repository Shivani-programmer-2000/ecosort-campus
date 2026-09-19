// Verifies the JavaScript engine (used by the website) gives the same answers as the Python
// evaluation set.   node scripts/check_engine.js
const fs = require("fs");
const path = require("path");
const { EcoSort } = require("../site/engine.js");

const root = path.join(__dirname, "..");
const kb = JSON.parse(fs.readFileSync(path.join(root, "data", "knowledge_base.json"), "utf8"));
const rows = fs.readFileSync(path.join(root, "eval", "test_items.csv"), "utf8").trim().split(/\r?\n/).slice(1)
  .map(l => { const i = l.lastIndexOf(","); return [l.slice(0, i), l.slice(i + 1)]; });

const bot = new EcoSort(kb);
let ok = 0, wrong = [];
for (const [item, expected] of rows) {
  const a = bot.ask(item);
  if (a.stream === expected) ok++; else wrong.push([item, expected, a.stream]);
}
console.log(`JS engine: ${ok}/${rows.length} correct`);
wrong.forEach(w => console.log("  mismatch:", w.join(" | ")));
process.exit(wrong.length ? 1 : 0);
