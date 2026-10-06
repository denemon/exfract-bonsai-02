from pathlib import Path
import json,hashlib,io,base64,re
from PIL import Image
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/organic-ensemble-1017');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();p=R/'candidate/index.html';t=p.read_text();names=['pc','wide','mobile-390','mobile-320','mobile-tall'];images=[];rows=[]
assert not(R/'candidate/public/stills').is_symlink()
for n in names:
 f=R/'candidate/public/stills'/f'{n}.webp';im=Image.open(f);dims=im.size;im.thumbnail((160,208));out=io.BytesIO();im.save(out,format='WEBP',quality=68,method=6);images.append(base64.b64encode(out.getvalue()).decode());rows.append({'name':n,'size':dims,'fullSHA256':H(f),'inlineSHA256':hashlib.sha256(out.getvalue()).hexdigest(),'ownNewCapture':True})
it=iter(images);t,k=re.subn(r'data:image/webp;base64,[A-Za-z0-9+/=]+',lambda m:'data:image/webp;base64,'+next(it),t);assert k==5
t=re.sub(r'(/compare/r34/stills/[a-z0-9-]+\.webp)(?:\?v=[a-zA-Z0-9_-]+)?',r'\1?v=organic-r34-final-v02',t);p.write_text(t)
(R/'qa/completed-inline-sync.json').write_text(json.dumps({'selectedFinalScene':'living-v01/normal-aged-growth-v01/organic-occupied-v02/stable','actualFiveFrames':'qa/completed-scene-five-verification/results.json','fiveIndependentDefaultCompositions':True,'inlineAndFullSameCompletedScene':True,'entries':rows},indent=2)+'\n')
files=['candidate/src/main.js','candidate/src/render-partition.js','candidate/src/native-wood-material.js','candidate/src/native-wood-material-r31.js','candidate/src/foliage-lod.js','candidate/src/study-light.js','candidate/src/shadow-filter.js','candidate/index.html','background/scene.js','background/garden-geometry.js','background/garden-materials.js','background/terrain-field.js','background/distant-crowns.js','background/broadleaf-support.js','materials/aged-growth-v01.webp'];(R/'selected-scene-freeze.json').write_text(json.dumps({'selected':'living-v01/aged-growth-v01/organic-occupied-v02','sourceSHA256':{n:H(R/n)for n in files},'fixedNativeSevenSHA256':json.loads((R/'qa/fixed-living-shape-v01.json').read_text()),'sourceFrozenBeforeQualification':True,'overallCompletion':False},indent=2)+'\n')
print('Own actual5completedWebP and inline5 synchronized; source frozen.')
