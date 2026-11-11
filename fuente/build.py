"""Regenera index.html desde fuente/template.html + fuente/data.json.
Uso: python3 fuente/build.py [estado.json]   (estado.json: {"MM-001": "Vendido", ...})"""
import json, sys, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(R, 'fuente', 'data.json'), encoding='utf-8'))
st = json.load(open(sys.argv[1], encoding='utf-8')) if len(sys.argv) > 1 else {}
for p in d:
    e = st.get(p['c'], p.get('e', '')).lower()
    p['e'] = e if e in ('vendido', 'reservado') else ''
t = open(os.path.join(R, 'fuente', 'template.html'), encoding='utf-8').read()
page = t.replace('__DATA__', json.dumps(d, ensure_ascii=False))
head = page.split('<style>')[0]; rest = page[len(head):]
html = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + rest.split('</style>')[0] + '</style>\n</head>\n<body>\n' + rest.split('</style>', 1)[1] + '\n</body>\n</html>\n')
open(os.path.join(R, 'docs', 'index.html'), 'w', encoding='utf-8').write(html)
print('ok', sum(p['e'] == 'vendido' for p in d), 'vendidos')
