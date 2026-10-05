from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib
RUN=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/wood-surface-0000')
out=RUN/'site/public/bark';out.mkdir(exist_ok=True)
url='https://api.polyhaven.com/files/chinese_cedar_bark'
response=subprocess.run(['curl','--fail','--silent','--show-error','--max-time','20',url],capture_output=True,text=True,check=True)
data=json.loads(response.stdout);selected={}
for kind,name in [('Diffuse','color'),('Displacement','height'),('nor_gl','normal'),('Rough','roughness')]:
 entry=data[kind]['1k']['jpg'];assert entry['size']<2*1024**2
 path=out/f'{name}.jpg';assert not path.exists()
 subprocess.run(['curl','--fail','--silent','--show-error','--max-time','30',entry['url'],'-o',str(path)],check=True)
 content=path.read_bytes();assert len(content)==entry['size'] and hashlib.md5(content).hexdigest()==entry['md5']
 selected[kind]={**entry,'local_file':str(path.relative_to(RUN)),'sha256':hashlib.sha256(content).hexdigest()}
manifest={'asset':'Chinese Cedar Bark','author':'Charlotte Baglioni','asset_page':'https://polyhaven.com/a/chinese_cedar_bark','license':'CC0-1.0','license_page':'https://polyhaven.com/license','legal_code':'https://creativecommons.org/publicdomain/zero/1.0/','api_source':url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'usage':'Actual bark surface maps on the 3D mesh, never a background or replacement scene image.','purchase':False,'files':selected}
(RUN/'qa/bark-source.json').write_text(json.dumps(manifest,indent=2)+'\n')
(RUN/'site/public/bark/README.txt').write_text('Chinese Cedar Bark\nCharlotte Baglioni / Poly Haven\nCC0 1.0\nhttps://polyhaven.com/a/chinese_cedar_bark\nhttps://polyhaven.com/license\nOriginal 1K JPEG texture maps, verified against official API MD5/size. No purchase.\n')
print(json.dumps({k:v['size'] for k,v in selected.items()},indent=2))
