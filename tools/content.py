"""Replace the template copy with Donny Ridwan Setiawan's CV content (run after tools/customize.py).

Only facts stated in the CV are used. Template photos stay as placeholders until real project images exist.
Text is matched on whole text nodes (exact, or by prefix for long paragraphs), so re-running is a no-op.
"""
import os, glob
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
SITE_URL = 'https://donnyridwan.github.io/Porto-2/'
EMAIL = 'halo@donnyridwan.my.id'
LINKEDIN = 'https://www.linkedin.com/in/donnyrs/'
NAME = 'Donny Ridwan'
TITLE = 'Donny Ridwan Setiawan — Senior UI/UX & Product Designer'
DESCRIPTION = ('Senior UI/UX and Product Designer with 4+ years of experience helping SaaS, fintech and '
               'e-commerce products convert. Research, prototyping, design systems and launch on WordPress or Shopify.')
CHAR_STYLE = ('display:inline-block;opacity:0.001;transform:translateX(0px) translateY(10px) '
              'scale(1) rotate(0deg) skewX(0deg) skewY(0deg)')

# old slug -> (new slug, title, card category, client, year, industry, result, description)
PROJECTS = {
    'arcveil-brand-identity': ('saas-platform-redesign', 'SaaS Platform — End-to-End UX Redesign', 'SaaS / Product Design',
        'Gandaria Studio', '2024 – Present', 'SaaS', '+20% user retention',
        'An end-to-end UX redesign of a SaaS platform. I found where users got stuck, reworked the core flows, and '
        'prototyped and tested the fixes in Figma before handoff — lifting user retention by 20% and task completion by 15%.'),
    'lumio-product-design': ('fintech-mobile-app', 'Fintech Mobile App — Design & Prototyping', 'Fintech / Mobile App',
        'Gandaria Studio', '2024 – Present', 'Fintech', '+30% app downloads',
        'Designed and prototyped a fintech mobile app, then iterated on it with user feedback. Each round of changes '
        'removed friction from the experience, and the feedback-driven iterations drove a 30% increase in downloads.'),
    'vela-brand-identity': ('event-tracking-app', 'Event Tracking App — F1 Event & Hajj 2025', 'Events / Mobile App',
        'Tappifyd, Jeddah', '2024 – 2026', 'Events & Operations', 'Used at Hajj 2025',
        'Led product design of a participant-tracking app for an F1-related event, which was later used during Hajj 2025. '
        'I turned complex operational requirements into user flows, wireframes, prototypes and production-ready UI.'),
    'kova-creative-direction': ('ecommerce-conversion', 'E-Commerce — Conversion Rate Optimization', 'E-Commerce / CRO',
        'Gandaria Studio', '2024 – Present', 'E-Commerce', '+25% conversion rate',
        'Worked with engineering and marketing on CRO-focused UX changes for an e-commerce platform: clearer hierarchy, '
        'stronger calls to action and simpler navigation. The result was a 25% increase in conversion rate.'),
    'haux-web-redesign': ('b2b-platform', 'Multi-Sector B2B Platform — MVP Redesign', 'B2B / SaaS',
        'Tappifyd, Jeddah', '2024 – 2026', 'Healthcare, Hospitality & More', 'MVP to multi-sector platform',
        'Redesigned an MVP into a multi-sector B2B platform for hospitals, hotels and other industries, with reusable UI '
        'patterns, components and responsive standards that hold up across very different workflows.'),
}
OLD_TITLES = {'arcveil-brand-identity': 'Arcveil — Brand Identity & Web', 'lumio-product-design': 'Lumio — Product Design & Strategy',
              'vela-brand-identity': 'Vela — Brand Identity & Go-to-Market', 'kova-creative-direction': 'Kova — Creative Direction & Campaign',
              'haux-web-redesign': 'Haux — Web Redesign & Digital Strategy'}
