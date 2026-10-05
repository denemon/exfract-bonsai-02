from pathlib import Path
from PIL import Image
import json,hashlib,argparse
R=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=R/'assets/source');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();out=args.output;assert not out.exists(),'Choose a new empty output directory';out.mkdir(parents=True);rows=[]
for asset in ['boulder_01','rock_09']:
 for name,quality,size in [('diff',86,1024),('nor_gl',90,1024),('arm',None,512)]:
  source=args.source/asset/'textures'/(asset+'_'+name+'_1k.jpg');p=out/(asset+'_'+name+'.webp');assert not p.exists();im=Image.open(source).convert('RGB');im.thumbnail((size,size),Image.Resampling.LANCZOS)
  if quality:im.save(p,'WEBP',quality=quality,method=6)
  else:im.save(p,'WEBP',lossless=True,method=6)
  rows.append({'source':str(source),'output':str(p.relative_to(out)),'dimensions':list(im.size),'quality':quality,'lossless':quality is None,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(out/'texture-manifest.json').write_text(json.dumps({'files':rows,'runtime_bytes':sum(r['bytes']for r in rows),'conversion_only':'Color and tangent normal preserve1024px; packed ambient/roughness/metal reduced to512px lossless output. Source JPEGs retained.'},indent=2)+'\n');print(json.dumps({'runtime_map_bytes':sum(r['bytes']for r in rows),'maps':len(rows)}))
