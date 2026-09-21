#!/usr/bin/env python3
"""Builds the website into public/ from the templates in src/.

  python3 build.py                          rebuild everything, keeping the current passwords
  python3 build.py --both "pw1" --one "pw2" --may "pw3"   change the passwords, then rebuild

public/index.html is the password page. Each password opens its own hidden folder, named after a
hash of the password, so neither the passwords nor the folder names appear in any published file:
  --both  -> the July 9 & 10 version
  --one   -> the July 10 only version
  --may   -> the May 14 version (same as July 10 only, with May 14, 2027 as the date)
Only the hashed folder names are stored (slugs.json). The passwords themselves are never written
to disk. Passwords are not case sensitive and ignore spaces at the ends.

Edit the files in src/ (never the generated folders in public/), then run this script and commit.
"""
import argparse, hashlib, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC, PUB, SLUGS = ROOT / 'src', ROOT / 'public', ROOT / 'slugs.json'
SALT = 'ishaandjonathan|'          # must match SALT in src/gate.html
VERSIONS = {'both': 'July 9 & 10', 'one': 'July 10 only', 'may': 'May 14'}
NOINDEX = '<meta name="robots" content="noindex, nofollow">\n'
MARKER = '<meta name="invite-site" content="1">\n'   # the password page looks for this to confirm a folder is real
# Shared assets live one level up from a version folder. Only real file paths are rewritten (they end in .ext), so MIME types such as type="audio/wav" are left alone.
ASSET = re.compile(r'(?<![\w/.\-])(img|fonts|audio|cal)/(?=[\w\-]+\.[A-Za-z0-9]{2,5}\b)')


def slug(password):
    return hashlib.sha256((SALT + password.strip().lower()).encode('utf-8')).hexdigest()[:16]


def with_head(html, extra):
    assert html.count('<head>') == 1
    return html.replace('<head>', '<head>\n' + extra, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--both', help='password for the July 9 & 10 version')
    ap.add_argument('--one', help='password for the July 10 only version')
    ap.add_argument('--may', help='password for the May 14 version')
    a = ap.parse_args()

    slugs = json.loads(SLUGS.read_text()) if SLUGS.exists() else {}
    for key, pw in (('both', a.both), ('one', a.one), ('may', a.may)):
        if pw is not None:
            if not pw.strip():
                sys.exit('empty password for --%s' % key)
            slugs[key] = slug(pw)
    if set(slugs) != set(VERSIONS):
        sys.exit('missing passwords: run  python3 build.py --both "..." --one "..." --may "..."')
    if len(set(slugs.values())) != len(slugs):
        sys.exit('the passwords must all be different')
    SLUGS.write_text(json.dumps(slugs, indent=2) + '\n')

    for d in PUB.iterdir():                        # clear old generated version folders
        if d.is_dir() and re.fullmatch(r'[0-9a-f]{16}', d.name):
            shutil.rmtree(d)

    for key, folder in slugs.items():
        out = PUB / folder
        out.mkdir()
        for name, extra in (('site.html', NOINDEX + MARKER), ('save-the-date.html', NOINDEX)):
            html = (SRC / name).read_text().replace('{{VERSION}}', key)
            html = ASSET.sub(r'../\1/', html)
            (out / ('index.html' if name == 'site.html' else name)).write_text(with_head(html, extra))
        print('%-4s (%s) -> public/%s/' % (key, VERSIONS[key], folder))

    (PUB / 'index.html').write_text(with_head((SRC / 'gate.html').read_text(), NOINDEX))
    (PUB / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    print('password page -> public/index.html')


if __name__ == '__main__':
    main()
