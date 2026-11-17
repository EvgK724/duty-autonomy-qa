# Isolated synthetic autonomy QA

Only fictitious January 2099 shifts for Synthetic Doctor A/B. This is not a real duty application or owner intake. No production endpoints, secrets, schedules or identifiers are used.

One manually/App-dispatched workflow builds actual PDF/XLSX/ICS and a stateless page, commits only an exact artifact allowlist, then deploys this repository's Pages artifact. No push/schedule triggers, inherited workflows, repository secrets, PAT or real reader are required. The GitHub App needs only this repository's Actions write plus mandatory Metadata read. The workflow's temporary GitHub token separately writes generated files; deploy job uses Pages/OIDC permissions.

Local: `python -m pip install -r dezhurstva/tools/pdf-requirements.txt` then `python -B dezhurstva/tools/owner_bridge/runner.py`.

Fixed public-safe payload: `qa/approved-fixture.json`. Queue/approval tests must explicitly set syntheticOnly and use the same payloadHash. A successful isolated test proves transport/correlation/artifact verification only, not real owner consent, real Sheets, all production workflows, or reliability under outage.

The page has no JavaScript, network connections, cookies, service worker or local/session storage. The source is derived from the reviewed synthetic source allowlist; unused workflows/reader code are not copied.
