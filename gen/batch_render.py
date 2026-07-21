#!/usr/bin/env python3
"""2060 Settlement Atlas — batch entry renderer (design instance, v1 · 2026-07-14).

Renders EVERY R-region in the newest workbook to entries/<RegionID>.html for the
cartographer's map click-through. Requires no hand-authored content files: the
artisanal layer is synthesized (FPO hero, FPO photos, auto title/eyebrow). Where a
real content file exists in content/, it is used instead (currently 5 regions).

Interface with the cartographer (ID-keyed, per house convention):
  centroids.json — optional, {"R042": [lat, lon], ...}. If present, the locator
  crosshair is placed via the locked marker transform. Regions absent from the
  file render the locator map without a crosshair (coord label suppressed).
  The cartographer generates this in one pass from their assignment geometry.

Run:  python3 batch_render.py [outdir]           (default outdir: ./entries)
Then: open entries/index.html for the contact sheet.

Fonts: entry pages reference ../fonts/ RELATIVELY (rewritten from the template's
absolute paths) so the bundle is portable: keep entries/ and fonts/ siblings.
"""
import os, sys, re, json, glob, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_gen as G

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entries')
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

# ---- FPO photo: an inline SVG data-URI so <img> needs no file and prints fine ----
def fpo_photo_uri(label):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420">'
           f'<rect width="100%" height="100%" fill="#EFE8D8"/>'
           f'<rect x="6" y="6" width="628" height="408" fill="none" stroke="#166450" '
           f'stroke-width="4" stroke-dasharray="14 10"/>'
           f'<text x="50%" y="46%" text-anchor="middle" font-family="sans-serif" '
           f'font-size="26" letter-spacing="4" fill="#166450">PHOTO · FPO</text>'
           f'<text x="50%" y="58%" text-anchor="middle" font-family="sans-serif" '
           f'font-size="17" fill="#3D3A33">{html.escape(label)}</text></svg>')
    return 'data:image/svg+xml;utf8,' + svg.replace('#', '%23').replace('"', "'")

# ---- centroids (optional, cartographer-supplied) ----
CENTROIDS = {}
cpath = os.path.join(HERE, 'centroids.json')
if os.path.exists(cpath):
    CENTROIDS = {k: v for k, v in json.load(cpath and open(cpath)).items() if not k.startswith('_')}

def marker_for(rid):
    """Locked transform from the template spec. No centroid → no crosshair."""
    if rid in CENTROIDS:
        lat, lon = CENTROIDS[rid]
        return (2.1836 * lon + 405.49, -2.5649 * lat + 510.44,
                f'{abs(lat):.0f}°{"N" if lat >= 0 else "S"}&thinsp;·&thinsp;{abs(lon):.0f}°{"E" if lon >= 0 else "W"}')
    return None

# ---- hand-authored content files take precedence (ID-keyed scan, never by filename) ----
import importlib.util
HAND = {}
for p in glob.glob(os.path.join(HERE, 'content', '*.py')):
    spec = importlib.util.spec_from_file_location('c_' + os.path.basename(p)[:-3], p)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        HAND[mod.CONTENT['region_id']] = mod.CONTENT
    except Exception as e:
        print(f'  [skip content file {os.path.basename(p)}: {e}]')

def auto_content(r):
    """Synthesize the artisanal layer from the workbook row. FPO throughout."""
    rid = r[56]
    name = str(r[1] or rid).strip()
    m = re.match(r'([^(]+?)\s*\((.*)\)\s*$', name)
    title, qual = (m.group(1).strip(), m.group(2).strip()) if m else (name, '')
    continent = str(r[2] or '').strip()
    eyebrow = ' · '.join(x for x in (continent, qual) if x) or continent or '—'
    mk = marker_for(rid)
    return {
        'region_id': rid, 'title': html.escape(title), 'eyebrow': html.escape(eyebrow),
        'hero_note': f'Hero illustration TK — {html.escape(title)}. Depiction note to be supplied.',
        'hero_caption': (html.escape(title), continent or '—'),
        'marker': mk if mk else (-999, -999, '—'),      # off-canvas when unknown
        'photos': [(fpo_photo_uri(f'{rid} · {title} — photo 1'), 'Caption TK'),
                   (fpo_photo_uri(f'{rid} · {title} — photo 2'), 'Caption TK')],
    }

