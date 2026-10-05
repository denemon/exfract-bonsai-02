from pathlib import Path
import bpy,bmesh,json,math,os,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];version='carved-v02';plan=json.loads((R/'design/direct-sculpt-plan-v02.json').read_text());assert not(R/'models'/f'{version}.glb').exists();assert os.statvfs(R).f_bavail*os.statvfs(R).f_frsize>=2147483648
bpy.ops.wm.open_mainfile(filepath=str(R/'models/carved-v01-editable.blend'));o=next(x for x in bpy.data.objects if x.type=='MESH');me=o.data;me.calc_loop_triangles();tri=[tuple(t.vertices)for t in me.loop_triangles];original_tri=tri.copy();original=[v.co.copy()for v in me.vertices];normals=[v.normal.copy()for v in me.vertices];tree=BVHTree.FromPolygons(original,tri,all_triangles=True,epsilon=1e-8);g=plan['surface_gate'];counts={};maxmove={}
def fade(t):
 if t<=.58:return 1
 if t>=1:return 0
 q=(t-.58)/.42;return 1-q*q*(3-2*q)
def mask(p,c,r,axes=(0,2)):
 return fade(math.sqrt(sum(((p[ax]-cc)/rr)**2 for ax,cc,rr in zip(axes,c,r))))
def gate(n,d):
 v=n.dot(d)
 if v<=g['normal_inward_dot_max']:return 1
 if v>=g['normal_fade_end']:return 0
 q=(v-g['normal_inward_dot_max'])/(g['normal_fade_end']-g['normal_inward_dot_max']);return 1-q*q*(3-2*q)
def capped(i,delta):
 if delta.length<1e-12:return delta
 direction=delta.normalized();hit,normal,index,dist=tree.ray_cast(original[i]+direction*.00008,direction,1.0)
 if hit is not None and dist>1e-4:
  delta*=min(1,max(0,dist*g['maximum_fraction_to_next_surface'])/delta.length)
 return delta
for shave in plan['plane_shaves']:
 changed=0;largest=0
 for i,v in enumerate(me.vertices):
  p=original[i];w=mask(p,shave['xz_center'],shave['xz_radius'])
  if shave.get('union_mask'):u=shave['union_mask'];w=max(w,mask(p,u['xz_center'],u['xz_radius']))
  if p.y>g['front_y_max']:continue
  w*=gate(normals[i],Vector((0,1,0)))
  if w<=0:continue
  cx,cz=shave['xz_center'];target=shave['plane_origin_y']+shave['slope_x']*(p.x-cx)+shave['slope_z']*(p.z-cz)
  dy=min(shave['maximum_inward_y'],max(0,target-p.y)*(1-g['plane_retained_depth_fraction']))*w
  if dy>0:d=capped(i,Vector((0,dy,0)));v.co.y=max(v.co.y,original[i].y+d.y);changed+=1;largest=max(largest,d.length)
 counts[shave['id']]=changed;maxmove[shave['id']]=largest
side=plan['right_body_plane'];changed=0;largest=0
for i,v in enumerate(me.vertices):
 p=original[i];w=mask(p,side['zy_center'],side['zy_radius'],(2,1))*gate(normals[i],Vector((-1,0,0)));cz,cy=side['zy_center'];target=side['plane_origin_x']+side['slope_z']*(p.z-cz)+side['slope_y']*(p.y-cy);dx=min(side['maximum_inward_x'],max(0,p.x-target)*.90)*w
 if p.z>.78:w*=fade((p.z-.78)/.08);dx*=fade((p.z-.78)/.08)
 if dx>0:d=capped(i,Vector((-dx,0,0)));v.co+=d;changed+=1;largest=max(largest,d.length)
