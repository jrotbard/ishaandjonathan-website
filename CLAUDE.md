# Isha & Jonathan wedding website

Static site (no build step): `index.html` (four-tab shell + sidebar), `save-the-date.html` (envelope page, shown in an iframe on the Save the Date tab), `img/`, `fonts/`, `audio/`, `cal/`.

- GitHub: https://github.com/jrotbard/ishaandjonathan-website (private, branch `main`).
- **Every change to any file here must be committed and pushed to `origin/main` right after you make it**, in the same turn, without asking: `git add -A && git commit -m "<what changed>" && git push`. Check `git status` first so unrelated edits from another session are not lost or overwritten. Never force-push.
- Live domain: ishaandjonathan.com (bought at Spaceship). The published copy carries a noindex tag until launch.
- Fonts in `fonts/` are demo builds (Kaelyna Script, Billa Mount); the full licenses must be bought before guests get the link.
- Use `agent-browser --session <name>` for previews so you do not hijack another session's browser.
- Contact form -> Google Sheet: the form in `index.html` POSTs JSON to a Google Apps Script web app (`FORM_ENDPOINT` in the contact-form block of index.html; empty = preview mode, nothing saved). The script appends one row per submission to the **Contact Form Responses** tab of the "Isha Kenkare & Jonathan Rotbard - 2027" sheet (id `1npn0U1b1h_sD48WdFkuzcZNXpn6EQDYtQUB9mgbsmYE`, tab gid 144044113). Script project (edit/redeploy here): https://script.google.com/d/1MwWODBDuHLV6IogFYhcjPHyZeEtF2p7Ami1q3DxGmwlCt4QROzkKUgfD/edit . Column order in the tab and in the script's `FIELDS` list must match; if a form field is added, add it to both plus the `data` list in the submit handler. Hidden `website` field is a bot honeypot.
