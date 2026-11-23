# Godere — static reconstruction

Static, script-free reconstruction of https://godere.framer.website (home + 5 project pages), built with the
[Replica](https://github.com/sukirman1901/replica) workflow and measured against the live site.

## Run

```sh
node tools/serve.mjs site 3000      # clean URLs, like the original (/projects/vela-brand-identity)
```

`site/` is plain HTML/CSS/assets and can also be deployed to any static host (links point at `*.html`).

## Layout

| Path | What |
| --- | --- |
| `site/` | The clone: 6 pages, 170 local assets (fonts + AVIF/WebP images), `clone.css`, `clone.js`, `vendor/lenis` |
| `ref/` | Captured server-rendered HTML of the reference |
| `tools/content.py` | CV content (see Content) |
| `tools/customize.py` | Applies the customisations above |
| `tools/build.py` | Rebuilds `site/` from `ref/`: strips Framer runtime scripts and badge, localises every asset (manifest with SHA-256 in `site/assets/manifest.json`) |
| `tools/capture-playwright.cjs` | Playwright adapter writing Replica's `captures.json` evidence contract (Una CLI was not available) |
| `tools/checks-playwright.cjs` | Behaviour checks run against both sites, writing `checks.json` receipts |
| `project.json` | Replica scope: 6 routes × 390/1024/1440 viewports, 4 required checks |
| `runs/run-007/` | Final evidence: screenshots, diffs, `comparison.json`, `report.md` |

## Customisations (on top of the reconstruction)

`tools/customize.py` (run after `tools/build.py`; idempotent, keeps the untouched home page in `tools/index.pristine.html`):

* Home hero images removed; headline sits a little lower (CSS in `site/clone.css`, "Customisations").
* "Trusted by Leading Brands" moved below "Selected Work".
* Nav links open real pages instead of scrolling: `projects.html`, `services.html`, `about.html`, `contact.html`
  (generated from the home layout with their own headline and sections). Also used by project pages and "Let's Talk".
* Mobile hamburger menu works (full-height menu, cross icon), matching the original's behaviour.

## Content

`tools/content.py` (run after `tools/customize.py`) replaces the template copy with Donny Ridwan Setiawan's CV:
hero, projects (5 case studies with new slugs), experience, process, services, about, highlights, contact, footer,
titles/meta/canonical URLs. Only CV facts are used; the template photos remain as placeholders for real project images.
It also restores three SVG icons Framer injects at runtime (`tools/svg-symbols.html`: section-label arrow, stars, play).

Full rebuild: `python3 tools/build.py && python3 tools/customize.py && python3 tools/content.py`

## Publish

GitHub Pages serves the `gh-pages` branch, which holds a copy of `site/`: https://donnyridwan.github.io/Porto-2/

## What replaces the Framer runtime

* `clone.js`: scroll-triggered appear animations (per-character headline reveal, fade-up blocks, image zoom-out from
  `scale(1.2)`), leaving the same final inline state as Framer; nav-link bracket hover; Lenis smooth scrolling.
* Lenis 1.3.23 (same version the original loads) vendored under `site/vendor/`.

## Fidelity (run-007, Replica report status: MEASURED — no acceptance thresholds were set)

* Coverage 18/18 visual cases, 4/4 behaviour checks PASS on both reference and clone
  (nav hover pulse, anchor scroll to #services, project link navigation, normal-motion headline reveal).
* Perceptual match (pixelmatch 0.1): 99.54–99.93 % per case. Page heights identical in all 18 cases.
* Exact RGBA match: 78.9–99.8 % per case. The remainder is photo rasterisation noise (the reference
  measured against itself gave 99.35 % exact on one page) and the intentionally removed "Made in Framer" badge.

Not reproduced: Framer's client-side page transitions (the clone does normal page loads), the Framer
editor bar and analytics. Contact/"Let's Talk" links behave as on the original (mailto/anchors); there is no backend.

Content, imagery and the "Godere" design belong to the template author (Zain Malik / Framer template) —
make sure you hold a licence before publishing this as your own site.
