"""A bounded smooth-distance field, not a swept surface or hard voxel union."""
import numpy as np
import argparse,json,time,shutil
from pathlib import Path
from form import BOUNDS,RESOLUTION,GROWTH,EROSION
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--version',required=True);p.add_argument('--resolution',type=int,default=RESOLUTION);a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True);prefix=out/f'hero-{a.version}'
if prefix.with_suffix('.field.f32').exists() or prefix.with_suffix('.json').exists():raise FileExistsError('Use a fresh version')
start=time.monotonic();n=a.resolution
lo=np.array(BOUNDS[0],dtype=np.float32);hi=np.array(BOUNDS[1],dtype=np.float32);step=(hi-lo)/n
field=np.full((n,n,n),2,dtype=np.float32)
axes=[lo[i]+np.arange(n,dtype=np.float32)*step[i] for i in range(3)]
def cat(points,t):
 q=t*(len(points)-1);i=min(len(points)-2,int(q));u=q-i
 a,b,c,d=[points[k] for k in [max(0,i-1),i,i+1,min(len(points)-1,i+2)]]
 return .5*(2*b+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)
def smooth_min(a,b,k):
 h=np.maximum(k-np.abs(a-b),0)/k
 return np.minimum(a,b)-h*h*k*.25
def capsule(a,b,depth,blend,negative=False):
 # Bounding-box work only. Far distances have no influence on the isosurface.
 rad=max(float(a[3]),float(b[3]));margin=rad*max(1,depth)+blend+.025
 first=np.maximum(1,np.floor((np.minimum(a[:3],b[:3])-margin-lo)/step).astype(int))
 last=np.minimum(n-1,np.ceil((np.maximum(a[:3],b[:3])+margin-lo)/step).astype(int)+1)
 if np.any(last<=first):return
 x=axes[0][first[0]:last[0]][None,None,:];y=axes[1][first[1]:last[1]][None,:,None];z=axes[2][first[2]:last[2]][:,None,None]
 qx=x-a[0];qy=(y-a[1])/depth;qz=z-a[2];ab=b[:3]-a[:3];ab[1]/=depth
 t=np.clip((qx*ab[0]+qy*ab[1]+qz*ab[2])/max(float(np.dot(ab,ab)),1e-10),0,1)
 d=np.sqrt((qx-ab[0]*t)**2+(qy-ab[1]*t)**2+(qz-ab[2]*t)**2)-(a[3]+t*(b[3]-a[3]))
 box=(slice(first[2],last[2]),slice(first[1],last[1]),slice(first[0],last[0]))
 current=field[box]
 field[box]=-smooth_min(-current,d,blend) if negative else smooth_min(current,d,blend)

paths=[]
for name,blend,depth,points in GROWTH+EROSION:
 points=np.array(points,dtype=np.float32);length=np.linalg.norm(np.diff(points[:,:3],axis=0),axis=1).sum()
 count=max(12,int(length/.026));samples=[cat(points,i/count) for i in range(count+1)]
 # Each path first unions its segments without accumulating an inflated joint.
 original=field.copy();field.fill(2)
 for left,right in zip(samples,samples[1:]):capsule(left,right,depth,.002)
 route=field;field=original
 if name in [r[0] for r in EROSION]:field=-smooth_min(-field,route,blend)
 else:field=smooth_min(field,route,blend)
 paths.append({'name':name,'blend':blend,'depth':depth,'control':points.tolist(),'sampled':np.array(samples).tolist()})
 print(f'{time.monotonic()-start:.2f}s {name}',flush=True)
# Three.js uses positive density inside; preserve full physical signed distance.
(-field).tofile(prefix.with_suffix('.field.f32'))
meta={'version':a.version,'method':'smooth union of authored spatial growth masses','resolution':n,'bounds':[lo.tolist(),hi.tolist()],'step':step.tolist(),'soil_height':.393,'world_scale':.66,'paths':paths,'field_seconds':time.monotonic()-start}
prefix.with_suffix('.json').write_text(json.dumps(meta,indent=2))
shutil.copy2(__file__,out/f'hero-{a.version}.field.py');shutil.copy2(Path(__file__).parent/'form.py',out/f'hero-{a.version}.form.py')
print(json.dumps({'field':str(prefix.with_suffix('.field.f32')),'seconds':time.monotonic()-start,'bytes':field.nbytes}))
