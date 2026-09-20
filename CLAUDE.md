# Isha & Jonathan wedding website

Static site behind a password page. No server, no framework; one small Python build script.

## Layout
- `src/` = **the source. Edit these.** `site.html` (the four-tab shell, Home/Save the Date/Contact/etc.), `save-the-date.html` (envelope page, shown in an iframe on the Save the Date tab), `gate.html` (password page).
- `public/` = **what gets published** (`netlify.toml` sets `publish = "public"`). Holds the shared assets (`img/`, `fonts/`, `audio/`, `cal/`), the password page (`index.html`), `robots.txt`, and two generated folders with 16-character hex names, one per version. **Never edit the generated files by hand.**
- `build.py` generates `public/index.html` and the two version folders from `src/`. Run `python3 build.py` after every change in `src/`, then commit `src/` and `public/` together.
- `slugs.json` = the two hashed folder names (not the passwords). Passwords are never stored anywhere.

## Password page
- `ishaandjonathan.com` shows a password form styled like the Contact Information form. Each password opens its own hidden version folder (the folder name is a hash of the password, so no published file contains the passwords or the folder names).
- Two versions: `both` (July 9 and 10) and `one` (July 10 only). The version is baked into `<body data-version>` at build time. There is no admin/preview switch any more.
- Change the passwords: `python3 build.py --both "new password" --one "new password"`, then commit and push. Passwords are not case sensitive.
- This is a soft gate, not real security: someone who knows a version's folder URL can open it without the password. Keep the URLs private.
- Everything is `noindex` (meta tags, `robots.txt`, `X-Robots-Tag` header).

## Rules
- GitHub is the source of truth: `git pull --rebase` before starting, and **commit and push every change right after making it**, in the same turn, without asking (`git add -A && git commit -m "<what changed>" && git push`). Check `git status` first since another session may be editing; never force-push.
- Repo: https://github.com/jrotbard/ishaandjonathan-website (private, branch `main`). Live domain: ishaandjonathan.com (Spaceship domain, hosted on Netlify).
- The live Netlify site is not yet linked to GitHub (it was uploaded by hand), so pushes do not go live on their own. Once linked (Netlify: Site configuration, Build and deploy, Link repository), every push to `main` publishes.
- Fonts in `public/fonts/` are demo builds (Kaelyna Script, Billa Mount); buy the full licenses (and Ivy Mode) before guests get the link.
- Use `agent-browser --session <name>` for previews so you do not hijack another session's browser. To preview locally: `cd public && python3 -m http.server 8000`.
- Safety net: a background job (`~/Library/LaunchAgents/com.jonathan.wedding-site-sync.plist`, script `~/.claude/tools/wedding-site-sync/sync.sh`, log `~/Library/Logs/wedding-site-sync.log`) commits and pushes any uncommitted change within about a minute. It does not replace committing with a real message right after a change.
