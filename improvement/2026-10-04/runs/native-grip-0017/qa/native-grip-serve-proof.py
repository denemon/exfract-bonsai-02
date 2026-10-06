from pathlib import Path
import json,urllib.request,hashlib,re,gzip
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/native-grip-0017');D=R.parent;origin='http://127.0.0.1:5214';sha=lambda b:hashlib.sha256(b).hexdigest();rows=[]
def read(url):
 with urllib.request.urlopen(origin+url)as r:
  b=r.read();return gzip.decompress(b)if r.headers.get('Content-Encoding')=='gzip'else b
for key,run in [('',D/'steady-render-2225'),('r20',D/'depth-balance-1905'),('r21',D/'layer-balance-2055'),('r22',D/'steady-render-2225'),('r23',R)]:
 prefix='/compare/'+key if key else '';path=prefix+'/';body=read(path);expected=(run/'candidate/dist/index.html').read_bytes()
 if key in ['r20','r21']:expected=expected.decode().replace('="/assets/','="'+prefix+'/assets/').replace('/stills/',prefix+'/stills/').encode()
 assert body==expected,(key,'html');rows.append({'url':path,'decoded_sha256':sha(body),'matches_disk':True})
 if key not in ['', 'r22','r23']:continue
 for u in re.findall(r'(?:src|href)="([^"]+\.(?:js|css))"',body.decode()):
  data=read(u);p=run/'candidate/dist/assets'/Path(u).name;assert data==p.read_bytes(),u;rows.append({'url':u,'decoded_sha256':sha(data),'matches_disk':True})
 staticprefix='/compare/r22'if key in ['', 'r22']else'/compare/r23'
 for n in ['pc','mobile-390','mobile-320','mobile-tall','wide']:
  u=staticprefix+'/stills/'+n+'.webp';data=read(u);p=run/'candidate/public/stills'/Path(u).name;assert data==p.read_bytes();rows.append({'url':u,'decoded_sha256':sha(data),'matches_disk':True})
(R/'qa/final-served-identity.json').write_text(json.dumps({'rows':rows,'selected_root':'R22 selected dist unchanged','trial':'R23 gray diagnostic, unadopted'},indent=2)+'\n');print('decoded served identities',len(rows))
