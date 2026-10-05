"""Build same-scene fallbacks from the selected actual Mac WebGL captures."""
from pathlib import Path
from PIL import Image
import json,hashlib,base64,io,argparse
args=argparse.ArgumentParser();args.add_argument('--version',required=True);args=args.parse_args()
RUN=Path(__file__).resolve().parents[2]
site=RUN/'site';dest=site/'public/stills';dest.mkdir(exist_ok=True)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
model=site/'public/models/hero.glb'
capture=json.loads((RUN/'qa/selected-stills/results.json').read_text())
assert not capture['logs']
manifest={'purpose':'Same selected real-WebGL scene for loading and unavailable WebGL. Selected night-B space-v2 with unchanged hero and cameras; architecture, room illumination and two CC0 garden rocks revised; premium natural quality and major aged form remain unfinished.','model':str(model.relative_to(RUN)),'model_sha256':digest(model),'version':args.version,'material_file_sha256':digest(site/'src/materials.js'),'scene_source_sha256':{p.name:digest(p) for p in (site/'src').glob('*.js')},'layout':'night-b','terrain_design_sha256':digest(site/'src/terrain-design.json'),'planting_version':'growth-v2','space_version':'space-v2','images':[]}
inline={}
for row in capture['results']:
    name=row['name']
    if name not in ['pc','mobile-390','mobile-320','mobile-tall','wide']:continue
    src=RUN/'qa/selected-stills'/f'{name}.png'
    assert row['stats']['model']['authoringVersion']==args.version and row['stats']['layout']=='night-b'
    image=Image.open(src).convert('RGB');output=dest/f'{name}.webp'
    image.save(output,'WEBP',quality=88,method=6)
    tiny=image.copy();tiny.thumbnail((384,384));buf=io.BytesIO();tiny.save(buf,'WEBP',quality=44,method=6)
    inline[name]='data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()
    manifest['images'].append({'name':name,'source':str(src.relative_to(RUN)),'source_sha256':digest(src),'source_url':row['url'],'viewport':row['viewport'],'camera':row['stats']['camera'],'full_webp':str(output.relative_to(site/'public')),'webp_sha256':digest(output),'webp_bytes':output.stat().st_size,'inline_dimensions':tiny.size,'inline_bytes':len(buf.getvalue()),'conversion':'PNG decode, WebP quality88 and small thumbnail quality44; no compositing or screenshot retouching'})
assert len(inline)==5
manifest['rock_assets_sha256']={p.name:digest(p) for p in (site/'public/rocks').iterdir() if p.is_file()}
manifest['rock_provenance_sha256']=digest(RUN/'assets/provenance.json')
manifest['garden_materials_sha256']={p.name:digest(p) for p in (site/'public/garden').glob('*.webp')}
(site/'public/still-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
css=(site/'src/style.css').read_text()
css+='\nmain{background-image:url("'+inline['pc']+'")}\n'
css+='@media(orientation:portrait){main{background-image:url("'+inline['mobile-390']+'")}}\n'
css+='@media(orientation:portrait) and (max-width:350px){main{background-image:url("'+inline['mobile-320']+'")}}\n'
css+='@media(max-aspect-ratio:2/5){main{background-image:url("'+inline['mobile-tall']+'")}}\n'
css+='@media(min-aspect-ratio:2/1){main{background-image:url(\"'+inline['wide']+'\")}}\n'
html='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title><link rel="icon" href="data:,"><style>CRITICAL</style></head><body><main>
<picture aria-hidden="true">
<source media="(min-aspect-ratio:2/1)" srcset="/stills/wide.webp">
<source media="(max-aspect-ratio:2/5)" srcset="/stills/mobile-tall.webp">
<source media="(orientation:portrait) and (max-width:350px)" srcset="/stills/mobile-320.webp">
<source media="(orientation:portrait)" srcset="/stills/mobile-390.webp">
<img src="/stills/pc.webp" alt="" fetchpriority="high" decoding="async"></picture>
<canvas aria-label="静かな夜の庭に置かれた盆栽"></canvas></main><script type="module" src="/src/main.js"></script></body></html>
'''.replace('CRITICAL',css)
(site/'index.html').write_text(html)
print(json.dumps({'images':5,'html_bytes':len(html.encode()),'stills_bytes':sum(x['webp_bytes'] for x in manifest['images']),'model_sha256':manifest['model_sha256']},indent=2))