counts[side['id']]=changed;maxmove[side['id']]=largest
for stroke in plan['real_geometry_strokes']:
 changed=0;largest=0;direction=Vector(stroke['direction']).normalized()
 for i,v in enumerate(me.vertices):
  p=original[i]
  if p.y>g['stroke_front_y_max']:continue
  strength=gate(normals[i],direction)
  if strength==0:continue
  best=0
  for j,(a,b)in enumerate(zip(stroke['xz_points'],stroke['xz_points'][1:])):
   q=Vector((p.x,p.z));A=Vector(a);B=Vector(b);D=B-A;t=max(0,min(1,(q-A).dot(D)/D.length_squared));dist=(q-(A+D*t)).length;width=stroke['widths'][j]*(1-t)+stroke['widths'][j+1]*t;depth=stroke['depths'][j]*(1-t)+stroke['depths'][j+1]*t
   # Flat-bottom inner face and finite feather: major real relief, not normal.
   f=fade(dist/width);best=max(best,depth*f)
  if best>0:d=capped(i,direction*(best*strength));v.co.y=max(v.co.y,original[i].y+d.y);changed+=1;largest=max(largest,d.length)
 counts[stroke['id']]=changed;maxmove[stroke['id']]=largest
me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.calc_loop_triangles();tri=[tuple(t.vertices)for t in me.loop_triangles];bm=bmesh.new();bm.from_mesh(me);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);areas=[f.calc_area()for f in bm.faces];bm.free();tree2=BVHTree.FromPolygons([v.co.copy()for v in me.vertices],tri,all_triangles=True,epsilon=1e-8);pairs=[(i,j)for i,j in tree2.overlap(tree2)if i<j and set(tri[i]).isdisjoint(tri[j])];adj=[set()for _ in me.vertices]
for t in tri:
 for a,b in zip(t,t[1:]+t[:1]):adj[a].add(b);adj[b].add(a)
pending=set(range(len(adj)));sizes=[]
while pending:
 seed=pending.pop();stack=[seed];size=1
 while stack:
  for i in adj[stack.pop()]:
   if i in pending:pending.remove(i);stack.append(i);size+=1
 sizes.append(size)
probes=[]
for x,z in [(.12,.45),(.10,.60),(-.10,.80),(-.20,1.03),(-.10,1.16)]:
 hits=[];start=Vector((x,-1,z))
 for _ in range(12):
  hit,n,idx,dist=tree2.ray_cast(start,Vector((0,1,0)),2)
  if hit is None:break
  hits.append(hit.y);start=hit+Vector((0,.0002,0))
 probes.append({'x':x,'z':z,'y_intersections':hits,'occupied_intervals':[[a,b]for a,b in zip(hits[::2],hits[1::2])]})
inspection={'version':version,'vertices':len(me.vertices),'faces':len(me.polygons),'triangles':len(tri),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'intersection_samples':pairs[:15],'components':sizes,'minimum_area':min(areas),'euler':len(me.vertices)-len(me.edges)+len(me.polygons),'bounds':{'min':[min(v.co[k]for v in me.vertices)for k in range(3)],'max':[max(v.co[k]for v in me.vertices)for k in range(3)]},'same_topology':tri==original_tri,'operations_vertex_count':counts,'maximum_displacement_by_operation':maxmove,'depth_probes':probes,'aesthetic_pass':False}
(R/'qa/geometry-inspection-v02.json').write_text(json.dumps(inspection,indent=2)+'\n');print(json.dumps(inspection),flush=True)
assert boundary==nonmanifold==len(pairs)==0 and len(sizes)==1 and volume>0 and min(areas)>1e-12,inspection
o['authoring_version']=version;o['construction']='Baked direct finite plane/chisel sculpt; initial volume blocking retained read-only';o['stage']='Gray/night shape gate, provisional UV/masks; not selected for shader finish';o['plan_sha256']=hashlib.sha256((R/'design/direct-sculpt-plan-v02.json').read_bytes()).hexdigest()
record={'version':version,'positions_sha256':hashlib.sha256(json.dumps([list(v.co)for v in me.vertices]).encode()).hexdigest(),'faces_sha256':hashlib.sha256(json.dumps([list(f.vertices)for f in me.polygons]).encode()).hexdigest(),'uv_sha256':{u.name:hashlib.sha256(json.dumps([list(v.uv)for v in u.data]).encode()).hexdigest()for u in me.uv_layers},'groups':[(g.name,len([v for v in me.vertices if any(a.group==g.index for a in v.groups)]))for g in o.vertex_groups],'inspection':inspection,'editable_surface':True,'modifiers':len(o.modifiers)}
(R/'sculpt/sculpt-record-v02.json').write_text(json.dumps(record,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'));bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'native_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
