from pathlib import Path
import bpy,bmesh,json,math,hashlib,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];plan=json.loads((R/'design/sections.json').read_text());version=plan['version'];assert not(R/'models'/f'{version}.glb').exists()
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
parts=[];fields=[]
def normal(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));
 if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
 bm.to_mesh(o.data);bm.free()
def sample(points):
 out=[]
 for i in range(len(points)-1):
  A=points[max(0,i-1)];B=points[i];C=points[i+1];D=points[min(len(points)-1,i+2)];n=max(3,math.ceil((Vector(B[:3])-Vector(C[:3])).length/.015))
  # Centripetal-ish bounded Hermite tangents: spatial overshoot limited to
  # local chord rather than a global periodic S-curve.
  chord=Vector(C[:3])-Vector(B[:3]);ta=(Vector(C[:3])-Vector(A[:3]))*.5;tb=(Vector(D[:3])-Vector(B[:3]))*.5
  if ta.length>chord.length:ta*=chord.length/ta.length
  if tb.length>chord.length:tb*=chord.length/tb.length
  for k in range(n):
   t=k/n;v=Vector(B[:3])*(2*t**3-3*t*t+1)+ta*(t**3-2*t*t+t)+Vector(C[:3])*(-2*t**3+3*t*t)+tb*(t**3-t*t);q=t*t*(3-2*t)
   out.append(list(v)+[B[j]*(1-q)+C[j]*q for j in range(3,7)])
 return out+[points[-1]]
for path in plan['paths']:
 rows=sample(path['points']);verts=[];faces=[];N=24;arclen=0
 for j,p in enumerate(rows):
  c=Vector(p[:3]);T=(Vector(rows[min(j+1,len(rows)-1)][:3])-Vector(rows[max(0,j-1)][:3])).normalized();front=Vector((0,-1,0));front-=T*front.dot(T);front.normalize();side=T.cross(front).normalized();roll=math.radians(p[5]);u=front*math.cos(roll)+side*math.sin(roll);b=side*math.cos(roll)-front*math.sin(roll)
  if j:arclen+=(c-Vector(rows[j-1][:3])).length
  fields.append((path['id'],path['role'],c,T,u,b,p[3],p[4],arclen))
  for k in range(N):
   a=math.tau*k/N;angle=(a+.35+math.pi)%math.tau-math.pi
   # ONE eccentric concavity and different broad lobes; no two parallel rails.
   eccentric=1+.11*math.cos(a-1.1)+.055*math.cos(3*a+.6)-p[6]*math.exp(-(angle/.60)**2)
   # Section-to-section small calibre asymmetry tracks local growth, not noise.
   eccentric+=.025*math.cos(2*a+.7+p[2]*1.3)
   verts.append(tuple(c+u*(p[4]*math.cos(a)*eccentric)+b*(p[3]*math.sin(a)*eccentric)))
 for j in range(len(rows)-1):
  for k in range(N):faces.append([j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k])
 faces.append(list(reversed(range(N))));faces.append([(len(rows)-1)*N+k for k in range(N)])
 me=bpy.data.meshes.new(path['id']+' authored sections');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(path['id'],me);bpy.context.collection.objects.link(o);normal(o);parts.append(o)
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name='Continuous aged trunk and primary branches';rem=o.modifiers.new('Deep overlapping growth union','REMESH');rem.mode='VOXEL';rem.voxel_size=plan['voxel_size'];rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
sm=o.modifiers.new('One limited union relaxation','SMOOTH');sm.factor=.20;sm.iterations=2;bpy.ops.object.modifier_apply(modifier=sm.name);o.data.calc_loop_triangles();pre=len(o.data.loop_triangles);dec=o.modifiers.new('Native surface budget','DECIMATE');dec.ratio=min(1,plan['target_triangles']/pre);dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name);normal(o);me=o.data
for f in me.polygons:f.use_smooth=True
# Provisional growth fields, independently assess after gray shape acceptance.
uvs=[me.uv_layers.new(name=n) for n in ['Main growth surface','Branch growth surface','Collar transition and calibre']];color=me.color_attributes.new(name='Continuous growth roles',type='FLOAT_COLOR',domain='POINT');me.color_attributes.active_color=color;vfields=[];groups={p['id']:[]for p in plan['paths']}
for v in me.vertices:
 p=v.co;rank=sorted(fields,key=lambda f:(p-f[2]).length);f=rank[0];main=min((q for q in fields if q[0]=='main'),key=lambda q:(p-q[2]).length)
 def uv(q):
  d=p-q[2];return (math.atan2(d.dot(q[5]),d.dot(q[4]))/math.tau+.5,q[8])
 blend=0 if f[0]=='main'else min(.95,max(0,((p-main[2]).length-(p-f[2]).length)/.11));vfields.append((uv(main),uv(f),(blend,1-min(1,f[6]/.18))))
 groups[f[0]].append(v.index);front=(p-main[2]).normalized().dot(main[4]);scar=max(0,min(1,(front-.35)/.6));color.data[v.index].color=(.55,scar,.25,1)
