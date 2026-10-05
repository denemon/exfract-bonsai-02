"""Finite volume blocking, unequal buttresses, then actual short wedge relief carving.
The editable output is a sculptable surface, not a fixed low-point body cell.
"""
from pathlib import Path
import bpy,bmesh,json,math,os,hashlib
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];plan=json.loads((R/'design/sculpt-plan.json').read_text());version='carved-v01';assert not(R/'models'/f'{version}.glb').exists();assert os.statvfs(R).f_bavail*os.statvfs(R).f_frsize>=2147483648
bpy.ops.wm.read_factory_settings(use_empty=True);parts=[]
def normals(obj):
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
 bm.to_mesh(obj.data);bm.free()
def mass(v):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16);o=bpy.context.object;o.name=v['id'];rot=Matrix.Rotation(math.radians(v['tilt']),3,'Y');c=Vector(v['center']);r=v['radii']
 for p in o.data.vertices:
  q=p.co.copy();w=1+.052*math.sin(q.x*3.1+q.z*2.4+len(parts))+.028*math.sin(q.y*5.1-q.z*1.7);q=Vector((q.x*r[0]*w,q.y*r[1]*(1+.075*q.x),q.z*r[2]));p.co=c+rot@q
 parts.append(o);normals(o)
def samples(rows,step=.024,linear=False):
 points=[]
 for j in range(len(rows)-1):
  A=rows[max(0,j-1)];B=rows[j];C=rows[j+1];D=rows[min(len(rows)-1,j+2)];n=max(2,math.ceil((Vector(B[:3])-Vector(C[:3])).length/step))
  for k in range(n):
   t=k/n
   q=[B[c]*(1-t)+C[c]*t if linear else .5*(2*B[c]+(-A[c]+C[c])*t+(2*A[c]-5*B[c]+4*C[c]-D[c])*t*t+(-A[c]+3*B[c]-3*C[c]+D[c])*t*t*t)for c in range(3)]
   points.append(q+[B[3]*(1-t)+C[3]*t,B[4]*(1-t)+C[4]*t])
 return points+[rows[-1]]
def path_mesh(path,cut=False):
 rows=samples(path['points'],linear=cut);verts=[];faces=[];N=3 if cut else 12
 for j,p in enumerate(rows):
  c=Vector(p[:3]);T=(Vector(rows[min(j+1,len(rows)-1)][:3])-Vector(rows[max(0,j-1)][:3])).normalized();u=Vector((0,-1,0));u-=T*u.dot(T);u.normalize();b=T.cross(u).normalized()
  if cut:
   # Outside/front wide mouth and one internal point. The return is an angular
   # finite wedge; it does not form a repeated round or full-height tube groove.
   offsets=[u*(p[4]*1.5)+b*p[3],u*(p[4]*1.5)-b*p[3],-u*p[4]*.9]
   verts.extend([tuple(c+x)for x in offsets])
  else:
   for k in range(N):
    a=k*math.tau/N;lobes=1+.095*math.sin(3*a+j*.065+len(parts)*.71)+.040*math.sin(5*a+j*.043);verts.append(tuple(c+u*(math.cos(a)*p[4]*lobes)+b*(math.sin(a)*p[3]*lobes)))
 for j in range(len(rows)-1):
  for k in range(N):faces.append([j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k])
 faces.append(list(reversed(range(N))));faces.append([(len(rows)-1)*N+k for k in range(N)])
 me=bpy.data.meshes.new(path['id']);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(path['id'],me);bpy.context.collection.objects.link(o);normals(o);return o
for v in plan['volumes']:mass(v)
for path in plan['paths']:parts.append(path_mesh(path))
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name='Continuous aged trunk and primary branches';rem=o.modifiers.new('Short masses and unequal root union','REMESH');rem.mode='VOXEL';rem.voxel_size=plan['voxel_size'];rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
precut_triangles=sum(len(p.vertices)-2 for p in o.data.polygons)
for cut in plan['blind_clefts']:
 tool=path_mesh(cut,True);bpy.context.view_layer.objects.active=o;mod=o.modifiers.new(cut['id'],'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=tool;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(tool,do_unlink=True)
# Re-grid boolean slivers once, preserving the angular finite carve and its own
# endpoint; then one weak smooth pass. Avoid a global Subsurf rubber surface.
rem=o.modifiers.new('Editable sculpt surface after finite real carving','REMESH');rem.mode='VOXEL';rem.voxel_size=plan['voxel_size']*.78;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
sm=o.modifiers.new('One weak grid relaxation','SMOOTH');sm.factor=plan['surface_smooth_factor'];sm.iterations=plan['surface_smooth_iterations'];bpy.ops.object.modifier_apply(modifier=sm.name);o.data.calc_loop_triangles();ratio=min(1,plan['maximum_final_triangles']/len(o.data.loop_triangles));dec=o.modifiers.new('Surface density budget preserving macro carve','DECIMATE');dec.ratio=ratio;dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name);normals(o);me=o.data
for face in me.polygons:face.use_smooth=True
# Store continuous material coordinates as provisional growth fields. They are
# not claimed a validated bark mapping before the ordinary-distance shape gate.
mainrows=[[.14,.025,.36,.20,.18],[.13,.025,.65,.23,.19],[-.12,.045,.94,.215,.16],[-.12,.07,1.18,.175,.15],[.13,.11,1.36,.10,.09],[.22,.025,1.52,.075,.06],[.16,0,1.66,.085,.06],[.4,.01,1.91,.028,.022]]
allpaths=[('main',mainrows)]+[(p['id'],p['points'])for p in plan['paths']];segments=[]
for name,rows in allpaths:
 run=0
 for A,B in zip(rows,rows[1:]):
  a=Vector(A[:3]);b=Vector(B[:3]);delta=b-a;length=delta.length;segments.append((name,a,delta,length,run,A[3],B[3]));run+=length