# ---- run ----
ws = G.load_workbook(G.WB, read_only=True, data_only=True)['Region Catalog']
rows = [r for r in list(ws.iter_rows(values_only=True))[1:] if r[56]]
ok, fell_back, failed = [], [], []
for r in rows:
    rid = r[56]
    c = HAND.get(rid) or auto_content(r)
    try:
        page = G.render(r, c)
        # portable fonts: absolute /home/claude/fonts/static/ → ../fonts/
        page = page.replace('file:///home/claude/fonts/static/', '../fonts/') \
                   .replace('/home/claude/fonts/static/', '../fonts/')
        open(os.path.join(OUT, f'{rid}.html'), 'w').write(page)
        (ok if G.cw_prose(r) else fell_back).append(rid)
    except Exception as e:
        failed.append((rid, str(e)))
        print(f'  FAIL {rid}: {e}')

# ---- X/W zone pages (exclusion & wildland records) ----
import exclusion_gen as XG
xz, wz, led = XG.load_zones()
zone_names = {r[0]: str(r[1]).strip() for r in xz + wz}
xw_ok, xw_failed = [], []
for zr, kind in [(z, 'X') for z in xz] + [(z, 'W') for z in wz]:
    zid = zr[0]
    mk = None
    if zid in CENTROIDS:
        lat, lon = CENTROIDS[zid]
        mk = (2.1836 * lon + 405.49, -2.5649 * lat + 510.44)
    try:
        page = XG.render_zone(zr, kind, led.get(zid), centroid=mk)
        page = page.replace('file:///home/claude/fonts/static/', '../fonts/') \
                   .replace('/home/claude/fonts/static/', '../fonts/')
        open(os.path.join(OUT, f'{zid}.html'), 'w').write(page)
        xw_ok.append(zid)
    except Exception as e:
        xw_failed.append((zid, str(e))); print(f'  FAIL {zid}: {e}')

# ---- contact sheet ----
name_of = {x[56]: x[1] for x in rows}; name_of.update(zone_names)
def li(ids):
    return ''.join(f'<li><a href="{i}.html"><strong>{i}</strong> — '
                   f'{html.escape(str(name_of[i]))}</a></li>' for i in sorted(ids))
open(os.path.join(OUT, 'index.html'), 'w').write(
    f'<!doctype html><meta charset="utf-8"><title>Atlas entries — contact sheet</title>'
    f'<body style="font-family:Georgia,serif;max-width:52em;margin:2em auto;background:#EFE8D8;'
    f'color:#2B2A26"><h1>2060 Settlement Atlas — rendered pages</h1>'
    f'<p>{len(ok)+len(fell_back)} settlement entries + {len(xw_ok)} exclusion/wildland records · '
    f'workbook {os.path.basename(G.WB)} · '
    f'centroids: {"supplied" if CENTROIDS else "NOT supplied (no locator crosshairs)"} · '
    f'heroes &amp; photos FPO by design</p>'
    f'<h2>Settlement regions (R)</h2><ol>{li(ok + fell_back)}</ol>'
    f'<h2>Exclusion records (X)</h2><ol>{li([z for z in xw_ok if z.startswith("X")])}</ol>'
    f'<h2>Wildland records (W)</h2><ol>{li([z for z in xw_ok if z.startswith("W")])}</ol></body>')

print(f'[batch_render] {len(ok)} CW-prose entries + {len(fell_back)} content-fallback '
      f'+ {len(xw_ok)} X/W records + {len(failed) + len(xw_failed)} failed → {OUT}')
if fell_back: print('  fallback-prose regions:', ', '.join(fell_back))
if CENTROIDS: print(f'  crosshairs placed for {sum(1 for x in ok+fell_back if x in CENTROIDS)} regions')
else: print('  NOTE: drop a centroids.json next to this script to light up the locator markers')