for loop in me.loops:
 for k,u in enumerate(uvs):u.data[loop.index].uv=vfields[loop.vertex_index][k]
for name,ids in groups.items():
 if ids:o.vertex_groups.new(name=name).add(ids,1,'REPLACE')
mat=bpy.data.materials.new('wood provisional gray review');mat.diffuse_color=(.30,.29,.27,1);mat.roughness=1;me.materials.append(mat);o['authoring_version']=version;o['construction']=plan['method'];o['stage']='Unadopted gray form; material fields provisional';o['plan_sha256']=hashlib.sha256((R/'design/sections.json').read_bytes()).hexdigest()
me.calc_loop_triangles();tri=[tuple(t.vertices)for t in me.loop_triangles];bm=bmesh.new();bm.from_mesh(me);vol=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);areas=[f.calc_area()for f in bm.faces];bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in me.vertices],tri,all_triangles=True,epsilon=1e-9);pairs=[(i,j)for i,j in tree.overlap(tree)if i<j and set(tri[i]).isdisjoint(tri[j])];adj=[set()for _ in me.vertices]
for t in tri:
 for a,b in zip(t,t[1:]+t[:1]):adj[a].add(b);adj[b].add(a)
pending=set(range(len(adj)));components=[]
while pending:
 seed=pending.pop();stack=[seed];n=1
 while stack:
  for i in adj[stack.pop()]:
   if i in pending:pending.remove(i);stack.append(i);n+=1
 components.append(n)
check={'version':version,'vertices':len(me.vertices),'triangles':len(tri),'pre_decimate_triangles':pre,'volume':vol,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'components':components,'minimum_area':min(areas),'bounds':{'min':[min(v.co[k]for v in me.vertices)for k in range(3)],'max':[max(v.co[k]for v in me.vertices)for k in range(3)]},'aesthetic_pass':False};(R/'qa/geometry-inspection.json').write_text(json.dumps(check,indent=2)+'\n');print(json.dumps(check),flush=True);assert boundary==nonmanifold==len(pairs)==0 and len(components)==1 and vol>0 and min(areas)>1e-12
record={'version':version,'positions_sha256':hashlib.sha256(json.dumps([list(v.co)for v in me.vertices]).encode()).hexdigest(),'faces_sha256':hashlib.sha256(json.dumps([list(f.vertices)for f in me.polygons]).encode()).hexdigest(),'normals_sha256':hashlib.sha256(json.dumps([list(v.normal)for v in me.vertices]).encode()).hexdigest(),'uv_sha256':{u.name:hashlib.sha256(json.dumps([list(v.uv)for v in u.data]).encode()).hexdigest()for u in me.uv_layers},'color_sha256':hashlib.sha256(json.dumps([list(c.color)for c in color.data]).encode()).hexdigest(),'groups':{n:len(ids)for n,ids in groups.items()},'geometry':check,'form_frozen':False};(R/'sculpt/sculpt-record.json').write_text(json.dumps(record,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'),compress=True);bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'blend_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
