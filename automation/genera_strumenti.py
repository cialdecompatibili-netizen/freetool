r"""genera_strumenti.py - crea le pagine di FreeTool partendo da assets/data/strumenti.json (IT + EN).
USO: python automation\genera_strumenti.py   (poi: python automation\allinea_hash.py  e commit)
FONTE UNICA: assets/data/strumenti.json = settori > categorie > strumenti. L'ordine nel file = priorita' di profitto.
- NUOVO SETTORE: aggiungi un oggetto in "settori" (id, it, en, slug.it, slug.en, ico, colore, desc.it, desc.en), le sue "categorie" (campo settore) e i suoi "strumenti". Rilancia: compaiono da soli
  la tessera in home, la pagina del settore, le pagine dei tool e la voce di menu (fino a 3 settori voci dirette, oltre una tendina "Strumenti").
- Pagine create: settore _pages/settori/<slug>.md | en/settori/<slug>.md ; tool _pages/strumenti/<id>.md | en/tools/<id>.md (quelle di cose tolte dal json si cancellano).
- Aggiorna anche: fallback senza JavaScript della home (blocks_home.json IT/EN), _data/navigation.yml e _data/i18n/en/navigation.yml, sottomenu.yml (solo la chiave Strumenti/Tools)."""
import io, json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_DIRETTE = 3

def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f: f.write(text)

def q(s): return s.replace('\\', '\\\\').replace('"', '\\"')
APP = ('<div id="ft-app" data-mode="%s" %s data-lang="%s" data-base="{{ \'\' | relative_url }}" data-endpoint="{{ site.contact_endpoint }}">%s</div>\n'
       '<script src="{{ \'/assets/js/freetool.js?v=2\' | relative_url }}" defer></script>\n')

def fm(ref, title, seo, perm, L):
    extra = '' if L == 'it' else 'lang: en\nlocale: en\ntr: tradotto\ntr_hash: x\n'
    return '---\nref: %s\nlayout: default\ntitle: "%s"\nseo_description: "%s"\ndescription: "%s"\n%spermalink: %s\n---\n' % (ref, q(title), q(seo), q(seo), extra, perm)

def pagina_tool(t, L):
    n, d = t[L]
    if L == 'it': title, seo, perm = '%s gratis online' % n, '%s Gratis, senza installare nulla.' % d, '/strumenti/%s/' % t['id']
    else: title, seo, perm = '%s free online' % n, '%s Free, nothing to install.' % d, '/en/tools/%s/' % t['id']
    return fm('tool-' + t['id'], title, seo, perm, L) + APP % ('tool', 'data-tool="%s"' % t['id'], L, '<section class="ft-box"><h1>%s</h1><p>%s</p></section>' % (n, d))

def url_settore(s, L): return '/%s/' % s['slug']['it'] if L == 'it' else '/en/%s/' % s['slug']['en']

def pagina_settore(s, L, data):
    n, d = s[L], s['desc'][L]
    pref = '/strumenti/' if L == 'it' else '/en/tools/'
    cats = set(c['id'] for c in data['categorie'] if c['settore'] == s['id'])
    lis = ''.join('<li><a href="{{ \'%s%s/\' | relative_url }}">%s</a></li>' % (pref, t['id'], t[L][0]) for t in data['strumenti'] if t['cat'] in cats)
    title = ('%s gratuiti online' if L == 'it' else '%s free online') % n
    seo = d + (' Gratis, senza installare nulla.' if L == 'it' else ' Free, nothing to install.')
    return fm('settore-' + s['id'], title, seo, url_settore(s, L), L) + APP % ('settore', 'data-sector="%s"' % s['id'], L, '<h1>%s</h1><p>%s</p><ul>%s</ul>' % (n, d, lis))

def leggi_nav(path):
    if not os.path.exists(path): return []
    t = io.open(path, encoding='utf-8').read()
    return re.findall(r'- title: "([^"]*)"\s*\n\s*url: (\S+)', t)

