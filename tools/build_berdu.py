#!/usr/bin/env python3
"""Pecah index.html menjadi potongan HTML per section untuk ditempel di blok
HTML/Embed builder (mis. Berdu).

Pemakaian:
    python3 tools/build_berdu.py                 # gambar dari Vercel (default)
    python3 tools/build_berdu.py --base URL      # gambar dari host lain

Hasil ada di folder berdu/. Jalankan ulang setiap kali index.html berubah.
"""
import argparse
import math
import os
import re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_BASE = 'https://dvn-glowlab-lp.vercel.app/assets/'

# id yang dipakai halaman; diberi awalan dvn- supaya tidak bentrok dengan id milik builder
IDS = ['top', 'hero', 'masalah', 'solusi', 'komposisi', 'testimoni', 'sertifikat', 'order',
       'p-count', 'p-msg', 'orbit', 'disc', 'beam', 'dbody', 'bar', 'auto', 'auto-label',
       'prev', 'next', 'track', 'dots']
KEYFRAMES = ['spin', 'float', 'breathe', 'ping', 'rise', 'pop', 'fill', 'nudge', 'twinkle',
             'fab-in', 'fab-ping']

SECTIONS = [  # (file, judul, penanda awal, penanda akhir)
    ('01-hero.html', 'Hero (logo DVN x Glow Lab + menu + hero)', '<section class="hero"', '</section>'),
    ('02-problem.html', 'Problem', '<section class="sec" id="masalah"', '</section>'),
    ('03-solusi.html', 'Solusi', '<section class="sec blush" id="solusi"', '</section>'),
    ('04-komposisi.html', 'Komposisi (interaktif)', '<section class="sec" id="komposisi"', '</section>'),
    ('05-testimoni.html', 'Testimoni', '<section class="sec blush" id="testimoni"', '</section>'),
    ('06-sertifikat.html', 'Sertifikat', '<section class="sec" id="sertifikat"', '</section>'),
    ('07-cta.html', 'CTA akhir', '<section class="sec cta" id="order"', '</section>'),
    ('08-tombol-wa-melayang.html', 'Tombol WhatsApp melayang', '<a class="fab"', '</a>'),
]


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


# ---------- CSS: beri awalan .dvn-lp pada semua selector ----------
def prefix_selector(sel):
    sel = sel.strip()
    if sel in (':root', 'html', 'body'):
        return '.dvn-lp'
    return '.dvn-lp ' + sel


