"""Site customisations on top of the reconstruction in site/ (run after tools/build.py).

1. Remove the two hero images on the home page.
2. Push the hero headline down a little (CSS in site/clone.css, section "Customisations").
3. Nav links go to real pages: projects.html, services.html, about.html, contact.html (generated here).
4. Move the "Trusted by Leading Brands" (Clients) section below "Selected Work".

Idempotent: index.html is regenerated from a pristine copy kept in tools/index.pristine.html.
"""
import os, re, shutil
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
PRISTINE = os.path.join(ROOT, 'tools', 'index.pristine.html')
if not os.path.exists(PRISTINE):
    shutil.copy(os.path.join(SITE, 'index.html'), PRISTINE)

CHAR_STYLE = ('display:inline-block;opacity:0.001;transform:translateX(0px) translateY(10px) '
              'scale(1) rotate(0deg) skewX(0deg) skewY(0deg)')
PAGES = {  # file -> (nav anchor, <title>, headline, right-column sections by class, in order)
    'projects.html': ('projects', 'Projects', 'Selected work that demands attention.',
                      ['framer-tq83uc', 'framer-5m3acn']),
    'services.html': ('services', 'Services', 'Services built for brands that want to grow.',
                      ['framer-1tim88w', 'framer-x6rxho']),
    'about.html': ('about', 'About', 'A boutique studio for brand and digital design.',
                   ['framer-r9sjus', 'framer-1tejz2m', 'framer-5m3acn']),
    'contact.html': ('contact', 'Contact', "Let's build something people remember.",
                     ['framer-gq3ulu']),
}
NAV = {v[0]: k for k, v in PAGES.items()}


def headline_html(text):
    words = []
    for w in text.split(' '):
        chars = ''.join(f'<span style="{CHAR_STYLE}">{c}</span>' for c in w)
        words.append(f'<span style="white-space:nowrap">{chars}</span>')
    return ' '.join(words)


def relink(html, prefix):
    """Nav anchors (index#section) -> dedicated pages."""
    for anchor, page in NAV.items():
        html = html.replace(f'href="{prefix}index.html#{anchor}"', f'href="{prefix}{page}"')
    return html


def soup_of(path):
    return BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')


def write(path, soup_or_html):
    open(path, 'w', encoding='utf-8').write(str(soup_or_html))


# ---- home page -------------------------------------------------------------
home = soup_of(PRISTINE)
hero = home.find('section', class_='framer-1azusu0')
hero.find('div', class_='framer-1roipvg', recursive=False).decompose()          # (1)
hero['class'] = hero.get('class', []) + ['rc-hero']                             # (2) hook for CSS
right = home.find('div', class_='framer-yushdo')
clients = right.find('section', class_='framer-5m3acn', recursive=False)
right.find('section', class_='framer-tq83uc', recursive=False).insert_after(clients.extract())  # (4)
home_html = str(home)

# ---- generated section pages ----------------------------------------------
for page, (anchor, title, headline, keep) in PAGES.items():
    s = BeautifulSoup(home_html, 'html.parser')
    s.title.string = f'{title} — Godere®'
    h1 = s.find('section', class_='framer-1azusu0').find('h1')
    h1.clear(); h1.append(BeautifulSoup(headline_html(headline), 'html.parser'))
    col = s.find('div', class_='framer-yushdo')
    sections = {sec['class'][0]: sec for sec in col.find_all('section', recursive=False)}
    for sec in list(sections.values()):
        sec.extract()
    for cls in keep:
        col.append(sections[cls])
    write(os.path.join(SITE, page), relink(str(s), './'))

write(os.path.join(SITE, 'index.html'), relink(home_html, './'))                # (3)

# ---- project detail pages: nav to the new pages ---------------------------
pdir = os.path.join(SITE, 'projects')
for f in os.listdir(pdir):
    p = os.path.join(pdir, f)
    write(p, relink(open(p, encoding='utf-8').read(), '../'))
print('customised:', ', '.join(['index.html', *PAGES]))
