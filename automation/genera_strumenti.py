r"""genera_strumenti.py - crea una pagina per ogni strumento di assets/data/strumenti.json (IT + EN).
USO: python automation\genera_strumenti.py   (poi: python automation\allinea_hash.py  e commit)
- La fonte e' SOLO assets/data/strumenti.json: per aggiungere uno strumento aggiungi un oggetto li' (l'ordine = priorita' di profitto) e rilancia.
- Pagine IT: _pages/strumenti/<id>.md   Pagine EN: en/tools/<id>.md   (le pagine di strumenti tolti dal json vengono cancellate)
- Anche la home (blocks_home.json, IT e EN) riceve l'elenco link come fallback per chi non ha JavaScript e per i motori di ricerca."""
import io, json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f: f.write(text)

def q(s): return s.replace('\\', '\\\\').replace('"', '\\"')

def pagina(t, L):
    n, d = t[L]
    if L == 'it':
        title = '%s gratis online' % n; seo = '%s Gratis, senza installare nulla.' % d; perm = '/strumenti/%s/' % t['id']
        extra = ''
    else:
        title = '%s free online' % n; seo = '%s Free, nothing to install.' % d; perm = '/en/tools/%s/' % t['id']
        extra = 'lang: en\nlocale: en\ntr: tradotto\ntr_hash: x\n'
    fm = '---\nref: tool-%s\nlayout: default\ntitle: "%s"\nseo_description: "%s"\ndescription: "%s"\n%spermalink: %s\n---\n' % (t['id'], q(title), q(seo), q(seo), extra, perm)
    body = ('<div id="ft-app" data-mode="tool" data-tool="%s" data-lang="%s" data-base="{{ \'\' | relative_url }}" data-endpoint="{{ site.contact_endpoint }}">'
            '<section class="ft-box"><h1>%s</h1><p>%s</p></section></div>\n'
            '<script src="{{ \'/assets/js/freetool.js?v=1\' | relative_url }}" defer></script>\n') % (t['id'], L, n, d)
    return fm + body

def main():
    data = json.load(io.open(os.path.join(R, 'assets/data/strumenti.json'), encoding='utf-8'))
    ids = set()
    for t in data['strumenti']:
        ids.add(t['id'])
        w(os.path.join(R, '_pages/strumenti/%s.md' % t['id']), pagina(t, 'it'))
        w(os.path.join(R, 'en/tools/%s.md' % t['id']), pagina(t, 'en'))
    for cartella in ('_pages/strumenti', 'en/tools'):
        p = os.path.join(R, cartella)
        for f in os.listdir(p):
            if f.endswith('.md') and f[:-3] not in ids: os.remove(os.path.join(p, f))
    # fallback senza JavaScript nella home
    for L, fn, pref in (('it', '_data/blocks_home.json', '/strumenti/'), ('en', '_data/i18n/en/blocks_home.json', '/en/tools/')):
        path = os.path.join(R, fn)
        blocks = json.load(io.open(path, encoding='utf-8'))
        lis = ''.join('<li><a href="__BASEURL__%s%s/">%s</a></li>' % (pref, t['id'], t[L][0]) for t in data['strumenti'])
        h1 = 'Tutti gli strumenti che ti servono, gratis' if L == 'it' else 'Every tool you need, for free'
        for b in blocks:
            if b['id'] == 'strumenti':
                b['html'] = ('<div id="ft-app" data-mode="home" data-lang="%s" data-base="__BASEURL__"><h1>%s</h1><ul>%s</ul></div>'
                             '<script src="__BASEURL__/assets/js/freetool.js?v=1" defer></script>') % (L, h1, lis)
        w(path, json.dumps(blocks, ensure_ascii=False, indent=2) + '\n')
    print('strumenti:', len(ids))

if __name__ == '__main__':
    main()
