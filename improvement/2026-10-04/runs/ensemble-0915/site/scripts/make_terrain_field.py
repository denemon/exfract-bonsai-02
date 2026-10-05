from pathlib import Path
import argparse,json,hashlib
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--design',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
assert not any(a.output.iterdir()),'Choose a new empty directory'
d=json.loads(a.design.read_text());n=d['size'];xmin,zmin,xmax,zmax=d['domain'];X,Z=np.meshgrid(xmin+(np.arange(n)+.5)/n*(xmax-xmin),zmax-(np.arange(n)+.5)/n*(zmax-zmin))
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def field(cells,seed):
 r=np.random.default_rng(seed).random((cells,cells));u=(X-xmin)/(xmax-xmin)*cells;v=(Z-zmin)/(zmax-zmin)*cells;i=np.floor(u).astype(int);j=np.floor(v).astype(int);f=u-i;g=v-j;f=f*f*(3-2*f);g=g*g*(3-2*g)
 return (1-g)*((1-f)*r[j%cells,i%cells]+f*r[j%cells,(i+1)%cells])+g*((1-f)*r[(j+1)%cells,i%cells]+f*r[(j+1)%cells,(i+1)%cells])
def spline(points):
 points=np.array(points);q=[]
 for k in range(len(points)):
  p0,p1,p2,p3=[points[i%len(points)] for i in [k-1,k,k+1,k+2]]
  for t in np.linspace(0,1,10,endpoint=False):q.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
 return np.array(q)
def signed_distance(points):
 best=np.full(X.shape,1000.);inside=np.zeros(X.shape,dtype=bool)
 for c,b in zip(points,np.roll(points,-1,axis=0)):
  dx,dz=b-c;u=np.clip(((X-c[0])*dx+(Z-c[1])*dz)/(dx*dx+dz*dz),0,1);best=np.minimum(best,(X-c[0]-u*dx)**2+(Z-c[1]-u*dz)**2)
  if abs(dz)>1e-10:inside^=((c[1]>Z)!=(b[1]>Z))&(X<(b[0]-c[0])*(Z-c[1])/dz+c[0])
 return np.sqrt(best)*np.where(inside,-1,1)
distance=np.minimum.reduce([signed_distance(spline(poly)) for poly in d['shores']]);distance+=.025*(field(29,313)-.5)+.011*(field(93,752)-.5)
shore=1-smooth(-.026,.047,distance);loss=np.zeros(X.shape);mounds=np.zeros(X.shape)
for x,z,rx,rz,amp in d['bareHollows']:loss+=amp*np.exp(-2.6*((X-x)**2/rx**2+(Z-z)**2/rz**2))
for x,z,rx,rz,height in d['mounds']+d.get('microRelief',[]):mounds+=height*np.exp(-1.8*((X-x)**2/rx**2+(Z-z)**2/rz**2))
coverage=shore*np.clip(.98-1.12*loss-.15*smooth(.54,.83,field(51,651)),0,1)
soil=np.clip(shore*(.23+.77*(1-coverage))+.24*(1-smooth(.016,.11,np.abs(distance)))*(1-coverage),0,1)
height=np.maximum(0,shore*(.007+mounds-.009*loss+.0014*(field(73,301)-.5)))
array=np.dstack([coverage,soil,np.clip(height/d['heightScale'],0,1),np.ones(X.shape)])
im=Image.fromarray(np.round(np.clip(array,0,1)*255).astype(np.uint8),'RGBA');png=a.output/'terrain-field.png';webp=a.output/'terrain-field.webp';im.save(png,optimize=True);im.save(webp,'WEBP',lossless=True,method=6,exact=True)
assert np.array_equal(np.array(im),np.array(Image.open(webp).convert('RGBA')))
meta={'version':d['version'],'design_sha256':hashlib.sha256(a.design.read_bytes()).hexdigest(),'domain':d['domain'],'baseY':d['baseY'],'heightScale':d['heightScale'],'size':[n,n],'channels':{'R':'moss coverage','G':'exposed organic soil','B':'continuous terrain rise / heightScale','A':'255, avoids canvas premultiplication when reading geometry data'},'colorSpace':'linear data; no sRGB conversion','row_zero':'zmax; Three default flipY=true','pixel_centres':True,'webp_lossless_pixels_verified':True,'maximum_height_metres':float(height.max()),'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [png,webp]}}
(a.output/'terrain-manifest.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
