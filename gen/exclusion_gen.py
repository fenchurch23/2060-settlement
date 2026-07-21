#!/usr/bin/env python3
"""2060 Settlement Atlas — X/W zone page generator ("exclusion & wildland records").
Companion species to the R-entry template (v1.1): same paper, fonts, and furniture;
different register. x1.0 (2026-07-14).

Data: 'Exclusion Zones' / 'Wildland Zones' sheets (copywriter's 8-block pages,
calibration_v1 spec) + 'Exclusion Ledger' sheet (city → absorbed-by, ID-keyed).
X pages carry a LEDGER OF LEAVING table; each absorbed-by cell links to the
absorbing R-region's entry page (RNNN.html) for the map click-through web.

Page grounds carry the register (authorized 2026-07-14):
  X  — THE LOST WORLDS: near-black night ground, text/colors reversed out, red accents.
  W-hostile — harsh concrete-gray ground, ink text (the planet's terms).
  W-wild    — the living cream paper, spruce accents (the covenant pair).
Heroes & photos are FPO by design; photo depiction notes come from the Captions col.
Coda foot lines are pure series labels, not new voice. No personal names in output.
"""
EXCL_VERSION = "x1.1 (2026-07-14: X pages dark-reversed + renamed THE LOST WORLDS; W-hostile pages harsh gray; W-wild keeps paper; personal references scrubbed from FPO notes)"
import re, os, json, html
from atlas_gen import WB, leadin, load_workbook

FONT_BASE = '/home/claude/fonts/static/'
_DIR = os.path.dirname(os.path.abspath(__file__))
WORLDMAP = open(os.path.join(_DIR, 'worldmap_inner.svg')).read()

def load_zones():
    wb = load_workbook(WB, read_only=True, data_only=True)
    xz = [r for r in list(wb['Exclusion Zones'].iter_rows(values_only=True))[1:] if r[0]]
    wz = [r for r in list(wb['Wildland Zones'].iter_rows(values_only=True))[1:] if r[0]]
    led = {}
    for r in list(wb['Exclusion Ledger'].iter_rows(values_only=True))[1:]:
        if r[0] and str(r[0]).startswith('X'):
            led.setdefault(r[0], []).append(r)   # (zone, city, peakM, abs_id, abs_name)
    return xz, wz, led

def fpo_photo(caption_bullet):
    """A dashed FPO figure carrying the copywriter's depiction bullet."""
    return (f'<figure class="phf"><div class="ph-fpo"><div class="fpo-tag">Photo · FPO</div>'
            f'<div class="fpo-note">{caption_bullet}</div></div>'
            f'<figcaption>{caption_bullet}</figcaption></figure>')

def split_captions(raw):
    parts = [p.strip(' •\u2022').strip() for p in str(raw or '').replace('\r','').split('\n') if p.strip()]
    return (parts + ['CAPTION TK', 'CAPTION TK'])[:2]

def marker_svg(mk):
    if not mk: return ''
    x, y = mk
    return (f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="#A6402B" stroke-width="1.3"/>'
            f'<circle cx="{x}" cy="{y}" r="2.2" fill="#A6402B"/>'
            f'<line x1="{x-25}" y1="{y}" x2="{x-7}" y2="{y}" stroke="#A6402B" stroke-width="1"/>'
            f'<line x1="{x+7}" y1="{y}" x2="{x+25}" y2="{y}" stroke="#A6402B" stroke-width="1"/>'
            f'<line x1="{x}" y1="{y-25}" x2="{x}" y2="{y-7}" stroke="#A6402B" stroke-width="1"/>'
            f'<line x1="{x}" y1="{y+7}" x2="{x}" y2="{y+25}" stroke="#A6402B" stroke-width="1"/>')