def scope_rules(css):
    out, i = [], 0
    while i < len(css):
        if css.startswith('/*', i):
            j = css.index('*/', i) + 2
            i = j
            continue
        if css[i].isspace():
            i += 1
            continue
        brace = css.index('{', i)
        head = css[i:brace].strip()
        # cari kurung tutup yang seimbang
        depth, j = 0, brace
        while True:
            if css[j] == '{':
                depth += 1
            elif css[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = css[brace + 1:j]
        i = j + 1
        if head.startswith('@keyframes'):
            name = head.split()[1]
            out.append('@keyframes dvn-%s {%s}' % (name, body))
        elif head.startswith('@media'):
            out.append('%s {\n%s\n}' % (head, scope_rules(body)))
        else:
            sels = [s for s in head.split(',') if '.js .rv' not in s]
            if not sels:
                continue
            out.append('%s {%s}' % (', '.join(prefix_selector(s) for s in sels), body))
    return '\n'.join(out)


def build_css(css):
    css = css.replace('.hero + .sec', '.sec#masalah')
    css = scope_rules(css)
    # nama animasi ikut diberi awalan
    def anim(m):
        decl = m.group(0)
        for k in sorted(KEYFRAMES, key=len, reverse=True):
            decl = re.sub(r'(?<![\w-])%s(?![\w-])' % re.escape(k), 'dvn-' + k, decl)
        return decl
    css = re.sub(r'animation\s*:[^;}]*', anim, css)
    for k in IDS:
        css = re.sub(r'#%s(?![\w-])' % re.escape(k), '#dvn-' + k, css)
    # wrapper: blok berdiri sendiri di dalam halaman builder
    css += '''
.dvn-lp { display: block; width: 100%; overflow-x: clip; line-height: 1.55; }
.dvn-lp.dvn-full { width: 100vw; margin-left: calc(50% - 50vw); }
.dvn-lp p, .dvn-lp h1, .dvn-lp h2, .dvn-lp h3, .dvn-lp ul { margin-top: 0; }
.dvn-lp ul.perks { margin: 0; padding: 0; list-style: none; }
.dvn-lp .top { position: relative; }
.dvn-lp + .dvn-lp { margin-top: 0; }
/* pengaman terhadap gaya tema builder */
.dvn-lp h1, .dvn-lp h2, .dvn-lp h3 { color: var(--ink); text-transform: none; }
.dvn-lp p, .dvn-lp li { line-height: inherit; }
.dvn-lp img { border: 0; padding: 0; background: transparent; }
.dvn-lp a { text-decoration: none; }
.dvn-lp a.link-down { text-decoration: none; }'''
    return css


# ---------- HTML ----------
def transform_html(html, base, wa_number, messages):
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    # buang kelas animasi-scroll (butuh script global yang belum tentu jalan di builder)
    def clean_class(m):
        cls = [c for c in m.group(1).split() if c != 'rv']
        return 'class="%s"' % ' '.join(cls) if cls else ''
    html = re.sub(r'class="([^"]*)"', clean_class, html)
    html = re.sub(r'<(\w+) >', r'<\1>', html)
    html = re.sub(r'<(\w+)\s+(?=[^>]*>)', lambda m: '<%s ' % m.group(1), html)
    for k in IDS:
        html = html.replace('id="%s"' % k, 'id="dvn-%s"' % k).replace('href="#%s"' % k, 'href="#dvn-%s"' % k)
    html = html.replace('src="assets/', 'src="' + base)
    # link WhatsApp ditulis langsung supaya tetap jalan tanpa script
    def wa(m):
        pos = m.group(2)
        url = 'https://wa.me/%s?text=%s' % (wa_number, quote(messages.get(pos, messages['final'])))
        return '%shref="%s" target="_blank" rel="noopener"' % (m.group(1), url)
    html = re.sub(r'(<a [^>]*data-wa="(\w+)"[^>]*?)href="#dvn-order"', wa, html)
    return html


def extract(body, start, end):
    i = body.index(start)
    j = body.index(end, i) + len(end)
    return body[i:j]


def ingredients_js(js, base):
    arr = re.search(r'var INGREDIENTS = \[.*?\n  \];', js, re.S).group(0)
    return arr.replace("img: 'assets/", "img: '" + base)


def static_orbit(ingredients):
    """Tombol bahan dirender langsung di HTML; script hanya menambah interaksi."""
    items = re.findall(r"short: '([^']*)', name: '([^']*)'.*?img: '([^']*)'", ingredients)
    bw, bh, cx, cy, r, half = 342, 360, 171, 172, 128, 29
    out = []
    for i, (short, name, img) in enumerate(items):
        a = math.radians(-90 + i * 360 / len(items))
        left = (cx + r * math.cos(a) - half) / bw * 100
        top = (cy + r * math.sin(a) - half) / bh * 100
        out.append('<button type="button" class="chip%s" style="left:%.3f%%;top:%.3f%%" aria-label="%s" aria-pressed="%s">'
                   '<img src="%s" alt="" width="160" height="160" loading="lazy" decoding="async">'
                   '<span class="clabel" aria-hidden="true">%s</span></button>'
                   % (' on' if i == 0 else '', left, top, name, 'true' if i == 0 else 'false', img, short))
    return '\n'.join(out)


def static_card(ingredients):
    m = re.search(r"\{ short: '([^']*)', name: '([^']*)', label: '([^']*)', group: '(\w+)', img: '([^']*)', bg: '([^']*)', fg: '([^']*)', desc: '([^']*)', rel: '([^']*)'", ingredients)
    _, name, label, group, img, bg, fg, desc, rel = m.groups()
    groups = {'hid': 'Kelembapan &amp; kekenyalan', 'aox': 'Perlindungan antioksidan'}
    return ('<div class="dhead"><img class="dicon" src="%s" alt="" width="160" height="160">'
            '<div class="dmeta"><span class="dnum">BAHAN 01 / 07</span>'
            '<span class="gpill" style="background:%s;color:%s">%s</span></div></div>'
            '<h3 class="dname">%s</h3><p class="dlabel">%s</p><p class="ddesc">%s</p>'
            '<p class="rel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>Relevan untuk: %s</p>'
            % (img, bg, fg, groups[group], name, label, desc, rel.replace('&', '&amp;')))


GLOBAL_SCRIPT = '''<script>
/* Klik tombol WhatsApp -> event Meta Pixel "Contact" (jika Pixel sudah terpasang di Berdu) */
(function () {
  if (window.__dvnWA) return; window.__dvnWA = 1;
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.dvn-lp [data-wa]');
    if (a && typeof window.fbq === 'function') window.fbq('track', 'Contact', { content_name: 'wa_' + a.getAttribute('data-wa') });
  }, true);
})();
</script>'''

PROBLEM_SCRIPT = '''<script>
(function () {
  var root = document.getElementById('dvn-masalah'); if (!root || root.__dvn) return; root.__dvn = 1;
  var MSG = ['Ketuk kartu di atas untuk mulai.', 'Wajar dialami, apalagi dengan aktivitas padat.', 'Wajar dialami, apalagi dengan aktivitas padat.', 'Kulitmu mungkin sedang butuh dukungan lebih.', 'Kulitmu mungkin sedang butuh dukungan lebih.'];
  var cards = root.querySelectorAll('.pcard'), segs = root.querySelectorAll('.seg');
  function update() {
    var n = root.querySelectorAll('.pcard[aria-pressed="true"]').length;
    document.getElementById('dvn-p-count').textContent = n;
    document.getElementById('dvn-p-msg').textContent = MSG[n];
    segs.forEach(function (s, i) { s.classList.toggle('on', i < n); });
  }
  cards.forEach(function (c) {
    c.addEventListener('click', function () {
      c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); update();
    });
  });
})();
</script>'''

KOMPOSISI_SCRIPT = '''<script>
(function () {
  var root = document.getElementById('dvn-komposisi'); if (!root || root.__dvn) return; root.__dvn = 1;
  %(ingredients)s
  var GROUPS = { hid: 'Kelembapan & kekenyalan', aox: 'Perlindungan antioksidan' };
  var STEP_MS = 3400;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var disc = document.getElementById('dvn-disc'), beam = document.getElementById('dvn-beam');
  var dbody = document.getElementById('dvn-dbody'), bar = document.getElementById('dvn-bar');
  var autoBtn = document.getElementById('dvn-auto'), pills = root.querySelectorAll('.pill');
  var chips = Array.prototype.slice.call(root.querySelectorAll('.chip'));
  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  var state = { active: 0, filter: 'all', auto: !reduceMotion, beam: -90, visible: false }, timer = null;
  function ids(f) { return INGREDIENTS.map(function (_, i) { return i; }).filter(function (i) { return f === 'all' || INGREDIENTS[i].group === f; }); }
  function render() {
    var ing = INGREDIENTS[state.active];
    chips.forEach(function (c, i) {
      var on = i === state.active, inF = state.filter === 'all' || INGREDIENTS[i].group === state.filter;
      c.classList.toggle('on', on); c.classList.toggle('dim', !on && !inF); c.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    disc.style.backgroundColor = ing.bg;
    beam.style.transform = 'rotate(' + state.beam + 'deg)';
    dbody.innerHTML = '<div class="dhead"><img class="dicon" src="' + ing.img + '" alt="" width="160" height="160">' +
      '<div class="dmeta"><span class="dnum">BAHAN 0' + (state.active + 1) + ' / 07</span>' +
      '<span class="gpill" style="background:' + ing.bg + ';color:' + ing.fg + '">' + GROUPS[ing.group] + '</span></div></div>' +
      '<h3 class="dname">' + ing.name + '</h3><p class="dlabel">' + ing.label + '</p><p class="ddesc">' + ing.desc + '</p>' +
      '<p class="rel">' + CHECK + 'Relevan untuk: ' + ing.rel + '</p>';
    dbody.classList.remove('anim'); void dbody.offsetWidth; dbody.classList.add('anim');
    restartBar();
  }
  function go(i) { var t = -90 + i * 360 / INGREDIENTS.length; state.beam += ((((t - state.beam) %% 360) + 540) %% 360) - 180; state.active = i; render(); }
  function step(d) { var l = ids(state.filter), k = l.indexOf(state.active); k = k < 0 ? 0 : (k + d + l.length) %% l.length; go(l[k]); }
  function running() { return state.auto && state.visible; }
  function restartBar() { bar.classList.remove('run'); if (running()) { void bar.offsetWidth; bar.classList.add('run'); } }
  function schedule() { clearInterval(timer); timer = running() ? setInterval(function () { step(1); }, STEP_MS) : null; restartBar(); }
  function setAuto(on) { state.auto = on; autoBtn.setAttribute('aria-pressed', on ? 'true' : 'false'); document.getElementById('dvn-auto-label').textContent = on ? 'Jeda tur' : 'Putar tur'; schedule(); }
  bar.style.setProperty('--step', STEP_MS + 'ms');
  chips.forEach(function (c, i) { c.addEventListener('click', function () { setAuto(false); go(i); }); });
  autoBtn.addEventListener('click', function () { setAuto(!state.auto); });
  document.getElementById('dvn-prev').addEventListener('click', function () { setAuto(false); step(-1); });
  document.getElementById('dvn-next').addEventListener('click', function () { setAuto(false); step(1); });
  pills.forEach(function (p) {
    p.addEventListener('click', function () {
      state.filter = p.getAttribute('data-filter');
      pills.forEach(function (q) { q.setAttribute('aria-pressed', q === p ? 'true' : 'false'); });
      var l = ids(state.filter); if (l.indexOf(state.active) < 0) go(l[0]); else render(); schedule();
    });
  });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { state.visible = e[0].isIntersecting; schedule(); }, { threshold: 0.35 }).observe(root);
  setAuto(state.auto);
})();
</script>'''

TESTI_SCRIPT = '''<script>
(function () {
  var track = document.getElementById('dvn-track'); if (!track || track.__dvn) return; track.__dvn = 1;
  var dots = document.querySelectorAll('#dvn-dots .d');
  track.addEventListener('scroll', function () {
    var card = track.querySelector('.tcard'), w = card ? card.offsetWidth + 12 : 312;
    var i = Math.max(0, Math.min(dots.length - 1, Math.round(track.scrollLeft / w)));
    dots.forEach(function (d, j) { d.classList.toggle('on', j === i); });
  }, { passive: true });
})();
</script>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=DEFAULT_BASE, help='URL folder gambar (diakhiri /)')
    ap.add_argument('--out', default='berdu')
    args = ap.parse_args()
    base = args.base if args.base.endswith('/') else args.base + '/'

    src = read('index.html')
    css = src[src.index('<style>') + 7:src.index('</style>')]
    fonts = re.search(r'<link href="https://fonts.googleapis.com/css2[^>]*>', src).group(0)
    body = src[src.index('<body>'):]
    js = src[src.rindex('<script>'):]
    wa_number = re.search(r"var WA_NUMBER = '(\d+)'", js).group(1)
    messages = dict(re.findall(r"^\s+(\w+): '([^']*)',?$", js[js.index('WA_MESSAGES'):js.index('};', js.index('WA_MESSAGES'))], re.M))
    ingredients = ingredients_js(js, base)

    out_dir = os.path.join(ROOT, args.out)
    os.makedirs(out_dir, exist_ok=True)
    head_note = '<!-- DVN x Glow Lab | %s | dibuat otomatis dari index.html oleh tools/build_berdu.py -->\n'

    glob = (head_note % '00 GLOBAL: tempel SEKALI, paling atas (font + gaya)') + \
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n' + \
        fonts + '\n<style>\n' + build_css(css) + '\n</style>\n' + GLOBAL_SCRIPT + '\n'
    files = {'00-global.html': glob}

    for fname, title, start, end in SECTIONS:
        html = transform_html(extract(body, start, end), base, wa_number, messages)
        if fname.startswith('01'):
            bar = transform_html(extract(body, '<header class="top"', '</header>'), base, wa_number, messages)
            bar = bar.replace('<header ', '<div ', 1)[:-len('</header>')] + '</div>'
            html = bar + '\n' + html
        script = ''
        if fname.startswith('02'):
            script = PROBLEM_SCRIPT
        elif fname.startswith('04'):
            html = re.sub(r'(<span class="beam"[^>]*></span>\s*<div class="bottle-wrap".*?</div>)',
                          lambda m: m.group(1) + '\n' + static_orbit(ingredients), html, flags=re.S)
            html = html.replace('<div class="anim" id="dvn-dbody"></div>', '<div class="anim" id="dvn-dbody">%s</div>' % static_card(ingredients))
            script = KOMPOSISI_SCRIPT % {'ingredients': ingredients.strip()}
        elif fname.startswith('05'):
            script = TESTI_SCRIPT
        files[fname] = (head_note % title) + '<div class="dvn-lp">\n' + html + '\n</div>\n' + (script + '\n' if script else '')

    # satu blok berisi semuanya
    allin = files['00-global.html'] + '\n'.join(v for k, v in sorted(files.items()) if k[:2] != '00')
    files['lp-lengkap-1-blok.html'] = allin
    # file pratinjau lokal: buka di browser untuk mengecek semua potongan
    files['preview.html'] = ('<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                             '<title>Pratinjau potongan Berdu</title><style>body{margin:0;font-family:Arial,sans-serif}'
                             '.builder{max-width:1200px;margin:0 auto}</style></head><body><div class="builder">\n'
                             + files['00-global.html'] + '\n'.join(v for k, v in sorted(files.items()) if k[:2].isdigit() and k[:2] != '00')
                             + '\n</div></body></html>')
    for name, content in files.items():
        with open(os.path.join(out_dir, name), 'w', encoding='utf-8') as f:
            f.write(content)
        print('%-32s %6.1f KB' % (name, len(content.encode()) / 1024))


if __name__ == '__main__':
    main()
