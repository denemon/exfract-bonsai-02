import bpy, math, numpy as np, json
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
r=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/hero-rebuild-1016')
bpy.ops.wm.open_mainfile(filepath=str(r/'sculpt/bonsai-structural-study.blend'))
def B(p):return Vector((p[0],-p[2],p[1]))
def cat(P,t):
 n=len(P)-1;k=min(n-1,int(t*n));u=t*n-k;a=P[max(0,k-1)];b=P[k];c=P[k+1];d=P[min(n,k+2)];return .5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)
wood_paths=[[(.02,.53,.01),(-.16,.76,-.13),(.025,.99,-.17),(-.28,1.24,.01),(-.39,1.49,.05),(-.16,1.75,-.07),(.19,1.97,-.09),(.34,2.22,.04),(.32,2.69,-.01)],[(.04,.65,.02),(-.25,.55,.10),(-.59,.518,.26)],[(-.07,.65,-.05),(-.36,.57,-.2),(-.59,.52,-.30)],[(.04,.63,-.1),(.28,.55,-.29),(.43,.522,-.35)],[(.10,.62,.08),(.36,.545,.18),(.65,.521,.14)],[(-.3,1.28,.0),(-.66,1.37,.01),(-.90,1.46,-.05),(-.91,1.60,-.11)],[(-.31,1.56,-.015),(-.51,1.82,-.13),(-.44,2.07,-.21)],[(.14,1.98,-.06),(.43,2.27,-.08),(.44,2.57,-.16)],[(-.05,.89,-.04),(.24,1.06,.09),(.33,1.24,.03)]]
live_paths=[[(.19,.53,.13),(.32,.74,.17),(.21,.97,.21),(-.08,1.22,.20),(-.28,1.47,.175),(-.12,1.70,.06),(.25,1.91,.01),(.43,2.17,.035),(.49,2.48,.01)],[(.23,.60,.12),(.48,.55,.26),(.7,.522,.31)],[(-.26,1.49,.13),(-.60,1.64,.13),(-.96,1.72,.20),(-1.25,1.89,.14)],[(-.16,1.71,.04),(-.41,1.97,.0),(-.65,2.14,.04),(-.91,2.23,.07)],[(.23,1.88,.01),(.61,1.63,.04),(1.03,1.67,.12),(1.31,1.79,.20)],[(.35,2.17,.02),(.60,2.36,.07),(.89,2.51,.02),(1.1,2.54,-.07)],[(.28,2.04,-.05),(.04,2.32,-.22),(.06,2.59,-.26),(.25,2.76,-.30)],[(-.31,1.50,-.02),(-.68,1.80,-.29),(-1.01,1.98,-.40)],[(.26,1.98,-.09),(.67,2.09,-.35),(1.04,2.28,-.38)]]
def flow_uv(obj,paths):
 samples=[]
 for pi,path in enumerate(paths):
  P=[B(p) for p in path];b=Vector((0,1,0));last=None;length=0
  for j in range(250):
   t=j/249;p=cat(P,t);d=(cat(P,min(1,t+.001))-cat(P,max(0,t-.001))).normalized();n=b.cross(d).normalized();b=d.cross(n).normalized()
   if last:length+=(p-last).length
   samples.append((p,n,b,length,pi));last=p
 kd=KDTree(len(samples))
 for i,(p,*_) in enumerate(samples):kd.insert(p,i)
 kd.balance();uv=[]
 for v in obj.data.vertices:
  _,i,_=kd.find(v.co);p,n,b,length,pi=samples[i];q=v.co-p
  uv.append((math.atan2(q.dot(b),q.dot(n))/math.tau+.5,length*.9+pi*.31))
 layer=obj.data.uv_layers.new(name='Wood flow')
 for poly in obj.data.polygons:
  ids=list(poly.loop_indices);us=[uv[obj.data.loops[i].vertex_index][0] for i in ids];seam=max(us)-min(us)>.5
  for i in ids:
   u,v=uv[obj.data.loops[i].vertex_index];layer.data[i].uv=(u+1 if seam and u<.5 else u,v)
 print('Flow UV',obj.name,len(uv),flush=True)
flow_uv(bpy.data.objects['Heartwood sculpt'],wood_paths);flow_uv(bpy.data.objects['Living bark and branch hierarchy'],live_paths)
N=1024;H=2048;u=np.linspace(0,1,N,endpoint=False,dtype=np.float32)[None,:];v=np.linspace(0,1,H,endpoint=False,dtype=np.float32)[:,None]
rng=np.random.default_rng(9406)
def image(name,arr,space):
 im=bpy.data.images.new(name,width=N,height=H,alpha=True);im.colorspace_settings.name=space;im.pixels.foreach_set(arr.astype(np.float32).reshape(-1));im.pack();return im
def surface(matname,living=False):
 flow=u+.006*np.sin(v*math.tau*2+u*13)+.002*np.sin(v*math.tau*9+u*29)
 narrow=np.maximum(0,np.sin(flow*math.tau*(86 if living else 123)+np.sin(v*math.tau*3)*.6))**18
 broad=np.sin(flow*math.tau*23+v*2)*.5+.5
 fine=rng.random((H,N),dtype=np.float32)-.5
 long=.5+.5*np.sin(flow*math.tau*61+np.sin(v*math.tau*2)*.8)
 fissures=narrow*(.5+.5*np.sin(v*math.tau*3+u*25)**2)
 h=.52+long*.12+fine*.06-fissures*(.25 if living else .17)+broad*.04
 tones=(.78+.12*long+.05*broad+.08*fine-fissures*.31)
 base=np.array([.49,.32,.20] if living else [.55,.49,.40],dtype=np.float32)
 # Image values are linear in Blender. Flowing grain has restrained albedo, with real normal relief.
 base=np.where(base<=.04045,base/12.92,((base+.055)/1.055)**2.4)
 al=np.ones((H,N,4),dtype=np.float32);al[:,:,:3]=tones[:,:,None]*base[None,None,:]
 gy,gx=np.gradient(h);normal=np.stack([-gx*3.0,-gy*2.0,np.ones_like(h)*.18],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
 nm=np.ones((H,N,4),dtype=np.float32);nm[:,:,:3]=normal*.5+.5
 a=image(('Bark' if living else 'Shari')+' flow albedo',al,'sRGB');n=image(('Bark' if living else 'Shari')+' flow normal',nm,'Non-Color')
 m=bpy.data.materials[matname];nodes=m.node_tree.nodes;p=nodes.get('Principled BSDF');tex=nodes.new('ShaderNodeTexImage');tex.image=a;m.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
 nt=nodes.new('ShaderNodeTexImage');nt.image=n;no=nodes.new('ShaderNodeNormalMap');no.inputs['Strength'].default_value=.50 if living else .38;m.node_tree.links.new(nt.outputs['Color'],no.inputs['Color']);m.node_tree.links.new(no.outputs['Normal'],p.inputs['Normal']);p.inputs['Roughness'].default_value=.90
surface('Weathered brown heartwood');surface('Living cinnamon bark',True)
for o in bpy.context.scene.objects:o.select_set(o.type=='MESH')
bpy.ops.wm.save_as_mainfile(filepath=str(r/'sculpt/bonsai-structural-study-textured.blend'))
bpy.ops.export_scene.gltf(filepath=str(r/'prototype/public/models/bonsai-structural-study.glb'),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_meshopt_compression_enable=True)
print('TEXTURED COMPRESSED MODEL EXPORTED',flush=True)
