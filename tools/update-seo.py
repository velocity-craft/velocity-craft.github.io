"""Regenerate canonical URLs and the sitemap for the static GitHub Pages site."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://velocitycraft.app'
urls = []
for path in sorted(ROOT.rglob('*.html')):
    if any(p.startswith('.') for p in path.relative_to(ROOT).parts):
        continue
    text = path.read_text()
    rel = path.relative_to(ROOT).as_posix()
    url = ORIGIN + '/' + (rel[:-10] if rel.endswith('index.html') else rel)
    # Language selectors navigate to a real locale page; don't submit them for indexing.
    redirect = 'window.location.replace(' in text or bool(re.search(r'http-equiv=["\']refresh', text, re.I))
    if redirect:
        continue
    if not re.search(r'<link\b[^>]*rel=["\']canonical', text, re.I):
        text = text.replace('</title>', f'</title>\n<link rel="canonical" href="{url}">', 1)
        path.write_text(text)
    if 'mac-testflight/' not in rel and not re.search(r'name=["\']robots["\'][^>]*noindex', text, re.I):
        urls.append(url)
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{escape(u)}</loc></url>\n' for u in urls) + '</urlset>\n')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
print(f'{len(urls)} canonical URLs in sitemap')