def render_zone(r, kind, ledger_rows=None, centroid=None, id_name_map=None):
    zid, name = r[0], str(r[1]).strip()
    is_x = (kind == 'X')
    is_wild = (not is_x) and str(r[2] or '').strip().lower() == 'wild'
    accent = 'var(--red)' if is_x else 'var(--spruce)'
    if is_x:                       # THE LOST WORLDS — night ground, reversed
        page, tx, sub_accent = '#141D1C', '#EFE8D8', '#E8927E'
        rule, mut = 'rgba(239,232,216,0.85)', 'rgba(239,232,216,0.65)'
    elif not is_wild:              # W-hostile — harsh concrete gray
        page, tx, sub_accent = '#ACB0AB', '#1E2E30', 'var(--spruce)'
        rule, mut = 'var(--ink)', '#3d4441'
    else:                          # W-wild — the living paper (covenant)
        page, tx, sub_accent = '#EFE8D8', '#1E2E30', 'var(--spruce)'
        rule, mut = 'var(--ink)', '#6b6350'
    series = 'The Lost Worlds' if is_x else 'Wildland Record'
    if is_x:
        cause = str(r[2] or '—').strip()
        pop_lost = r[3]; setts = r[4]
        pop_disp = f'{float(pop_lost):g} M' if pop_lost not in (None,'') else '—'
        band = f'''
  <div class="statband">
    <div class="stat hero"><div class="stat-sub">Population Displaced</div>
      <div class="n">{pop_disp} <span class="arr">&#9660;</span></div>
      <div class="l">left before &amp; during the Contraction · <em>EXCLUDED</em></div></div>
    <div class="stat"><div class="stat-sub">Settlements Closed</div>
      <div class="n" style="font-size:15pt">{setts if setts not in (None,'') else '—'}</div>
      <div class="l">carried in the ledger below</div></div>
    <div class="stat"><div class="stat-sub">Cause</div>
      <div class="n" style="font-size:12pt">{html.escape(cause.upper())}</div>
      <div class="l">the binding condition</div></div>
  </div>'''
    else:
        character = str(r[2] or '—').strip().upper()
        basis = str(r[3] or '—').strip()
        islands = str(r[4] or '').strip()
        ch_cls = 'wild' if character == 'WILD' else 'hostile'
        islands_html = (f'<div class="stat"><div class="stat-sub">Named Exceptions</div>'
                        f'<div class="l" style="margin-top:2px">{html.escape(islands)}</div></div>') if islands else ''
        band = f'''
  <div class="statband">
    <div class="stat hero ch-{ch_cls}"><div class="stat-sub">Character</div>
      <div class="n">{character}</div>
      <div class="l">{'the planet&rsquo;s terms, stated plainly' if ch_cls=='hostile' else 'held by covenant, not by hardship'}</div></div>
    <div class="stat"><div class="stat-sub">Basis</div>
      <div class="n" style="font-size:11.5pt">{html.escape(basis.upper())}</div>
      <div class="l">no settled claim in this record</div></div>
    {islands_html}
  </div>'''

    subtitle, lead, context = str(r[5] or ''), str(r[6] or ''), str(r[7] or '')
    try:
        mb = json.loads(str(r[8]))
        mb_label, mb_text = mb.get('label','').strip(), mb.get('text','').strip()
    except Exception:
        mb_label, mb_text = '', str(r[8] or '')
    ledger_prose = str(r[9] or '')
    coda_h, coda_s = str(r[10] or ''), str(r[11] or '')
    cap1, cap2 = split_captions(r[12])

    ledger_table = ''
    if is_x and ledger_rows:
        trs = ''
        for _, city, peak, aid, aname in sorted(ledger_rows, key=lambda t: -(t[2] or 0)):
            peak_d = f'{float(peak):g} M' if peak not in (None,'') else '—'
            dest = (f'<a href="{aid}.html">{html.escape(str(aname or aid))}</a>'
                    if aid and str(aid).startswith('R') else html.escape(str(aname or '—')))
            trs += (f'<tr><td class="c">{html.escape(str(city))}</td><td class="p">{peak_d}</td>'
                    f'<td class="d">&rarr; {dest}</td></tr>')
        ledger_table = f'''
  <div class="block cities-inv keep" style="margin-top:13px">
    <h3>The Ledger of Leaving</h3>
    <table class="cities">
      <tr><th>Settlement closed</th><th>Peak pop.</th><th>Absorbed by — a direction, not a guaranteed seat</th></tr>
      {trs}
    </table>
    <div class="cities-foot">Peak figures are pre-Contraction; destinations are the nearest survivable direction and are never added to the settled population.</div>
  </div>'''

    mk = marker_svg(centroid)
    fonts = ''.join(
        f"@font-face {{ font-family:'{fam}'; src:url('{FONT_BASE}{f}.woff2'); font-weight:{w};{it} }}\n"
        for fam,f,w,it in [
          ('Oswald','oswald-latin-400-normal',400,''),('Oswald','oswald-latin-500-normal',500,''),
          ('Oswald','oswald-latin-600-normal',600,''),('Oswald','oswald-latin-700-normal',700,''),
          ('SourceSerif','source-serif-4-latin-400-normal',400,''),
          ('SourceSerif','source-serif-4-latin-400-italic',400,' font-style:italic;'),
          ('SourceSerif','source-serif-4-latin-600-normal',600,''),
          ('SourceSerif','source-serif-4-latin-700-normal',700,'')])

    # ground-dependent furniture values
    if is_x:
        eyebrow_c, fpo_c, fpo_tint = 'var(--fog)', 'var(--fog)', 'rgba(195,208,203,0.07)'
        hero_box, bar_bg, co_tint, co_lab = 'var(--red)', 'rgba(239,232,216,0.12)', '0.16', 'var(--gold)'
    else:
        eyebrow_c, fpo_c, fpo_tint = 'var(--teal)', 'var(--teal)', 'rgba(22,70,80,0.05)'
        hero_box = 'var(--spruce)' if is_wild else 'var(--ink)'
        bar_bg, co_tint, co_lab = 'var(--ink)', '0.10', 'var(--accent)'
    lead_html = f'<p>{leadin(lead, 0)}</p>'
    return f'''<!DOCTYPE html>
<!-- 2060 Settlement Atlas · {series} Template {EXCL_VERSION} · companion to Entry Template v1.1 -->
<html lang="en"><head><meta charset="utf-8">
<title>2060 Settlement Atlas — {html.escape(name)} ({zid})</title>
<style>
{fonts}
:root{{ --paper:#EFE8D8; --ink:#1E2E30; --teal:#164650; --red:#A6402B; --spruce:#3D5A40;
       --gold:#DCA53C; --fog:#C3D0CB; --line:#C8BFA8; --blue:#2F5C8F; --accent:{accent};
       --page:{page}; --tx:{tx}; --rule:{rule}; --mut:{mut}; }}
@page {{ size:8.5in 11in; margin:0.5in 0.58in 0.55in; background:{page}; }}
@media screen {{ body {{ background:#8a8578; padding:28px 0; }}
  .sheet {{ max-width:7.5in; margin:0 auto; background:var(--page); padding:0.5in 0.58in 0.55in; box-shadow:0 6px 30px rgba(0,0,0,0.35); }} }}
@media print {{ .sheet {{ padding:0; }} }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'SourceSerif',serif; color:var(--tx); background:var(--page); font-size:9.6pt; line-height:1.42; }}
.keep {{ break-inside:avoid; page-break-inside:avoid; }}
.masthead {{ display:flex; justify-content:space-between; align-items:baseline; border-bottom:2.5px solid var(--rule); padding-bottom:5px; }}
.masthead .atlas {{ font-family:'Oswald'; font-weight:600; font-size:9pt; letter-spacing:2.4px; text-transform:uppercase; }}
.masthead .series {{ font-family:'Oswald'; font-weight:500; font-size:7.5pt; letter-spacing:2px; text-transform:uppercase; color:{sub_accent}; }}
.eyebrow {{ font-family:'Oswald'; font-weight:600; font-size:8.5pt; letter-spacing:3.5px; text-transform:uppercase; color:{eyebrow_c}; margin-top:12px; }}
h1 {{ font-family:'Oswald'; font-weight:700; font-size:34pt; line-height:0.96; letter-spacing:0.5px; text-transform:uppercase; margin-top:3px; }}
.subhead {{ font-family:'Oswald'; font-weight:500; font-size:12.5pt; letter-spacing:1px; color:{sub_accent}; margin-top:6px; }}
.hero-fpo {{ margin-top:10px; border:2.5px dashed {fpo_c}; background:repeating-linear-gradient(45deg,{fpo_tint},{fpo_tint} 10px,transparent 10px,transparent 20px); min-height:2.4in; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:22px; }}
.fpo-tag {{ font-family:'Oswald'; font-weight:700; font-size:8pt; letter-spacing:3px; text-transform:uppercase; color:{fpo_c}; margin-bottom:8px; }}
.fpo-note {{ font-family:'SourceSerif'; font-style:italic; font-size:9.5pt; line-height:1.45; color:var(--tx); max-width:5in; }}
.statband {{ display:flex; gap:0.12in; margin-top:10px; align-items:stretch; }}
.stat {{ flex:1; border:2px solid var(--rule); padding:8px 10px; display:flex; flex-direction:column; }}
.stat.hero {{ background:{hero_box}; color:var(--paper); }}
.stat.hero.ch-wild {{ background:var(--spruce); }}\n.stat.hero.ch-hostile {{ background:var(--ink); }}
.stat .stat-sub {{ font-family:'Oswald'; font-weight:600; font-size:6.2pt; letter-spacing:1.4px; text-transform:uppercase; }}
.stat:not(.hero) .stat-sub {{ background:{bar_bg}; color:var(--gold); margin:-8px -10px 7px -10px; padding:3.5px 10px; }}
.stat.hero .stat-sub {{ color:var(--gold); margin-bottom:4px; }}
.stat .n {{ font-family:'Oswald'; font-weight:700; font-size:19pt; line-height:1.02; }}
.stat.hero .n .arr {{ color:#E8927E; font-size:12pt; }}
.stat .l {{ font-size:7.4pt; line-height:1.3; margin-top:4px; color:inherit; opacity:0.92; }}
.stat .l em {{ font-style:italic; font-weight:600; font-family:'Oswald'; }}
p {{ margin-top:9px; text-align:justify; }}
.leadin {{ font-family:'Oswald'; font-weight:600; letter-spacing:0.5px; }}
h3 {{ font-family:'Oswald'; font-weight:700; font-size:12.5pt; letter-spacing:1.5px; text-transform:uppercase; margin-top:14px; border-bottom:2.5px solid var(--rule); padding-bottom:3px; }}
.callout {{ margin-top:12px; border-left:4px solid var(--gold); background:rgba(220,165,60,{co_tint}); padding:8px 13px; break-inside:avoid; }}
.callout .co-lab {{ font-family:'Oswald'; font-weight:600; font-size:7.5pt; letter-spacing:2.2px; text-transform:uppercase; color:{co_lab}; }}
.callout .co-body {{ font-size:9.4pt; line-height:1.4; margin-top:2px; }}
table.cities {{ width:100%; border-collapse:collapse; }}
table.cities th {{ font-family:'Oswald'; font-weight:600; font-size:6.8pt; letter-spacing:1.4px; text-transform:uppercase; text-align:left; padding:0 0 3px; }}
table.cities td {{ padding:3px 0; font-size:9pt; }}
table.cities td.c {{ font-weight:600; }}
table.cities td.p {{ width:14%; }}
table.cities td.d {{ width:46%; }}
.block.cities-inv {{ background:var(--paper); border:2px solid var(--paper); padding:11px 13px; color:var(--ink); }}
.block.cities-inv h3 {{ color:var(--red); border-bottom:2px solid rgba(30,46,48,0.4); margin-top:0; }}
.block.cities-inv th {{ color:var(--teal); border-bottom:1.5px solid rgba(30,46,48,0.5); }}
.block.cities-inv td {{ border-bottom:1px solid rgba(30,46,48,0.18); }}
.block.cities-inv td.p {{ color:#6b6350; }}
.block.cities-inv td.d a {{ color:var(--red); text-decoration:none; border-bottom:1px dotted rgba(166,64,43,0.55); }}
.block.cities-inv .cities-foot {{ color:#6b6350; font-size:6.8pt; margin-top:4px; font-style:italic; }}
.locator {{ margin-top:11px; border:2.5px solid var(--rule); background:#E3EBEC; break-inside:avoid; }}
.locator svg {{ display:block; width:100%; height:auto; }}
.locator-land path {{ fill:#C9D2C4; stroke:none; }}
.loc-coord {{ background:var(--ink); color:var(--paper); font-family:'Oswald'; font-weight:500; font-size:7pt; letter-spacing:1.5px; text-transform:uppercase; padding:3px 10px; text-align:right; }}
.photos {{ display:flex; gap:0.16in; margin-top:11px; break-inside:avoid; }}
figure.phf {{ flex:1; }}
.ph-fpo {{ height:1.95in; border:2.5px dashed {fpo_c}; background:repeating-linear-gradient(45deg,{fpo_tint},{fpo_tint} 10px,transparent 10px,transparent 20px); display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:12px; }}
.ph-fpo .fpo-note {{ font-size:8pt; }}
figure.phf figcaption {{ font-family:'Oswald'; font-weight:500; font-size:6.8pt; letter-spacing:0.8px; text-transform:uppercase; color:var(--mut); margin-top:4px; line-height:1.3; }}
.cta {{ margin-top:12px; background:var(--accent); color:var(--paper); padding:16px 20px 12px; break-inside:avoid; }}
.cta .big {{ font-family:'Oswald'; font-weight:700; font-size:17pt; line-height:1.05; letter-spacing:0.5px; }}
.cta .small {{ font-size:9.4pt; line-height:1.4; margin-top:6px; }}
.cta .foot {{ font-family:'Oswald'; font-weight:500; font-size:7pt; letter-spacing:1.6px; text-transform:uppercase; margin-top:8px; padding-top:7px; border-top:1px solid rgba(239,232,216,0.4); color:var(--fog); }}
</style></head><body><div class="sheet">
  <div class="masthead"><div class="atlas">The 2060 Settlement Atlas · {series}</div>
    <div class="series">Entry · {zid}</div></div>
  <div class="eyebrow">{html.escape(name)}</div>
  <h1>{html.escape(name)}</h1>
  <div class="subhead">{subtitle}</div>
  {band}
  <div class="hero-fpo keep"><div class="fpo-tag">Hero illustration · FPO</div>
    <div class="fpo-note">Hero illustration TK — {html.escape(name)}. Depiction note to be supplied.</div></div>
  {lead_html}
  <p>{context}</p>
  <div class="callout"><div class="co-lab">{mb_label}</div><div class="co-body">{mb_text}</div></div>
  {ledger_table}
  <h3>The Honest Ledger</h3>
  <p>{ledger_prose}</p>
  <div class="photos">{fpo_photo(cap1)}{fpo_photo(cap2)}</div>
  <div class="locator keep"><svg viewBox="0 0 1010 666" xmlns="http://www.w3.org/2000/svg">
    <g class="locator-land">{WORLDMAP}</g>{mk}</svg>
    <div class="loc-coord">{zid} · {html.escape(name)}</div></div>
  <div class="cta keep"><div class="big">{coda_h}</div><div class="small">{coda_s}</div>
    <div class="foot">The 2060 Settlement Atlas · {series}</div></div>
</div></body></html>'''

if __name__ == '__main__':
    import sys
    xz, wz, led = load_zones()
    zid = sys.argv[1] if len(sys.argv) > 1 else 'X001'
    row = next((r for r in xz + wz if r[0] == zid), None)
    kind = 'X' if zid.startswith('X') else 'W'
    out = sys.argv[2] if len(sys.argv) > 2 else f'/tmp/{zid}.html'
    open(out, 'w').write(render_zone(row, kind, led.get(zid)))
    print(f'[exclusion_gen {EXCL_VERSION}] wrote {out} · {zid} {row[1]} · workbook {WB.split("/")[-1]}')