weights={name:[]for name,_ in allpaths};fields=[];masks=[]
for v in me.vertices:
 p=v.co;near=[]
 for name,a,delta,length,start,ra,rb in segments:
  t=max(0,min(1,(p-a).dot(delta)/(length*length)));q=a+delta*t;dist=(p-q).length;near.append((dist,name,q,delta.normalized(),start+t*length,ra*(1-t)+rb*t))
 nearest=min(near,key=lambda r:r[0]);main=min((r for r in near if r[1]=='main'),key=lambda r:r[0]);_,name,q,T,L,cal=nearest;u=Vector((0,-1,0));u-=T*u.dot(T);u.normalize();b=T.cross(u);D=p-q;angle=math.atan2(D.dot(b),D.dot(u))/math.tau+.5
 _,_,mq,mT,mL,_=main;mu=Vector((0,-1,0));mu-=mT*mu.dot(mT);mu.normalize();mb=mT.cross(mu);md=p-mq;ma=math.atan2(md.dot(mb),md.dot(mu))/math.tau+.5;branchblend=0 if name=='main'else min(.95,max(0,(main[0]-nearest[0])/.11));fields.append(((ma,mL),(angle,L),(branchblend,min(1,cal/.22))));weights[name].append(v.index)
 # Scar/front mask remains a rough role marker pending actual frozen-geometry
 # material evaluation; do not use it as evidence that the shari is finished.
 dead=max(0,min(1,(-p.y+.005)/.19))*(1 if p.z<1.27 else.25);masks.append((.55,dead,.28,1))
for name,ids in weights.items():
 if ids:o.vertex_groups.new(name=name).add(ids,1,'REPLACE')
for name in ['Growth direction','Branch growth direction','Branch blend and calibre']:me.uv_layers.new(name=name)
col=me.color_attributes.new(name='Provisional wood roles',type='FLOAT_COLOR',domain='POINT')
for c,v in zip(col.data,masks):c.color=v
for loop in me.loops:
 for i,layer in enumerate(me.uv_layers):layer.data[loop.index].uv=fields[loop.vertex_index][i]
mat=bpy.data.materials.new('Unfinished dry wood shape review');mat.diffuse_color=(.34,.32,.29,1);me.materials.append(mat);o['authoring_version']=version;o['construction']=plan['method'];o['photo_origin_status']=plan['source_relation'];o['stage']='Editable sculpt surface, provisional UV/masks; not selected for shader finish';o['plan_sha256']=hashlib.sha256((R/'design/sculpt-plan.json').read_bytes()).hexdigest()
me.calc_loop_triangles();tri=[tuple(t.vertices)for t in me.loop_triangles];bm=bmesh.new();bm.from_mesh(me);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);areas=[f.calc_area()for f in bm.faces];bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in me.vertices],tri,all_triangles=True,epsilon=1e-8);pairs=[(i,j)for i,j in tree.overlap(tree)if i<j and set(tri[i]).isdisjoint(tri[j])]
adj=[set()for _ in me.vertices]
for t in tri:
 for a,b in zip(t,t[1:]+t[:1]):adj[a].add(b);adj[b].add(a)
pending=set(range(len(adj)));sizes=[]
while pending:
 seed=pending.pop();stack=[seed];size=1
 while stack:
  for i in adj[stack.pop()]:
   if i in pending:pending.remove(i);stack.append(i);size+=1
 sizes.append(size)
inspection={'vertices':len(me.vertices),'faces':len(me.polygons),'triangles':len(tri),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'components':sizes,'minimum_area':min(areas),'euler':len(me.vertices)-len(me.edges)+len(me.polygons),'pre_carve_triangles':precut_triangles,'bounds':{'min':[min(v.co[k]for v in me.vertices)for k in range(3)],'max':[max(v.co[k]for v in me.vertices)for k in range(3)]},'aesthetic_pass':False};(R/'qa/geometry-inspection.json').write_text(json.dumps(inspection,indent=2)+'\n');print(json.dumps(inspection),flush=True);assert boundary==nonmanifold==len(pairs)==0 and len(sizes)==1 and volume>0 and min(areas)>1e-12 and len(tri)<=plan['maximum_final_triangles'],inspection
record={'version':version,'inspection':inspection,'positions_sha256':hashlib.sha256(json.dumps([list(v.co)for v in me.vertices]).encode()).hexdigest(),'faces_sha256':hashlib.sha256(json.dumps([list(f.vertices)for f in me.polygons]).encode()).hexdigest(),'groups':{name:ids for name,ids in weights.items()if ids},'editable_surface':True,'modifier_baked':True};(R/'sculpt/sculpt-record.json').write_text(json.dumps(record,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'));bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'native_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
