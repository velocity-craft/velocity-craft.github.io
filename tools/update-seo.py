"""Generate canonical URLs and localized sitemap entries for GitHub Pages."""

from collections import defaultdict
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://velocitycraft.app'
SITEMAP = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XHTML = 'http://www.w3.org/1999/xhtml'
DOCUMENTS = {'privacy', 'terms', 'support', 'delete-account', 'delete-data'}
CANONICAL = re.compile(r'<link\b[^>]*rel=["\']canonical["\']', re.I)


def url_for(path):
    relative = path.relative_to(ROOT).as_posix()
    if path.name == 'index.html':
        relative = relative.removesuffix('index.html')
    return f'{ORIGIN}/{relative}'


def add_canonical(path, html, url):
    if not CANONICAL.search(html):
        path.write_text(html.replace('</title>', f'</title>\n<link rel="canonical" href="{url}">', 1))


pages = {}
translations = defaultdict(dict)
for path in sorted(ROOT.rglob('*.html')):
    if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
        continue
    html = path.read_text()
    redirect = 'window.location.replace(' in html or re.search(r'http-equiv=["\']refresh', html, re.I)
    if redirect:
        # Locale routers retain the user's browser-language choice. The default
        # English destination is the canonical; the router is not a sitemap URL.
        english = path.with_name('en.html')
        if path.name == 'index.html' and "var target = 'en'" in html and english.is_file():
            add_canonical(path, html, url_for(english))
        continue
    url = url_for(path)
    add_canonical(path, html, url)
    if 'mac-testflight' in path.parts or re.search(r'name=["\']robots["\'][^>]*noindex', html, re.I):
        continue
    pages[path] = url
    if path.parent.name in DOCUMENTS:
        lang = re.search(r'<html\s+lang=["\']([^"\']+)', html, re.I).group(1)
        family = translations[path.parent]
        if lang in family:
            raise ValueError(f'Duplicate locale {lang} in {path.parent}')
        family[lang] = url

ET.register_namespace('', SITEMAP)
ET.register_namespace('xhtml', XHTML)
urlset = ET.Element(f'{{{SITEMAP}}}urlset')
for path, url in pages.items():
    entry = ET.SubElement(urlset, f'{{{SITEMAP}}}url')
    ET.SubElement(entry, f'{{{SITEMAP}}}loc').text = url
    family = translations.get(path.parent, {})
    if len(family) > 1:
        for lang, href in sorted(family.items()):
            ET.SubElement(entry, f'{{{XHTML}}}link', rel='alternate', hreflang=lang, href=href)
        if 'en' in family:
            ET.SubElement(entry, f'{{{XHTML}}}link', rel='alternate', hreflang='x-default', href=family['en'])

ET.indent(urlset, space='  ')
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding='unicode') + '\n')
(ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
print(f'{len(pages)} canonical URLs in sitemap')
