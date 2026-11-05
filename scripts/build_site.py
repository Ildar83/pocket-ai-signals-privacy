"""Generate the full static privacy page; no browser JavaScript is used."""
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "src" / "privacy-policy.md"
policy = source.read_text(encoding="utf-8")
policy = policy.replace("\n**Draft for review — not yet approved for publication**\n", "\n")
assert "## 9. Contact" in policy, "The policy must be complete."
assert "com.pocketai.signals" in policy
body = markdown.markdown(policy, output_format="html")
page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Privacy Policy for Pocket AI Signals / Pocket AISignals, Android package com.pocketai.signals. Developer: Σpsilon AI, Ильдар Хузин. Contact: otrade2019@gmail.com.">
  <meta name="referrer" content="no-referrer">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; img-src 'none'; script-src 'none'; connect-src 'none'; base-uri 'none'; form-action 'none'">
  <title>Privacy Policy — Pocket AI Signals</title>
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
  <main>
    <article aria-label="Pocket AI Signals Privacy Policy">
{body}
    </article>
  </main>
</body>
</html>
'''
output = ROOT / "docs" / "index.html"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(page, encoding="utf-8")
print(f"Generated {output.relative_to(ROOT)} — full policy as static HTML")
