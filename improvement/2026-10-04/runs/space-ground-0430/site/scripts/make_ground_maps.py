from pathlib import Path
import numpy as np
from PIL import Image
import json,hashlib,argparse
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True,help='New empty output directory; existing assets are never overwritten');args=parser.parse_args()
out=args.output;out.mkdir(parents=True,exist_ok=True);assert not any(out.iterdir()),'Choose an empty output directory'
n=512;rng=np.random.default_rng(260905);yy,xx=np.mgrid[0:n,0:n].astype(np.float64)
def field(cells,seed):
 r=np.random.default_rng(seed).random((cells,cells));u=xx/n*cells;v=yy/n*cells;i=np.floor(u).astype(int);j=np.floor(v).astype(int);a=u-i;b=v-j;a=a*a*(3-2*a);b=b*b*(3-2*b)
 return (1-b)*((1-a)*r[j%cells,i%cells]+a*r[j%cells,(i+1)%cells])+b*((1-a)*r[(j+1)%cells,i%cells]+a*r[(j+1)%cells,(i+1)%cells])
cells=73;u=xx/n*cells;v=yy/n*cells;i=np.floor(u).astype(int);j=np.floor(v).astype(int);fx=u-i;fy=v-j;sites=rng.random((cells,cells,3));best=np.full((n,n),9.);second=best.copy();tone=np.zeros((n,n))
for oy in [-1,0,1]:
 for ox in [-1,0,1]:
  s=sites[(j+oy)%cells,(i+ox)%cells];dx=ox+.16+.68*s[:,:,0]-fx;dy=oy+.16+.68*s[:,:,1]-fy;d=dx*dx+dy*dy;hit=d<best;second=np.where(hit,best,np.minimum(second,d));tone=np.where(hit,s[:,:,2],tone);best=np.minimum(best,d)
border=np.sqrt(second)-np.sqrt(best);rounding=np.clip(border/.105,0,1);rounding=rounding*rounding*(3-2*rounding);height=rounding*(.62+.27*np.clip(1-np.sqrt(best),0,1))
# Dry sub-centimetre grit. Color variations are modest; joints never pure black.
brightness=.375+.09*tone+.022*(field(5,44)-.5)-.047*(1-rounding)+.006*(field(193,91)-.5)
rgb=np.stack([brightness*1.00,brightness*1.015,brightness*.968],axis=-1)
gravel=np.dstack([np.clip(rgb,0,1),height]);
coarse=field(5,740);middle=field(17,330);tips=field(91,321);fine=field(207,730)
density=.25*coarse+.32*middle+.28*tips+.15*fine
# A continuous small moss material, not pasted individual photographic tufts.
moss_rgb=np.stack([.215+.055*density,.263+.081*density,.109+.055*density],axis=-1)
moss_h=np.clip(.23*coarse+.24*middle+.36*tips+.17*fine,0,1)
moss=np.dstack([moss_rgb,moss_h]);manifest=[]
for name,array,metres in [('mineral',gravel,.36),('moss',moss,.42)]:
 p=out/f'{name}.png';assert not p.exists();Image.fromarray(np.round(np.clip(array,0,1)*255).astype(np.uint8),'RGBA').save(p,optimize=True)
 manifest.append({'name':name,'file':p.name,'dimensions':[n,n],'repeat_metres':metres,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'RGB':'dry material color, sRGB','alpha':'linear micro-height; no transparency use'})
assert sum(x['bytes'] for x in manifest)<1048576
(out/'manifest.json').write_text(json.dumps({'author':'Procedural material generated locally for this project','sources':'No external image or paid asset','generator':'make_ground_maps.py; NumPy1/Pillow; deterministic seeds','maps':manifest},indent=2)+'\n');print(json.dumps(manifest,indent=2))
