"""Genera docs/catalogo_meta.csv: fuente de datos para el catálogo de Meta (Facebook + WhatsApp).
Los vendidos salen como 'out of stock'. Productos sin precio se omiten (Meta exige precio)."""
import json, os, csv
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = 'https://jvckillita-ship-it.github.io/miaumarket/'
d = json.load(open(os.path.join(R, 'fuente', 'data.json'), encoding='utf-8'))
SEC = {'ropa': 'Ropa', 'calzado': 'Calzado', 'accesorios': 'Accesorios y varios'}
out = os.path.join(R, 'docs', 'catalogo_meta.csv'); n = 0
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['id', 'title', 'description', 'availability', 'condition', 'price', 'link', 'image_link', 'brand', 'product_type', 'custom_label_0'])
    for p in d:
        if p['p'] is None: continue
        title = p['n'] + (f" – Talla {p['t']}" if p['t'] else '')
        desc = p['d'] + (f" Talla: {p['t']}." if p['t'] else '') + (f" Precio {p['u']}." if p['u'] else '') + f" Código {p['c']}. Pedidos por WhatsApp."
        w.writerow([p['c'], title[:150], desc, 'out of stock' if p.get('e') == 'vendido' else 'in stock', 'new',
                    f"{p['p']:.2f} BOB", WEB, f"{WEB}img/{p['c']}.jpg", p['m'] or 'MIAUMARKET', SEC[p['s']], SEC[p['s']]])
        n += 1
print('csv', n)
