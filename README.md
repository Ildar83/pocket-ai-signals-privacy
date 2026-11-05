# Pocket AI Signals Privacy Policy

Independent, text-only privacy-policy website for **Pocket AI Signals / Pocket AISignals**, Android package `com.pocketai.signals`. Developer: **Σpsilon AI / Ильдар Хузин**. Privacy contact: **otrade2019@gmail.com**.

The policy text and data-handling procedures were approved by the owner on November 5, 2026 before publication. The policy does not make trading, performance, accuracy, or approval claims.

## Static website

`docs/index.html` contains the entire policy as ordinary HTML. It does not require JavaScript, account access, a server, or a database. `docs/styles.css` is the only page asset. No images, ads, installation links, Telegram links, forms, or analytics are included.

GitHub Pages is configured to publish the `docs` folder from the `main` branch. The empty `docs/.nojekyll` file prevents Jekyll processing. No user-maintained GitHub Actions workflow is required.

## Updating the text

The approved source is `src/privacy-policy.md`. Obtain owner approval of changed factual disclosures, update the policy date when appropriate, and regenerate the committed static HTML:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build_site.py
```

For local review only, serve `docs` with `python3 -m http.server 3000 --directory docs`. Visitors to the deployed website do not need Python or Markdown.

This repository contains only the privacy site, not the Android application. Do not commit credentials, support correspondence, application source, or unrelated projects. Hosting this policy does not update Google Play Data Safety declarations or guarantee approval.
