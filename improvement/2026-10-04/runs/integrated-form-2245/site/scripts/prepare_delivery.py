from pathlib import Path
import json, hashlib, base64, io, shutil
from PIL import Image

RUN=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/integrated-form-2245')
site=RUN/'site'
dest=site/'public/stills'
dest.mkdir(exist_ok=True)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
model=RUN/'models/integrated-v03.glb'
capture=json.loads((RUN/'qa/selected-stills/results.json').read_text())
assert not capture['logs']
manifest={'purpose':'Same selected real-WebGL scene, used while loading or without WebGL. This is an unfinished integrated study, not a finished garden.','model':str(model.relative_to(RUN)),'model_sha256':digest(model),'version':'integrated-v03','images':[]}
inline={}
for row in capture['results']:
    name=row['name'];src=RUN/'qa/selected-stills'/f'{name}.png'
    assert row['stats']['model']['authoringVersion']=='integrated-v03'
    im=Image.open(src).convert('RGB')
    out=dest/f'{name}.webp';im.save(out,'WEBP',quality=88,method=6)
    tiny=im.copy();tiny.thumbnail((384,384));buf=io.BytesIO();tiny.save(buf,'WEBP',quality=44,method=6)
    inline[name]='data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()
    manifest['images'].append({'name':name,'source':str(src.relative_to(RUN)),'source_sha256':digest(src),'source_url':row['url'],'viewport':row['viewport'],'camera':row['stats']['camera'],'full_webp':str(out.relative_to(site/'public')),'webp_sha256':digest(out),'webp_bytes':out.stat().st_size,'inline_dimensions':tiny.size,'inline_bytes':len(buf.getvalue()),'conversion':'Pillow lossless PNG decode; WebP quality 88 full, quality 44 thumbnail; no compositing or image alteration'})
(site/'public/still-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
critical=(site/'src/style.css').read_text()
critical+='\nmain{background-image:url("'+inline['pc']+'")}\n'
critical+='@media(orientation:portrait){main{background-image:url("'+inline['mobile-390']+'")}}\n'
critical+='@media(orientation:portrait) and (max-width:350px){main{background-image:url("'+inline['mobile-320']+'")}}\n'
critical+='@media(max-aspect-ratio:2/5){main{background-image:url("'+inline['mobile-tall']+'")}}\n'
html='''<!doctype html>
<html lang="ja">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title></title><link rel="icon" href="data:,"><style>CRITICAL</style></head>
<body><main>
<picture aria-hidden="true">
<source media="(max-aspect-ratio:2/5)" srcset="/stills/mobile-tall.webp">
<source media="(orientation:portrait) and (max-width:350px)" srcset="/stills/mobile-320.webp">
<source media="(orientation:portrait)" srcset="/stills/mobile-390.webp">
<img src="/stills/pc.webp" alt="" fetchpriority="high" decoding="async">
</picture>
<canvas aria-label="静かな庭に置かれた盆栽"></canvas>
</main><script type="module" src="/src/main.js"></script></body>
</html>
'''.replace('CRITICAL',critical)
(site/'index.html').write_text(html)
package=json.loads((site/'package.json').read_text());package['scripts']['build']='node scripts/build.mjs'
(site/'package.json').write_text(json.dumps(package,indent=2)+'\n')
(site/'scripts/build.mjs').write_text('''import {build} from 'vite';
import {symlink,readlink} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
const root=fileURLToPath(new URL('../',import.meta.url));
await build({root,configFile:false,build:{copyPublicDir:false}});
// The local review build shares immutable model/decoder/stills instead of copying them.
for(const name of ['models','draco','stills','still-manifest.json']){
  const path=resolve(root,'dist',name),target='../public/'+name;
  try{await symlink(target,path);}catch(e){if(e.code!=='EEXIST'||await readlink(path)!==target)throw e;}
}
''')
integrate=RUN/'sculpt/integrate.py'
source=integrate.read_text()
old="core['wood_basis']=a.base"
new=old+";core['source_control_record']=str(out/f'{a.base}.json');core['status']='integrated editing study; aged deadwood and whole garden unfinished'"
if new not in source:
    assert source.count(old)==1
    integrate.write_text(source.replace(old,new))
if Path(__file__).parent != site/'scripts':
    shutil.copy2(Path(__file__).with_name('fix_model_metadata.py'),RUN/'sculpt/fix_model_metadata.py')
    shutil.copy2(Path(__file__),RUN/'site/scripts/prepare_delivery.py')
print(json.dumps({'images':len(manifest['images']),'html_bytes':len(html.encode()),'stills_bytes':sum(x['webp_bytes'] for x in manifest['images']),'model_sha256':manifest['model_sha256']},indent=2))