OLD_CATS = {'arcveil-brand-identity': 'SaaS / Technology', 'lumio-product-design': 'Fintech / Finance',
            'vela-brand-identity': 'Health Tech / Wellness', 'kova-creative-direction': 'E-Commerce / Lifestyle'}

# Text shared by all pages: (old text, new text, match by prefix?)
TEXT = [
    ('Godere®', NAME, False),
    ('We craft brands and digital experiences that demand attention.', 'I design SaaS, fintech & e-commerce products that convert.', False),
    ("Great design isn't decoration", 'Senior UI/UX & Product Designer with 4+ years of experience. I find where users get stuck or '
     'drop off, then research, prototype and test the fix — and ship it with a design system developers can actually use.', True),
    ('From brand transformations to performance-driven', 'Recent work across SaaS, fintech, e-commerce and events — each one '
     'researched, prototyped, tested and shipped with measurable results.', True),
    ('Clients', 'Experience', False),
    ('Trusted by Leading Brands', "Teams I've Worked With", False),
    ('How We Work', 'How I Work', False),
    ('Our process is built for clarity', 'I start where users get stuck or drop off, then research, wireframe, prototype and test '
     'the fix in Figma — and hand over a design system developers can actually use.', True),
    ('Goals, Scope and Direction', 'Find Where Users Drop Off', False),
    ('Project Kickoff', 'UX & CRO Audit', False),
    ('Design and Prototyping Process', 'Research, Wireframe & Prototype', False),
    ('Design Process', 'Design in Figma', False),
    ('Polish and Quality Control', 'Test, Systemize & Ship', False),
    ('Testing', 'Launch', False),
    ('What We Offer', 'What I Offer', False),
    ('From identity to interface', 'From conversion-focused websites to SaaS dashboards and B2B platforms — every project ships '
     'with organized Figma handoff and a design system developers can use.', True),
    ('Web Design & Development', 'Website Design & Development', False),
    ('Custom websites built to perform', 'Responsive marketing sites and landing pages, taken live on WordPress or Shopify with '
     'AI-assisted development.', True),
    ('Creative Direction', 'Conversion Rate Optimization', False),
    ('Art directing campaigns', 'UX and CRO audits turned into clearer hierarchy, stronger CTAs and simpler navigation.', True),
    ('Brand Identity', 'UI/UX & Product Design', False),
    ('Logos, typography, colour systems', 'User flows, wireframes, prototypes and high-fidelity UI for SaaS, B2B platforms and apps.', True),
    ('Strategy & Concepts', 'Figma Design Systems', False),
    ('We define your positioning', 'Components, variants and auto layout that keep products consistent and speed up handoff.', True),
    ('Digital Product Design', 'SEO & Web Accessibility', False),
    ('UI/UX design for SaaS, apps, and dashboards', 'SEO-aware, mobile-first layouts built to WCAG standards and checked with '
     'responsive QA.', True),
    ('About Us', 'About Me', False),
    ('Built on Craft. Driven by Impact.', 'Designing for Results, Not Decoration.', False),
    ('We are a boutique creative studio', "I'm Donny Ridwan Setiawan, a Senior UI/UX and Product Designer from Indonesia with a "
     'Computer Engineering degree from Diponegoro University. I work remotely with teams in Indonesia, the Philippines, '
     'Australia, Saudi Arabia and the UAE.', True),
    ('Testimonials', 'Highlights', False),
    ('Words From Our Clients', 'Results & Recognition', False),
    ('We measure success by the impact', 'A few numbers I am proud of, from freelance work on Upwork to design shots that '
     'brought in international clients.', True),
    ('Liam Carter', 'Upwork', False),
    ('Head of Product, Arcveil', 'Top Rated · 100% Job Success', False),
    ('They asked the right questions', '60+ contracts and 1,200+ hours delivered across website design, landing pages, SaaS, '
     'e-commerce, mobile app and CRO projects.', True),
    ('Sofia Reyes', 'Dribbble', False),
    ('Founder & CEO, Lumio', 'Aksantara Digital', False),
    ('Our new website has completely changed', 'A Dribbble shot that reached 20,000 impressions and 150 likes, bringing inbound '
     'inquiries from international clients.', True),
    ('Have a project in mind', "Have a product that isn't converting, or a design that needs to go live? Drop me a line — "
     "I'd love to hear what you're working on and see how I can help.", True),
    ('hello@godere.com', EMAIL, False),
    ('X (Twitter)', 'LinkedIn', False),
    ('Godera® - All rights reserved.', '© 2026 Donny Ridwan Setiawan. All rights reserved.', False),
    ('Live Preview', "Let's Talk", False),
    # generated section pages (tools/customize.py)
    ('Selected work that demands attention.', 'Selected work with measurable results.', False),
    ('Services built for brands that want to grow.', 'Design that converts, systems that scale.', False),
    ('A boutique studio for brand and digital design.', 'Senior UI/UX & Product Designer.', False),
    ("Let's build something people remember.", "Let's fix where your users drop off.", False),
]
for old, (_, title, cat, *_r) in PROJECTS.items():
    TEXT.append((OLD_TITLES[old], title, False))
    if old in OLD_CATS:
        TEXT.append((OLD_CATS[old], cat, False))
