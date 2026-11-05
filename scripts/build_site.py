"""Generate the full static privacy page for GitHub Pages and Webdev preview."""
from pathlib import Path
from shutil import copyfile

import markdown

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "src" / "privacy-policy.md"
policy = source.read_text(encoding="utf-8")
assert "Draft for review" not in policy, "Only an approved policy can be published."
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
# The owner enabled GitHub Pages from main:/; publish the same static files there.
(ROOT / "index.html").write_text(page, encoding="utf-8")
for name in ["styles.css", "manus-routes.json"]:
    copyfile(ROOT / "docs" / name, ROOT / name)
(ROOT / ".nojekyll").touch()
print("Generated complete static policy in docs/ and the GitHub Pages root")
