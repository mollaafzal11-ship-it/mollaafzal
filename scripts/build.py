from pathlib import Path
import json, re, html
ROOT=Path(__file__).resolve().parents[1]
BASE="https://mollaafzal.netlify.app"

def read(p):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return None

def esc(v): return html.escape(str(v or ""), quote=True)

def meta(doc, pattern, value):
    return re.sub(pattern, lambda m:m.group(1)+esc(value)+m.group(3), doc, count=1, flags=re.I|re.S)

def section(s):
    t=s.get("type","text")
    if t=="text":
        h=f'<h2 class="section-title">{esc(s.get("heading"))}</h2>' if s.get("heading") else ""
        paras="".join(f"<p>{esc(x.strip())}</p>" for x in s.get("body","").split(chr(10)+chr(10)) if x.strip())
        return f'<section class="content"><div class="wrap">{h}<div class="body-copy">{paras}</div></div></section>'
    if t=="cards":
        cards=[]
        for item in s.get("items",[]):
            li="".join(f"<li>{esc(x)}</li>" for x in item.get("items",[]))
            cards.append(f'<article class="card"><h2>{esc(item.get("title"))}</h2><ul class="list">{li}</ul></article>')
        return f'<section class="content"><div class="wrap"><div class="grid">{"".join(cards)}</div></div></section>'
    if t=="image_text":
        return f'<section class="content"><div class="wrap"><div class="card"><h2>{esc(s.get("heading"))}</h2><p>{esc(s.get("body"))}</p><img src="{esc(s.get("image"))}" alt="{esc(s.get("heading"))}" loading="lazy" style="max-width:100%;height:auto"></div></div></section>'
    if t=="cta":
        return f'<section class="content"><div class="wrap"><div class="cta"><h2 class="section-title">{esc(s.get("heading"))}</h2><p class="body-copy">{esc(s.get("text"))}</p><a class="button primary" href="{esc(s.get("button_url") or "/#contact")}">{esc(s.get("button_text") or "Get in touch")} ↗</a></div></div></section>'
    return ""

def new_page(d,url):
    title=d.get("seo_title") or d.get("title") or "Molla Afzal"
    desc=d.get("seo_description") or d.get("description") or d.get("short_description") or d.get("summary") or ""
    h=d.get("hero_heading") or d.get("title") or ""
    lead=d.get("hero_description") or d.get("description") or d.get("short_description") or d.get("summary") or ""
    blocks="".join(section(x) for x in d.get("sections",[]))
    if not blocks and d.get("body"): blocks=section({"type":"text","body":d["body"]})
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{esc(url)}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(url)}"><style>:root{{color-scheme:dark;--bg:#20201e;--panel:#292927;--text:#f5f2ec;--muted:#aaa8a1;--orange:#e87943;--line:rgba(245,242,236,.15);--serif:Georgia,serif}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.65 Inter,Arial,sans-serif}}a{{color:inherit}}.wrap{{width:min(1120px,calc(100% - 40px));margin:auto}}header{{padding:22px 0;border-bottom:1px solid var(--line)}}nav{{float:right;display:flex;gap:20px}}nav a{{color:var(--muted);text-decoration:none;font-size:13px}}.hero{{padding:80px 0 50px}}.eyebrow{{color:var(--orange);letter-spacing:.16em;text-transform:uppercase;font-size:11px}}h1{{font-size:clamp(42px,7vw,76px);line-height:1.05}}.lead,.body-copy,.card li{{color:var(--muted)}}section.content{{padding:32px 0 56px}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.card,.cta{{padding:25px;border:1px solid var(--line);border-radius:16px;background:var(--panel)}}.list li{{margin:8px 0}}.button{{display:inline-block;padding:12px 18px;border:1px solid var(--orange);text-decoration:none}}footer{{padding:25px 0;border-top:1px solid var(--line);color:var(--muted)}}@media(max-width:700px){{nav{{float:none;margin-top:12px;flex-wrap:wrap}}.grid{{grid-template-columns:1fr}}}}</style></head><body><header><div class="wrap"><a href="/">AFZAL · DIGITAL MARKETING</a><nav><a href="/">Home</a><a href="/services/">Services</a><a href="/#work">Selected work</a><a href="/#contact">Contact</a></nav></div></header><main><section class="hero"><div class="wrap"><div class="eyebrow">Molla Afzal · Digital Marketing</div><h1>{esc(h)}</h1><p class="lead">{esc(lead)}</p></div></section>{blocks}</main><footer><div class="wrap">© 2026 Molla Afzal · <a href="/">Home</a> · <a href="/#contact">Contact</a></div></footer><script src="/cms-loader.js"></script></body></html>'''

def main():
    home=read(ROOT/"cms/homepage.json") or {}
    index=ROOT/"index.html"
    if index.exists():
        d=index.read_text(encoding="utf-8")
        if home.get("seo_title"): d=re.sub(r"<title>.*?</title>",f"<title>{esc(home['seo_title'])}</title>",d,count=1,flags=re.I|re.S)
        if home.get("seo_description"): d=meta(d,r'(<meta name="description" content=")([^"]*)(")',home["seo_description"])
        index.write_text(d,encoding="utf-8")
    urls={BASE+"/"}
    sm=ROOT/"sitemap.xml"
    if sm.exists(): urls.update(re.findall(r"<loc>(.*?)</loc>",sm.read_text(encoding="utf-8")))
    for folder in ("services","pages","projects"):
        source=ROOT/"cms"/folder
        if not source.exists(): continue
        for f in source.glob("*.json"):
            d=read(f)
            if not d: continue
            slug=re.sub(r"[^a-z0-9-]","",(d.get("slug") or f.stem).lower().replace(" ","-"))
            if not slug: continue
            url=f"{BASE}/{folder}/{slug}/"
            target=ROOT/folder/slug/"index.html"
            if folder=="services" and target.exists():
                doc=target.read_text(encoding="utf-8")
                title=d.get("seo_title") or d.get("title")
                desc=d.get("seo_description") or d.get("short_description")
                if title: doc=re.sub(r"<title>.*?</title>",f"<title>{esc(title)}</title>",doc,count=1,flags=re.I|re.S)
                if desc: doc=meta(doc,r'(<meta name="description" content=")([^"]*)(")',desc)
                if d.get("hero_heading"): doc=re.sub(r"<h1[^>]*>.*?</h1>",f"<h1>{esc(d['hero_heading'])}</h1>",doc,count=1,flags=re.I|re.S)
                if d.get("hero_description"): doc=re.sub(r'(<p class="lead">).*?(</p>)',lambda m:m.group(1)+esc(d["hero_description"])+m.group(2),doc,count=1,flags=re.I|re.S)
                if d.get("sections"):
                    blocks="".join(section(x) for x in d["sections"])
                    doc=re.sub(r'<section class="content">.*?</section>(?=</main>)',blocks,doc,count=1,flags=re.S)
                if 'cms-loader.js' not in doc: doc=doc.replace('</body>', '<script src="/cms-loader.js"></script></body>')
                target.write_text(doc,encoding="utf-8")
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text(new_page(d,url),encoding="utf-8")
            urls.add(url)
    sm.write_text('<?xml version="1.0" encoding="UTF-8"?>'+chr(10)+'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+chr(10)+"".join(f"  <url><loc>{html.escape(u)}</loc></url>"+chr(10) for u in sorted(urls))+"</urlset>"+chr(10),encoding="utf-8")
    print("CMS build complete")

if __name__=="__main__": main()
