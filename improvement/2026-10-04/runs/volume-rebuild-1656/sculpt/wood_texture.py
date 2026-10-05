"""Own tileable wood data texture; grain, relief, checks, mottling in RGBA.

No photography, image generation, external texture or baked lighting is used.
Mip filtering replaces fragment-noise derivatives that produced a woven alias.
"""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
W,H=1024,2048;rng=np.random.default_rng(51004)
def noise(nx,ny):
 grid=rng.random((ny,nx),dtype=np.float32)
 tile=np.tile(grid,(3,3));image=Image.fromarray(tile,mode='F').resize((W*3,H*3),Image.Resampling.BICUBIC)
 return np.asarray(image,dtype=np.float32)[H:2*H,W:2*W].copy()
y,x=np.mgrid[:H,:W];warp=(noise(12,17)-.5)*W*.029+(noise(37,9)-.5)*W*.009
def bend(v):
 q=(x+warp)%W;i=np.floor(q).astype(np.int32);f=q-i
 return v[y,i]*(1-f)+v[y,(i+1)%W]*f
broad=bend(noise(51,8));fibres=bend(noise(271,29));fine=bend(noise(720,130));mottle=noise(23,39)
grain=np.clip(.5+(broad-.5)*.65+(fibres-.5)*.30+(fine-.5)*.14,0,1)
height=np.clip(.5+(fibres-.5)*.62+(broad-.5)*.15+(fine-.5)*.11,0,1)
checks=np.clip((.25-fibres)*7,0,1)**1.5*np.clip((noise(69,53)-.29)*2,0,1)
array=(np.stack([grain,height,checks,mottle],axis=-1)*255).round().astype('uint8')
path=out/'wood-grain.webp';Image.fromarray(array[:,:,:3],'RGB').save(path,quality=95,method=6)
decoded=np.asarray(Image.open(path).convert('RGB'),dtype=np.float32);error=np.abs(decoded-array[:,:,:3])
(out/'wood-grain.json').write_text(json.dumps({'kind':'authored material data; no lighting','size':[W,H],'channels':['fibre colour','surface height','broken checks'],'seed':51004,'compression_mae_255':error.mean(axis=(0,1)).tolist(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size},indent=2));print(path.stat().st_size)