CLIENT_LOGOS = ['Gandaria Studio', 'Upwork', 'Tappifyd', 'Aksantara Digital', 'Tupai Tech', 'Diponegoro University']
SUBPAGE_TITLES = {'projects.html': 'Projects', 'services.html': 'Services', 'about.html': 'About', 'contact.html': 'Contact'}


def headline(soup, text):
    frag = ' '.join('<span style="white-space:nowrap">' + ''.join(f'<span style="{CHAR_STYLE}">{c}</span>' for c in w) + '</span>'
                    for w in text.split(' '))
    return BeautifulSoup(frag, 'html.parser')


def replace_text(soup, pairs):
    # char-split headlines first (h1 whose joined text matches)
    for h in soup.find_all('h1'):
        if h.find('span'):
            joined = h.get_text()
            for old, new, prefix in pairs:
                if joined == old or (prefix and joined.startswith(old)):
                    h.clear(); h.append(headline(soup, new)); break
    for node in list(soup.find_all(string=True)):
        if node.parent.name in ('style', 'script'):
            continue
        t = node.strip()
        if not t:
            continue
        for old, new, prefix in pairs:
            if t == old or (prefix and t.startswith(old)):
                node.replace_with(node.replace(t, new)); break


def apply(path, extra_pairs=(), depth=0):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    up = '../' * depth
    replace_text(soup, list(extra_pairs) + TEXT)
    # head
    page = os.path.basename(path)
    page_url = SITE_URL + ('' if page == 'index.html' else ('projects/' if depth else '') + page)
    for l in soup.find_all('link', rel='canonical'):
        l['href'] = page_url
    if soup.title:
        t = soup.title.string or ''
        if depth == 0 and page == 'index.html':
            soup.title.string = TITLE
        elif depth == 0 and page in SUBPAGE_TITLES:
            soup.title.string = f'{SUBPAGE_TITLES[page]} — {NAME}'
        elif ' - Godere®' in t:
            soup.title.string = t.replace(' - Godere®', f' — {NAME}')
    for m in soup.head.find_all('meta'):
        key = m.get('name') or m.get('property')
        if key in ('description', 'og:description', 'twitter:description'): m['content'] = DESCRIPTION
        if key in ('og:title', 'twitter:title'): m['content'] = soup.title.string
        if key == 'og:url': m['content'] = page_url
    # links
    for a in soup.find_all('a', href=True):
        if a.decomposed or a.attrs is None:
            continue
        h = a['href']
        if h == f'mailto:hello@godere.com': a['href'] = f'mailto:{EMAIL}'
        elif h.startswith('https://x.com'): a['href'] = LINKEDIN; a['target'] = '_blank'; a['rel'] = 'noopener'
        elif h.startswith('https://dribbble.com'):
            a['href'] = f'mailto:{EMAIL}'; a.attrs.pop('target', None)
            for n in a.find_all(string=lambda x: x and x.strip() == 'Dribbble'): n.replace_with('Email')
        elif h.startswith('https://instagram.com'):
            a.decompose(); continue
        elif h == 'https://framer.com/@zain' and "Let's Talk" in a.get_text(): a['href'] = f'{up}contact.html'; a.attrs.pop('target', None)
        for old, (new, *_r) in PROJECTS.items():
            if old in a['href']: a['href'] = a['href'].replace(old, new)
    for el in soup.find_all(attrs={'data-framer-hydrate-v2': True}):
        del el['data-framer-hydrate-v2']   # Framer runtime metadata (unused, names template routes)
    # SVG symbols the Framer runtime normally injects (section-label arrow, stars, play button)
    if not soup.find(id='rc-svg-symbols'):
        sym = open(os.path.join(ROOT, 'tools', 'svg-symbols.html'), encoding='utf-8').read().split('\n', 1)[1]
        soup.body.insert(0, BeautifulSoup(sym, 'html.parser'))
    # leftover hidden Framer badge
    for a in soup.select('a.__framer-badge'):
        (a.find_parent('div', id='__framer-badge-container') or a).decompose()
    # client logos -> names (text tiles)
    for i, wrap in enumerate(soup.find_all('div', attrs={'data-framer-name': 'Logo Wrapper'})):
        wrap.clear()
        wrap['class'] = wrap.get('class', []) + ['rc-logo-text']
        span = soup.new_tag('span'); span.string = CLIENT_LOGOS[i % len(CLIENT_LOGOS)]; wrap.append(span)
    # highlights cards: monogram instead of stock portraits; no star rating on the Dribbble card
    for card in soup.find_all('div', attrs={'data-framer-name': 'Avatar'}):
        comp = card.find_parent('div', class_='framer-EeCDC')
        name_el = comp.find(class_='framer-1ip446m') if comp else None
        letter = 'U' if name_el and 'Upwork' in name_el.get_text() else 'D'
        card.clear(); card['class'] = [c for c in card.get('class', []) if c != 'rc-monogram'] + ['rc-monogram']
        span = soup.new_tag('span'); span.string = letter; card.append(span)
        if letter == 'D' and comp:
            stars = comp.find('div', attrs={'data-framer-name': 'Stars'})
            if stars and 'rc-hidden' not in stars.get('class', []): stars['class'] = stars.get('class', []) + ['rc-hidden']
    open(path, 'w', encoding='utf-8').write(str(soup))


for page in ['index.html', *SUBPAGE_TITLES]:
    apply(os.path.join(SITE, page))

pdir = os.path.join(SITE, 'projects')
for old, (new, title, cat, client, year, industry, result, desc) in PROJECTS.items():
    src, dst = os.path.join(pdir, f'{old}.html'), os.path.join(pdir, f'{new}.html')
    if os.path.exists(src):
        os.replace(src, dst)
    soup = BeautifulSoup(open(dst, encoding='utf-8').read(), 'html.parser')
    ps = [p for p in soup.find_all('p')]
    labels = [p.get_text() for p in ps]
    if 'Timeline' in labels or 'Result' in labels:
        i = labels.index('Client')
        for j, val in zip(range(i, i + 8), ['Client', client, 'Year', year, 'Industry', industry, 'Result', result]):
            ps[j].string = val
    long_p = [p for p in ps if len(p.get_text()) > 80 and p.get_text() not in (desc,)]
    for p in long_p[:1]:
        if not p.get_text().startswith(('Senior UI/UX',)):
            p.string = desc
    soup.title.string = f'{title} — {NAME}'
    open(dst, 'w', encoding='utf-8').write(str(soup))
    apply(dst, depth=1)
print('content applied')
