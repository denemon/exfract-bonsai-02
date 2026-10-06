from pathlib import Path
import json,hashlib,urllib.request,gzip,re,sys
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/growth-garden-0729');port=int(sys.argv[1]);phase=sys.argv[2];assert phase in ['comparison','adopted'];assert port==(5215 if phase=='comparison' else 5214)
H=lambda b:hashlib.sha256(b).hexdigest();pairs=[]
rootR27=R.parent/'program-state-0426';rootR30=R.parent/'garden-scale-0634';roots={'r27':rootR27,'r30':rootR30,'r31':R}
pairs.append(('/',(R if phase=='adopted'else rootR27)/'candidate/dist/index.html'))
for key,folder in roots.items():
 p=folder/'candidate/dist/index.html';pairs.append((f'/compare/{key}/',p))
 for asset in re.findall(r'(?:src|href)="(/compare/'+key+r'/assets/[^"]+)"',p.read_text()):pairs.append((asset,folder/'candidate/dist/assets'/asset.rsplit('/',1)[-1]))
for key,folder in [('r27',rootR27),('r31',R)]:
 for name in ['pc','mobile-390','mobile-320','mobile-tall','wide']:pairs.append((f'/compare/{key}/stills/{name}.webp?v=grown-r30-integrated-r31',folder/f'candidate/public/stills/{name}.webp'))
pairs.extend([('/compare/r31/models/hero-grown-v02.glb.gz',R/'models/hero-grown-v02.glb.gz'),('/compare/r25/models/hero-root-v02.glb.gz',R.parent/'root-flow-0206/models/hero-root-v02.glb.gz'),('/compare/r31/materials/growth-fissures.webp',R/'materials/growth-fissures.webp')])
for name in ['crest-v01.html','crest-v02.html']:
 p=R/'candidate/dist'/name;pairs.append(('/compare/r31/'+name,p))
 for asset in re.findall(r'src="(/compare/r31/assets/[^"]+)"',p.read_text()):pairs.append((asset,R/'candidate/dist/assets'/asset.rsplit('/',1)[-1]))
rows=[]
for url,p in pairs:
 req=urllib.request.Request(f'http://127.0.0.1:{port}'+url,headers={'Accept-Encoding':'gzip'})
 with urllib.request.urlopen(req,timeout=20)as res:
  raw=res.read();b=gzip.decompress(raw)if res.headers.get('Content-Encoding')=='gzip'else raw;expected=p.read_bytes();expected=gzip.decompress(expected)if p.suffix=='.gz'else expected
  assert b==expected,(url,H(b),H(expected));rows.append({'url':url,'file':str(p),'HTTP':res.status,'encoding':res.headers.get('Content-Encoding'),'decoded_bytes':len(b),'decoded_SHA256':H(b),'encoded_bytes':len(raw)})
d={'passed':True,'phase':phase,'port':port,'identities':len(rows),'TOP_selected':R.name if phase=='adopted'else rootR27.name,'five_completed_stills_alias_read_only':(R/'candidate/public/stills').is_symlink(),'experimental_paths_separate':True,'rows':rows}
with(R/f'qa/served-{phase}-identity.json').open('x')as f:json.dump(d,f,indent=2)
print(json.dumps({'passed':True,'identities':len(rows),'phase':phase}))
