# Isha & Jonathan wedding website

Static site behind a password page. No server, no framework; one small Python build script.

## Layout
- `src/` = **the source. Edit these.** `site.html` (the four-tab shell, Home/Save the Date/Contact/etc.), `save-the-date.html` (envelope page, shown in an iframe on the Save the Date tab), `gate.html` (password page).
- `public/` = **what gets published** (Cloudflare Pages output directory = `public`; `netlify.toml` is legacy). Holds the shared assets (`img/`, `fonts/`, `audio/`, `cal/`), the password page (`index.html`), `robots.txt`, `_headers` (noindex header for Cloudflare Pages, written by `build.py`), and generated folders with 16-character hex names, one per version. **Never edit the generated files by hand.**
- `build.py` generates `public/index.html` and the two version folders from `src/`. Run `python3 build.py` after every change in `src/`, then commit `src/` and `public/` together.
- `slugs.json` = the two hashed folder names (not the passwords). Passwords are never stored anywhere.

## Password page
- `ishaandjonathan.com` shows a password form styled like the Contact Information form. Each password opens its own hidden version folder (the folder name is a hash of the password, so no published file contains the passwords or the folder names).
- Three versions: `both` (July 9 and 10), `one` (July 10 only) and `may` (identical to `one` but with May 14, 2027 as the date, countdown and calendar files). The version is baked into `<body data-version>` at build time. There is no admin/preview switch any more. Both passwords and all three open the Save the Date tab.
- Version data (date text, countdown target, Google/Apple calendar) lives in the `VERSIONS` map in `src/save-the-date.html`; calendar files are in `public/cal/`.
- Change the passwords: `python3 build.py --both "new" --one "new" --may "new"` (any subset), then commit and push. Passwords are not case sensitive.
- This is a soft gate, not real security: someone who knows a version's folder URL can open it without the password. Keep the URLs private.
- Everything is `noindex` (meta tags, `robots.txt`, `X-Robots-Tag` header).

## Rules
- GitHub is the source of truth: `git pull --rebase` before starting, and **commit and push every change right after making it**, in the same turn, without asking (`git add -A && git commit -m "<what changed>" && git push`). Check `git status` first since another session may be editing; never force-push.
- Repo: https://github.com/jrotbard/ishaandjonathan-website (private, branch `main`). Live domain: ishaandjonathan.com (Spaceship domain). Hosted on Cloudflare (Workers static assets, free, no per-deploy credits) since 2026-09-28, after Netlify's free credits ran out. Config is `wrangler.jsonc` (serves `public/`, custom domains ishaandjonathan.com and www). DNS zone is in Cloudflare (nameservers davina/kyree.ns.cloudflare.com); Spaceship is registrar only. **To publish: `python3 build.py`, commit, push, then `npx wrangler deploy` (pushing to GitHub does NOT deploy).** wrangler login is an OAuth token stored in ~/Library/Preferences/.wrangler.
- Pushing does not deploy, so pushes are free. Netlify (old host) is no longer used; unlink or delete that site.
- Fonts in `public/fonts/` are demo builds (Kaelyna Script, Billa Mount); buy the full licenses (and Ivy Mode) before guests get the link.
- Use `agent-browser --session <name>` for previews so you do not hijack another session's browser. To preview locally: `cd public && python3 -m http.server 8000`.
- The auto-sync launchd job (`com.jonathan.wedding-site-sync`) was turned off on 2026-09-27 because a push every 60s meant a deploy every 60s. Plist and script are still on disk; re-enable only with a much longer interval.