def scrivi_nav(path, L, data):
    home = ('Home', '/' if L == 'it' else '/en/')
    sett = [(s[L], url_settore(s, L)) for s in data['settori']]
    gruppo = ('Strumenti' if L == 'it' else 'Tools', '/' if L == 'it' else '/en/')
    skip_t = set(['Home', 'Strumenti', 'Tools'] + [x[0] for x in sett]); skip_u = set(x[1] for x in sett)
    resto = [(a, b) for a, b in leggi_nav(path) if a not in skip_t and b not in skip_u and b != home[1]]
    voci = [home] + (sett if len(sett) <= MAX_DIRETTE else [gruppo]) + resto
    w(path, 'main:\n' + ''.join('  - title: "%s"\n    url: %s\n' % v for v in voci))
    return len(sett) > MAX_DIRETTE, gruppo[0], sett

def scrivi_sottomenu(path, chiave, attivo, sett):
    if not os.path.exists(path): w(path, '')
    t = io.open(path, encoding='utf-8').read()
    t = re.sub(r'(?m)^%s:\n(?:[ \t]+.*\n|[ \t]*\n)*' % re.escape(chiave), '', t)
    if attivo:
        if t and not t.endswith('\n'): t += '\n'
        t += '%s:\n' % chiave + ''.join('  - title: "%s"\n    url: %s\n' % v for v in sett)
    w(path, t)

def main():
    data = json.load(io.open(os.path.join(R, 'assets/data/strumenti.json'), encoding='utf-8'))
    ids = set(t['id'] for t in data['strumenti'])
    for t in data['strumenti']:
        w(os.path.join(R, '_pages/strumenti/%s.md' % t['id']), pagina_tool(t, 'it'))
        w(os.path.join(R, 'en/tools/%s.md' % t['id']), pagina_tool(t, 'en'))
    for s in data['settori']:
        w(os.path.join(R, '_pages/settori/%s.md' % s['slug']['it']), pagina_settore(s, 'it', data))
        w(os.path.join(R, 'en/settori/%s.md' % s['slug']['en']), pagina_settore(s, 'en', data))
    for cartella, tieni in (('_pages/strumenti', ids), ('en/tools', ids), ('_pages/settori', set(s['slug']['it'] for s in data['settori'])), ('en/settori', set(s['slug']['en'] for s in data['settori']))):
        p = os.path.join(R, cartella)
        if os.path.isdir(p):
            for f in os.listdir(p):
                if f.endswith('.md') and f[:-3] not in tieni: os.remove(os.path.join(p, f))
    # home: fallback senza JavaScript = link ai settori
    for L, fn in (('it', '_data/blocks_home.json'), ('en', '_data/i18n/en/blocks_home.json')):
        path = os.path.join(R, fn)
        blocks = json.load(io.open(path, encoding='utf-8'))
        lis = ''.join('<li><a href="__BASEURL__%s">%s</a></li>' % (url_settore(s, L), s[L]) for s in data['settori'])
        h1 = 'Tutti gli strumenti che ti servono, gratis' if L == 'it' else 'Every tool you need, for free'
        for b in blocks:
            if b['id'] == 'strumenti':
                b['html'] = ('<div id="ft-app" data-mode="home" data-lang="%s" data-base="__BASEURL__"><h1>%s</h1><ul>%s</ul></div>'
                             '<script src="__BASEURL__/assets/js/freetool.js?v=2" defer></script>') % (L, h1, lis)
        w(path, json.dumps(blocks, ensure_ascii=False, indent=2) + '\n')
    # menu
    for L, nav, sm in (('it', '_data/navigation.yml', '_data/sottomenu.yml'), ('en', '_data/i18n/en/navigation.yml', '_data/i18n/en/sottomenu.yml')):
        dropdown, chiave, sett = scrivi_nav(os.path.join(R, nav), L, data)
        scrivi_sottomenu(os.path.join(R, sm), chiave, dropdown, sett)
    print('settori:', len(data['settori']), 'strumenti:', len(ids))

if __name__ == '__main__':
    main()
