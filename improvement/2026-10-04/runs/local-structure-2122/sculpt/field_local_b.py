"""Local positive-volume repair. Stream the density to extraction; no raw field file."""
import numpy as np,gzip,json,sys,subprocess,time,hashlib,shutil
from pathlib import Path
r=Path(__file__).resolve().parent.parent;base=r.parent/'volume-rebuild-1656/models/hero-v20';prefix=r/'models/local-b';assert not prefix.with_suffix('.glb').exists();assert shutil.disk_usage(r).free>2*1024**3
start=time.monotonic();meta=json.loads(base.with_suffix('.json').read_text());n=meta['resolution'];lo=np.array(meta['bounds'][0],np.float32);hi=np.array(meta['bounds'][1],np.float32);step=(hi-lo)/n
with gzip.open(base.with_suffix('.field.f32.gz'),'rb') as f:field=-np.frombuffer(f.read(),dtype=np.float32).reshape((n,n,n)).copy()
axes=[lo[i]+np.arange(n,dtype=np.float32)*step[i] for i in range(3)]
def smin(a,b,k):
 h=np.maximum(k-np.abs(a-b),0)/k;return np.minimum(a,b)-h*h*k*.25
# Remove only the old rooted base below the transition. The complete upper
# branching structure and canopy guide arrangement are retained.
field=np.maximum(field,.225-axes[2][:,None,None])
def cat(points,t):
 q=t*(len(points)-1);i=min(len(points)-2,int(q));u=q-i;a,b,c,d=[points[k] for k in [max(0,i-1),i,i+1,min(len(points)-1,i+2)]];return .5*(2*b+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)
repairs=[
 ('dominant left root flare',.090,1.03,[(.075,.075,.32,.172),(-.09,.050,.15,.175),(-.285,.055,.045,.130),(-.435,.075,-.045,.093),(-.55,.055,-.14,.062)]),
 ('front descending buttress',.080,1.10,[(.085,-.045,.25,.135),(.065,-.115,.135,.137),(.042,-.215,.025,.113),(.018,-.33,-.095,.070)]),
 ('right anchoring root',.070,1.00,[(.155,.060,.245,.132),(.270,.006,.106,.103),(.425,-.09,.003,.070),(.54,-.17,-.105,.033)]),
 ('rear root ridge',.075,1.0,[(.055,.135,.245,.145),(.015,.260,.082,.102),(-.16,.355,-.053,.073),(-.295,.38,-.125,.030)]),
 ('lower shoulder supporting wood',.075,.93,[(-.08,.015,.38,.130),(-.225,-.015,.52,.129),(-.345,-.035,.65,.121),(-.305,.008,.77,.104)]),
 ('upper deadwood supporting volume',.065,1.02,[(-.20,.025,.815,.091),(-.15,.009,.955,.096),(-.06,.013,1.085,.085),(.04,.055,1.192,.058)])
]
for name,blend,depth,points in repairs:
 points=np.array(points,np.float32);length=np.linalg.norm(np.diff(points[:,:3],axis=0),axis=1).sum();count=max(12,int(length/.008));samples=np.array([cat(points,i/count) for i in range(count+1)])
 margin=max(points[:,3])*max(1,depth)+blend+.03;first=np.maximum(1,np.floor((samples[:,:3].min(axis=0)-margin-lo)/step).astype(int));last=np.minimum(n-1,np.ceil((samples[:,:3].max(axis=0)+margin-lo)/step).astype(int)+1);box=(slice(first[2],last[2]),slice(first[1],last[1]),slice(first[0],last[0]));shape=tuple((last-first)[::-1]);local=np.full(shape,2,np.float32)
 x=axes[0][first[0]:last[0]][None,None,:];y=axes[1][first[1]:last[1]][None,:,None];z=axes[2][first[2]:last[2]][:,None,None]
 for a,b in zip(samples,samples[1:]):
  qx=x-a[0];qy=(y-a[1])/depth;qz=z-a[2];ab=b[:3]-a[:3];ab[1]/=depth;t=np.clip((qx*ab[0]+qy*ab[1]+qz*ab[2])/max(float(np.dot(ab,ab)),1e-9),0,1);dx=qx-ab[0]*t;dy=qy-ab[1]*t;dz=qz-ab[2]*t;d=np.sqrt(dx*dx+dy*dy+dz*dz)-(a[3]+t*(b[3]-a[3]));np.minimum(local,d,out=local)
 field[box]=smin(field[box],local,blend)
 record={'name':name,'blend':blend,'depth':depth,'control':points.tolist(),'sampled':samples.tolist()};found=next((i for i,p in enumerate(meta['paths']) if p['name']==name),None)
 if found is None:meta['paths'].append(record)
 else:meta['paths'][found]=record
 print(name,round(time.monotonic()-start,2),flush=True)
# Three shallow, uneven losses anchored to the actual front surface. Positive
# structure is repaired first so these cannot create the paper shells of A.
losses=[]
for cx,cz,rx,rz,depth in [(-.21,.515,.074,.160,.020),(-.35,.710,.110,.060,.026),(-.115,1.035,.047,.125,.018)]:
 ix=int(round((cx-lo[0])/step[0]));iz=int(round((cz-lo[2])/step[2]));inside=np.flatnonzero(field[iz,:,ix]<0)
 if not len(inside):raise RuntimeError('The loss is not on a supporting wood mass')
 sy=float(axes[1][inside[0]]);ry=.08;cy=sy-ry+depth;centre=np.array([cx,cy,cz]);radii=np.array([rx,ry,rz]);first=np.maximum(1,np.floor((centre-radii-.015-lo)/step).astype(int));last=np.minimum(n-1,np.ceil((centre+radii+.015-lo)/step).astype(int)+1);box=(slice(first[2],last[2]),slice(first[1],last[1]),slice(first[0],last[0]));x=axes[0][first[0]:last[0]][None,None,:];y=axes[1][first[1]:last[1]][None,:,None];z=axes[2][first[2]:last[2]][:,None,None]
 # A small shear and nonuniform wall depth avoid repeated aligned ovals.
 qx=(x-cx+.16*(z-cz))/rx;qy=(y-cy)/ry;qz=(z-cz)/rz;distance=(np.sqrt(qx*qx+qy*qy+qz*qz)-1)*min(radii);field[box]=-smin(-field[box],distance,.008);losses.append({'centre':[cx,cy,cz],'radii':radii.tolist(),'surface_y':sy,'depth':depth})
field=np.maximum(field,-.064-axes[2][:,None,None]);meta.update(version='local-b',method='retained upper volume with locally rebuilt rooted buttresses and supporting deadwood masses',local_repairs=repairs,shallow_losses=losses,source_field_sha256='8accedd5-placeholder',seconds_before_extraction=time.monotonic()-start)
# The original field archive is retained unchanged; its manifest holds the raw hash.
meta['source_field_archive']=str(base.with_suffix('.field.f32.gz'));meta['source_field_sha256']=hashlib.sha256(base.with_suffix('.field.f32.gz').read_bytes()).hexdigest();prefix.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n');field*=-1
process=subprocess.Popen(['node',str(r/'sculpt/extract_stream.mjs'),str(prefix)],stdin=subprocess.PIPE,cwd=r)
for layer in field:process.stdin.write(layer.tobytes())
process.stdin.close();assert process.wait()==0;print('Streamed field; no raw field written',round(time.monotonic()-start,2),flush=True)
