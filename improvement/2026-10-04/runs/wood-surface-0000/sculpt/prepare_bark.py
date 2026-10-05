"""Derive bounded-size local WebP maps from verified CC0 source JPEGs."""
from pathlib import Path
from PIL import Image
import json,hashlib
RUN=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/wood-surface-0000')
root=RUN/'site/public/bark'
rows=[]
for name,size,quality in [('color',768,85),('normal',1024,88),('height',256,85),('roughness',256,85)]:
    source=root/(name+'.jpg');target=root/(name+'.webp')
    assert source.exists() and not target.exists()
    image=Image.open(source).convert('RGB')
    if image.size!=(size,size):image=image.resize((size,size),Image.Resampling.LANCZOS)
    image.save(target,'WEBP',quality=quality,method=6)
    rows.append({'name':name,'original':str(source.relative_to(RUN)),'source_bytes':source.stat().st_size,'derived':str(target.relative_to(RUN)),'bytes':target.stat().st_size,'dimensions':[size,size],'quality':quality,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
(RUN/'qa/bark-runtime-assets.json').write_text(json.dumps({'method':'Pillow resize and WebP encoding. Only runtime texture packaging; no screenshot retouching. Original verified CC0 images retained unchanged.','images':rows,'total_original_bytes':sum(r['source_bytes'] for r in rows),'total_runtime_bytes':sum(r['bytes'] for r in rows)},indent=2)+'\n')
path=RUN/'site/src/materials.js';source=path.read_text();assert "n+'.jpg'" in source
path.write_text(source.replace("n+'.jpg'","n+'.webp'"))
path=RUN/'site/scripts/build.mjs';source=path.read_text();path.write_text(source.replace("['models','draco','stills','still-manifest.json']","['models','draco','stills','still-manifest.json','bark']"))
print(json.dumps({'original_bytes':sum(r['source_bytes'] for r in rows),'runtime_bytes':sum(r['bytes'] for r in rows)}))
