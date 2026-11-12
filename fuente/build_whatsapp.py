"""Genera docs/whatsapp.html: hoja de carga para el catálogo de WhatsApp Business (copiar/pegar)."""
import json, os, html
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(R, 'fuente', 'data.json'), encoding='utf-8'))
WEB = 'https://jvckillita-ship-it.github.io/miaumarket/'
SEC = [('ropa', 'Ropa'), ('calzado', 'Calzado'), ('accesorios', 'Accesorios y varios')]
def fmt(n): return f"{n:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
cards = []
for sid, sname in SEC:
    items = [p for p in d if p['s'] == sid and p.get('e') != 'vendido']
    cards.append(f'<h2 id="{sid}">{sname} <small>{len(items)} productos · colección «{sname}»</small></h2>')
    for p in items:
        name = p['n'] + (f" – {p['m']}" if p['m'] else '')
        desc = p['d'] + (f"\nTalla: {p['t']}" if p['t'] else '') + (f"\nPrecio {p['u']}" if p['u'] else '') + f"\nCódigo: {p['c']}"
        price = ((str(int(p['p'])) if p['p'] == int(p['p']) else f"{p['p']:.2f}") if p['p'] is not None else '')
        fields = [('Nombre', name), ('Precio', price), ('Descripción', desc), ('Enlace', WEB), ('Código de artículo', p['c'])]
        rows = ''.join(
            f'<div class="f"><span class="k">{k}</span><span class="v">{html.escape(v) if v else "<em>— sin precio, dejar vacío —</em>"}</span>'
            + (f'<button type="button" data-copy="{html.escape(v, quote=True)}">Copiar</button>' if v else '') + '</div>'
            for k, v in fields)
        cards.append(f'''<article class="card" id="{p['c']}">
  <div class="top"><label class="done"><input type="checkbox" data-id="{p['c']}"> Cargado</label><b>{p['c']}</b><span>{'Bs. ' + fmt(p['p']) if p['p'] is not None else 'Sin precio'}</span></div>
  <div class="body"><a class="ph" href="img/{p['c']}.jpg" download="{p['c']}.jpg"><img src="img/{p['c']}.jpg" alt="{html.escape(p['n'])}" loading="lazy"><span>Guardar foto</span></a>
  <div class="fields">{rows}</div></div></article>''')
page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Carga catálogo WhatsApp · MIAUMARKET</title>
<style>
:root{{--bg:#eef3f3;--s:#fff;--ink:#191e23;--mu:#5d6a6c;--li:#d3dcdc;--rose:#b85c5f;--wa:#1d8a4b}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}}
.wrap{{max-width:900px;margin:0 auto;padding:16px}}h1{{font:600 22px/1.2 Georgia,serif;margin:4px 0 8px}}
.help{{background:var(--s);border:1px solid var(--li);border-radius:12px;padding:12px 14px}}.help ol{{margin:6px 0 0;padding-left:20px}}.help li{{margin:4px 0}}
.prog{{position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:5;display:flex;gap:10px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--li)}}
.prog a{{color:var(--ink);background:var(--s);border:1px solid var(--li);border-radius:999px;padding:5px 12px;text-decoration:none;font-size:14px}}
.prog b{{margin-left:auto;font-variant-numeric:tabular-nums}}
h2{{font:600 19px Georgia,serif;margin:22px 0 10px}}h2 small{{font:400 13px system-ui,sans-serif;color:var(--mu)}}
.card{{background:var(--s);border:1px solid var(--li);border-radius:12px;margin:0 0 12px;overflow:hidden}}
.card.ok{{opacity:.55}}.top{{display:flex;gap:12px;align-items:center;padding:8px 12px;background:#f5f8f8;border-bottom:1px solid var(--li)}}
.top b{{color:var(--rose);letter-spacing:.05em}}.top span{{margin-left:auto;font-weight:600}}.done{{display:flex;gap:6px;align-items:center;font-size:14px}}
.done input{{width:20px;height:20px}}.body{{display:grid;grid-template-columns:150px 1fr;gap:12px;padding:12px}}
.ph{{display:flex;flex-direction:column;gap:6px;text-decoration:none;color:var(--wa);font-size:13px;font-weight:600;text-align:center}}
.ph img{{width:150px;height:150px;object-fit:contain;border:1px solid var(--li);border-radius:8px;background:#fff}}
.fields{{display:grid;gap:8px;min-width:0}}.f{{display:grid;grid-template-columns:1fr auto;gap:2px 8px;align-items:start}}
.k{{grid-column:1/-1;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mu)}}.v{{white-space:pre-wrap;word-break:break-word;min-width:0}}
.f button{{border:1px solid var(--wa);background:#fff;color:var(--wa);border-radius:8px;padding:5px 10px;font:600 13px system-ui,sans-serif;cursor:pointer}}
.f button.c{{background:var(--wa);color:#fff}}
@media (max-width:560px){{.body{{grid-template-columns:1fr}}.ph img{{width:100%;height:auto;aspect-ratio:1}}}}
</style></head><body><div class="wrap">
<h1>Carga del catálogo en WhatsApp Business</h1>
<div class="help"><b>Cómo cargar cada producto (desde el celular):</b><ol>
<li>Toca <b>Guardar foto</b> para bajar la imagen a tu galería.</li>
<li>En WhatsApp Business: <b>Herramientas para la empresa → Catálogo → Añadir artículo nuevo</b>.</li>
<li>Agrega la foto y pega cada campo con su botón <b>Copiar</b> (Nombre, Precio, Descripción, Enlace y Código de artículo).</li>
<li>Guarda y marca <b>Cargado</b> aquí para no repetirlo.</li>
<li>Al final crea las colecciones <b>Ropa</b>, <b>Calzado</b> y <b>Accesorios y varios</b> y asigna los productos.</li></ol></div>
<div class="prog"><a href="#ropa">Ropa</a><a href="#calzado">Calzado</a><a href="#accesorios">Accesorios</a><b id="cnt"></b></div>
{''.join(cards)}
</div><script>
const KEY="mm-wa-cargados";let done={{}};try{{done=JSON.parse(localStorage.getItem(KEY)||"{{}}")}}catch(e){{}}
const boxes=[...document.querySelectorAll("input[data-id]")];
function upd(){{const n=boxes.filter(b=>b.checked).length;document.getElementById("cnt").textContent=n+" de "+boxes.length+" cargados";}}
boxes.forEach(b=>{{b.checked=!!done[b.dataset.id];b.closest(".card").classList.toggle("ok",b.checked);
 b.onchange=()=>{{done[b.dataset.id]=b.checked;try{{localStorage.setItem(KEY,JSON.stringify(done))}}catch(e){{}};b.closest(".card").classList.toggle("ok",b.checked);upd();}};}});
upd();
document.querySelectorAll("button[data-copy]").forEach(btn=>btn.onclick=async()=>{{
 const t=btn.dataset.copy;try{{await navigator.clipboard.writeText(t)}}catch(e){{const a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();document.execCommand("copy");a.remove();}}
 btn.textContent="Copiado ✓";btn.classList.add("c");setTimeout(()=>{{btn.textContent="Copiar";btn.classList.remove("c")}},1500);}});
</script></body></html>'''
open(os.path.join(R, 'docs', 'whatsapp.html'), 'w', encoding='utf-8').write(page)
print('ok', sum(1 for p in d if p.get('e') != 'vendido'))
